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


class Health(sgqlc.types.Enum):
    __schema__ = subgraph_status_schema
    __choices__ = ('healthy', 'unhealthy', 'failed')


ID = sgqlc.types.ID

String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################

########################################################################
# Output Objects and Interfaces
########################################################################
class Block(sgqlc.types.Type):
    __schema__ = subgraph_status_schema
    __field_names__ = ('hash', 'number')
    hash = sgqlc.types.Field(sgqlc.types.non_null(Bytes), graphql_name='hash')
    number = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='number')


class ChainIndexingStatus(sgqlc.types.Interface):
    __schema__ = subgraph_status_schema
    __field_names__ = ('network', 'chain_head_block', 'earliest_block', 'latest_block', 'last_healthy_block')
    network = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='network')
    chain_head_block = sgqlc.types.Field(Block, graphql_name='chainHeadBlock')
    earliest_block = sgqlc.types.Field(Block, graphql_name='earliestBlock')
    latest_block = sgqlc.types.Field(Block, graphql_name='latestBlock')
    last_healthy_block = sgqlc.types.Field(Block, graphql_name='lastHealthyBlock')


class Query(sgqlc.types.Type):
    __schema__ = subgraph_status_schema
    __field_names__ = ('indexing_status_for_current_version', 'indexing_status_for_pending_version', 'indexing_statuses_for_subgraph_name', 'indexing_statuses', 'proof_of_indexing')
    indexing_status_for_current_version = sgqlc.types.Field('SubgraphIndexingStatus', graphql_name='indexingStatusForCurrentVersion', args=sgqlc.types.ArgDict((
        ('subgraph_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='subgraphName', default=None)),
))
    )
    indexing_status_for_pending_version = sgqlc.types.Field('SubgraphIndexingStatus', graphql_name='indexingStatusForPendingVersion', args=sgqlc.types.ArgDict((
        ('subgraph_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='subgraphName', default=None)),
))
    )
    indexing_statuses_for_subgraph_name = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SubgraphIndexingStatus'))), graphql_name='indexingStatusesForSubgraphName', args=sgqlc.types.ArgDict((
        ('subgraph_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='subgraphName', default=None)),
))
    )
    indexing_statuses = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SubgraphIndexingStatus'))), graphql_name='indexingStatuses', args=sgqlc.types.ArgDict((
        ('subgraphs', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='subgraphs', default=None)),
))
    )
    proof_of_indexing = sgqlc.types.Field(Bytes, graphql_name='proofOfIndexing', args=sgqlc.types.ArgDict((
        ('subgraph', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='subgraph', default=None)),
        ('block_hash', sgqlc.types.Arg(sgqlc.types.non_null(Bytes), graphql_name='blockHash', default=None)),
        ('indexer', sgqlc.types.Arg(Bytes, graphql_name='indexer', default=None)),
))
    )


class SubgraphError(sgqlc.types.Type):
    __schema__ = subgraph_status_schema
    __field_names__ = ('message', 'block', 'handler')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')
    block = sgqlc.types.Field(Block, graphql_name='block')
    handler = sgqlc.types.Field(String, graphql_name='handler')


class SubgraphIndexingStatus(sgqlc.types.Type):
    __schema__ = subgraph_status_schema
    __field_names__ = ('subgraph', 'synced', 'health', 'fatal_error', 'non_fatal_errors', 'chains', 'node')
    subgraph = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='subgraph')
    synced = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='synced')
    health = sgqlc.types.Field(sgqlc.types.non_null(Health), graphql_name='health')
    fatal_error = sgqlc.types.Field(SubgraphError, graphql_name='fatalError')
    non_fatal_errors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SubgraphError))), graphql_name='nonFatalErrors')
    chains = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ChainIndexingStatus))), graphql_name='chains')
    node = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='node')


class EthereumIndexingStatus(sgqlc.types.Type, ChainIndexingStatus):
    __schema__ = subgraph_status_schema
    __field_names__ = ()



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
subgraph_status_schema.query_type = Query
subgraph_status_schema.mutation_type = None
subgraph_status_schema.subscription_type = None

