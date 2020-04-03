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

        # Get specified subgraph statuses
        self.subgraph_statuses = self.get_subgraph_statuses()

    def get_subgraph_statuses(self):
        """
        Get subgraph statuses
        :return: bool
        """

        # Operation module helps to create complex queries and interpret the JSON returned into native Python objects
        operation_definition = Operation(subgraph_status_schema.Query)

        operation_definition.indexing_statuses_for_subgraph_name(subgraph_name=self.subgraph_name)
        # Important: we must select explicity which fields we want to request in our Graphql Query
        # In this case we select all possible fields
        operation_definition.indexing_statuses_for_subgraph_name.__fields__()

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
        subgraph_statuses = (operation_definition + subgraph_statuses_json).indexing_statuses_for_subgraph_name

        return subgraph_statuses

    def is_current_subgraph_version_ok(self) -> bool:
        """
        Check if current subgraph version is ok
        :return: bool
        """

        subgraph_statuses = self.subgraph_statuses

        # There can be only 2 subgraphs status as max:
        # - Current version
        # - Pending version if there is
        assert (0 < len(subgraph_statuses) <= 2), 'There can be only 2 subgraph statuses as maximum'

        current_subgraph_status = subgraph_statuses[0]

        return not current_subgraph_status.failed and current_subgraph_status.synced

    def is_pending_subgraph_version_ok(self) -> bool:
        """
        Check if pending subgraph version is ok
        :return: bool
        """

        subgraph_statuses = self.subgraph_statuses

        # There can be only 2 subgraph statuses as max:
        # - Current version
        # - Pending version if there is
        assert (0 < len(subgraph_statuses) <= 2), 'There can be only 2 subgraph statuses as maximum'

        # When there is not a pending subgraph version, status is always ok
        if len(subgraph_statuses) == 2:
            pending_subgraph_status = subgraph_statuses[1]

            return not pending_subgraph_status.failed
        else:
            return True
