![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)

# Thegraph Subgraphs monitor
A monitor system to check **statuses of subgraphs** that are running on Thegraph platform.

What exactly things does it monitor?
--------------------------------------
- **CURRENT** subgraph version. This is the subgraph version that is used to answer requests to graphql endpoint.
- **PENDING** subgraph version. This is the subgraph version that will replace the current version when it is full synced.

If one of them has `status: FAILED`, a notification message will be sent to the defined Slack channel (using an Slack incoming webhook).

How to use
------------
- Install project requirements: `pip install -r requirements.txt`
- Define subgraphs to monitor in `config.py` file.
- Execute it: `python main.py`

Another tool
------------
- **Graphql schema generator**. This project uses a graphql endpoint to monitor subgraphs 
(https://api.thegraph.com/index-node/graphql). 
If this endpoint schema changes, the command `python tools/graphql_schema_generator.py` has to be executed 
to update the schema definition that this project uses.

Check manually a Subgraph status
-----------------------------------
- Send a HTTP request to https://api.thegraph.com/index-node/graphql using this query:
    ```
    {
        indexingStatusesForSubgraphName(subgraphName: "[SUBGRAPH_NAME]") {
            subgraph
            synced
            failed
            chains {
                network
                ... on EthereumIndexingStatus {
                    earliestBlock { number hash }
                    latestBlock { number hash }
                    chainHeadBlock { number hash }
                }
            }
        }
    }
    ```