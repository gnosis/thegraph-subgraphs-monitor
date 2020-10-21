#!/usr/bin/env python
import config
import logging
import os
import traceback

from services.thegraph_service import ThegraphService, StatusEndpointUnavailableException
from services.infura_service import InfuraProvider

import requests
from templates import slack_templates

# Read log level as environment variable (by default INFO)
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
assert (LOGLEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), 'LOGLEVEL is not valid'

# Configure logs format
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=LOGLEVEL)


if __name__ == '__main__':

    # Check status of each defined subgraph
    for subgraph in config.subgraphs:

        try:
            # Subgraph information
            subgraph_name = subgraph['name']
            slack_incoming_webhook = subgraph['notifications']['slack']['incoming_webhook']

            thegraph_service = ThegraphService(subgraph_name=subgraph_name)
            infura_service = InfuraProvider()

            if not thegraph_service.is_current_subgraph_version_ok():
                subgraph_last_block_number = thegraph_service.get_current_subgraph_last_block_number()
                subgraph_network = thegraph_service.get_current_subgraph_network()
                infura_last_block_number = infura_service.get_latest_block_number_of_network(subgraph_network)

                slack_message = slack_templates.get_slack_current_subgraph_notification_message(
                    subgraph_name=subgraph_name,
                    subgraph_version='current',
                    subgraph_network=subgraph_network,
                    subgraph_last_block_number=subgraph_last_block_number,
                    infura_last_block_number=infura_last_block_number
                    )
                # Send notification to Slack
                # Using the json parameter in the request will change the Content-Type to application/json.
                requests.post(url=slack_incoming_webhook,
                              json=slack_message,
                              timeout=2)
            else:
                logging.debug(f'Subgraph {subgraph_name} CURRENT version is OK')

            if not thegraph_service.is_pending_subgraph_version_ok():
                slack_message = slack_templates.get_slack_pending_subgraph_notification_message(
                    subgraph_name=subgraph_name)

                # Send notification to Slack
                # Using the json parameter in the request will change the Content-Type  to application/json.
                requests.post(url=slack_incoming_webhook,
                              json=slack_message,
                              timeout=2)
            else:
                logging.debug(f'Subgraph {subgraph_name} PENDING version is OK')

        except StatusEndpointUnavailableException as unavailable_endpoint:
            logging.error('Thegraph subgraph status endpoint is unavailable. '
                          'No more subgraphs will be checked until status endpoint is available again')

            raise unavailable_endpoint
        except Exception as exception:
            logging.error(f'Exception when checking subgraph {subgraph_name}. Exception: {exception}')
            # Show exception stack trace
            traceback.print_exc()
