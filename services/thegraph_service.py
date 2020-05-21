from logging import getLogger

# Operation generates valid queries, which can be printed out and properly indented.
# Bonus point is that it can be used to later interpret the JSON results into native Python objects.
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint
from graphql_schemas.subgraph_status_schema import subgraph_status_schema


class ThegraphService(Exception):
    pass


class StatusEndpointUnavailableException(Exception):
    pass


class ThegraphService:
    def __init__(self, subgraph_name: str, thegraph_status_url: str = 'https://api.thegraph.com/index-node/graphql'):
        self.subgraph_name = subgraph_name
        self.thegraph_status_url = thegraph_status_url

        # Get subgraph statuses
        self.current_subgraph_status = self.get_current_subgraph_status()
        self.pending_subgraph_status = self.get_pending_subgraph_status()

    def get_current_subgraph_status(self):
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

    def get_pending_subgraph_status(self):
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

        subgraph_status = self.current_subgraph_status

        is_healthy = self._is_subgraph_healthy(subgraph_status)
        is_synced = subgraph_status.synced

        return is_healthy and is_synced

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

    def _is_subgraph_healthy(self, subgraph_status) -> bool:
        """
        Check if a subgraph status is healthy
        """

        return subgraph_status.health.lower() == 'healthy'
