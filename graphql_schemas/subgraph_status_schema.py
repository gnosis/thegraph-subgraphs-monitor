import sgqlc.types


subgraph_status_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class BigInt(sgqlc.types.Scalar):
    __schema__ = subgraph_status_schema


Boolean = sgqlc.types.Boolean

class Bytes(sgqlc.types.Scalar):
    __schema__ = subgraph_status_schema


ID = sgqlc.types.ID

String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################

########################################################################
# Output Objects and Interfaces
########################################################################
class ChainIndexingStatus(sgqlc.types.Interface):
    __schema__ = subgraph_status_schema
    __field_names__ = ('network',)
    network = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='network')


class EthereumBlock(sgqlc.types.Type):
    __schema__ = subgraph_status_schema
    __field_names__ = ('hash', 'number')
    hash = sgqlc.types.Field(sgqlc.types.non_null(Bytes), graphql_name='hash')
    number = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='number')


class Query(sgqlc.types.Type):
    __schema__ = subgraph_status_schema
    __field_names__ = ('indexing_statuses_for_subgraph_name', 'indexing_statuses')
    indexing_statuses_for_subgraph_name = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SubgraphIndexingStatus'))), graphql_name='indexingStatusesForSubgraphName', args=sgqlc.types.ArgDict((
        ('subgraph_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='subgraphName', default=None)),
))
    )
    indexing_statuses = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SubgraphIndexingStatus'))), graphql_name='indexingStatuses', args=sgqlc.types.ArgDict((
        ('subgraphs', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='subgraphs', default=None)),
))
    )


class SubgraphIndexingStatus(sgqlc.types.Type):
    __schema__ = subgraph_status_schema
    __field_names__ = ('subgraph', 'synced', 'failed', 'error', 'chains', 'node')
    subgraph = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='subgraph')
    synced = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='synced')
    failed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='failed')
    error = sgqlc.types.Field(String, graphql_name='error')
    chains = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ChainIndexingStatus))), graphql_name='chains')
    node = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='node')


class EthereumIndexingStatus(sgqlc.types.Type, ChainIndexingStatus):
    __schema__ = subgraph_status_schema
    __field_names__ = ('chain_head_block', 'earliest_block', 'latest_block')
    chain_head_block = sgqlc.types.Field(EthereumBlock, graphql_name='chainHeadBlock')
    earliest_block = sgqlc.types.Field(EthereumBlock, graphql_name='earliestBlock')
    latest_block = sgqlc.types.Field(EthereumBlock, graphql_name='latestBlock')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
subgraph_status_schema.query_type = Query
subgraph_status_schema.mutation_type = None
subgraph_status_schema.subscription_type = None

