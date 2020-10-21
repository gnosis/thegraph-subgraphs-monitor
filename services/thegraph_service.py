import logging
import os

# Operation generates valid queries, which can be printed out and properly indented.
# Bonus point is that it can be used to later interpret the JSON results into native Python objects.
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint
from graphql_schemas.subgraph_status_schema import subgraph_status_schema

from .infura_service import InfuraProvider, InfuraEndpointUnavailableException

# Read log level as environment variable (by default INFO)
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
assert (LOGLEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), 'LOGLEVEL is not valid'

# Configure logs format
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=LOGLEVEL)


class ThegraphService(Exception):
    pass


class StatusEndpointUnavailableException(Exception):
    pass


class ThegraphService:
    def __init__(self, subgraph_name: str, thegraph_status_url: str = 'https://api.thegraph.com/index-node/graphql'):
        self.subgraph_name = subgraph_name
        self.thegraph_status_url = thegraph_status_url
        # Use a provider to reuse the same service and not make so many requests to Infura
        self.infura_service = InfuraProvider()

        # Get subgraph statuses
        self.current_subgraph_status = self.fetch_current_subgraph_status()
        self.pending_subgraph_status = self.fetch_pending_subgraph_status()

    def fetch_current_subgraph_status(self):
        """
        Get CURRENT subgraph status
        :return: bool
        """

        # Operation module helps to create complex queries and interpret the JSON returned into native Python objects
        operation_definition = Operation(subgraph_status_schema.Query)

        operation_definition.indexing_status_for_current_version(subgraph_name=self.subgraph_name)

        # Important: we must select explicity which fields we want to request in our Graphql Query
        # In this case we select all possible fields
        operation_definition.indexing_status_for_current_version.__fields__('health', 'synced', 'fatal_error', 'chains')
        # It is needed so that "latest_block" is parsed as it is as subfield
        operation_definition.indexing_status_for_current_version.chains.__fields__()
        operation_definition.indexing_status_for_current_version.chains.latest_block.__fields__()

        # Call the endpoint:
        headers = {}
        endpoint = HTTPEndpoint(self.thegraph_status_url, headers)

        try:
            subgraph_statuses_json = endpoint(operation_definition)
        except Exception:
            raise StatusEndpointUnavailableException()

        # INTERPRET RESULTS INTO NATIVE PYTHON OBJECTS
        # Since we don’t want to cobbler GraphQL fields, we cannot provide nicely named methods.
        # Then we use overloaded methods such as __iadd__, __add__ (`+` symbol), __bytes__(compressed GraphQL
        # representation) and __str__(indented GraphQL representation).
        #
        # A convenience is the `__add__()` (the symbol `+`) to apply the operation to a resulting JSON data,
        # interpreting the results and producing convenient objects
        subgraph_status = (operation_definition + subgraph_statuses_json).indexing_status_for_current_version

        return subgraph_status

    def fetch_pending_subgraph_status(self):
        """
        Get PENDING subgraph status
        :return: bool
        """

        # Operation module helps to create complex queries and interpret the JSON returned into native Python objects
        operation_definition = Operation(subgraph_status_schema.Query)

        operation_definition.indexing_status_for_pending_version(subgraph_name=self.subgraph_name)

        # Important: we must select explicity which fields we want to request in our Graphql Query
        # In this case we select all possible fields
        operation_definition.indexing_status_for_pending_version.__fields__('health', 'synced', 'fatal_error', 'chains')

        # Call the endpoint:
        headers = {}
        endpoint = HTTPEndpoint(self.thegraph_status_url, headers)

        try:
            subgraph_statuses_json = endpoint(operation_definition)
        except Exception:
            raise StatusEndpointUnavailableException()

        # INTERPRET RESULTS INTO NATIVE PYTHON OBJECTS
        # Since we don’t want to cobbler GraphQL fields, we cannot provide nicely named methods.
        # Then we use overloaded methods such as __iadd__, __add__ (`+` symbol), __bytes__(compressed GraphQL
        # representation) and __str__(indented GraphQL representation).
        #
        # A convenience is the `__add__()` (the symbol `+`) to apply the operation to a resulting JSON data,
        # interpreting the results and producing convenient objects
        subgraph_status = (operation_definition + subgraph_statuses_json).indexing_status_for_pending_version

        return subgraph_status

    def is_current_subgraph_version_ok(self) -> bool:
        """
        Check if current subgraph version is ok
        :return: bool
        """
        is_subgraph_ok = None

        subgraph_status = self.current_subgraph_status

        is_healthy = self._is_subgraph_healthy(subgraph_status)

        try:
            is_synced = self.is_current_subgraph_version_synced()

            is_subgraph_ok = is_healthy and is_synced
        except InfuraEndpointUnavailableException:
            logging.error('Infura endpoint to check `synced` status is unavailable (Now only checking healthy status)'
                          'Please, check this! Possible causes: Infura token has reached the limit, Endpoint is down...')

            # When Infura is not available, we only consider healthy status
            is_subgraph_ok = is_healthy

        return is_subgraph_ok

    def is_pending_subgraph_version_ok(self) -> bool:
        """
        Check if pending subgraph version is ok
        :return: bool
        """

        subgraph_status = self.pending_subgraph_status

        # When there is not a pending subgraph version, status is always ok
        if subgraph_status:
            is_healthy = self._is_subgraph_healthy(subgraph_status)

            # Here we do not check if the subgraph is synced because a `pending` subgraph will be always syncing. And when a `pending` subgraphs is synced it changes to `current`
            return is_healthy
        else:
            return True

    def get_current_subgraph_last_block_number(self) -> int:
        """
        Return current subgraph last block number
        :return: int
        """

        subgraph_status = self.current_subgraph_status
        # Convert to string so that it can be used later
        # chains[0] is used because Thegraph has said that right now it only has 1 element. Maybe in the future it has more...
        subgraph_latest_block_number = int(subgraph_status.chains[0].latest_block.number)

        return subgraph_latest_block_number

    def get_current_subgraph_network(self) -> str:
        """
        Return current subgraph network
        :return: str
        """

        subgraph_status = self.current_subgraph_status
        subgraph_network = subgraph_status.chains[0].network.lower()

        return subgraph_network

    def is_current_subgraph_version_synced(self) -> bool:
        """
        Check if current subgraph version is synced against Infura
        Because "synced" property of subgraphs is not useful as it only indicates that a subgraph was synced at some point
        :return: bool
        """

        BLOCKS_TO_CONSIDER_OUT_OF_SYNC = 15

        subgraph_latest_block_number = self.get_current_subgraph_last_block_number()
        subgraph_network = self.get_current_subgraph_network()

        infura_service = self.infura_service
        infura_latest_block_number = infura_service.get_latest_block_number_of_network(subgraph_network)

        return (infura_latest_block_number - subgraph_latest_block_number) < BLOCKS_TO_CONSIDER_OUT_OF_SYNC

    def _is_subgraph_healthy(self, subgraph_status) -> bool:
        """
        Check if a subgraph status is healthy
        """

        return subgraph_status.health.lower() == 'healthy'
