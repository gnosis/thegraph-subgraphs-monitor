#!/usr/bin/env python
import config
import logging
import os

from services.thegraph_service import ThegraphService, StatusEndpointUnavailableException
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

            if not thegraph_service.is_current_subgraph_version_ok():
                # Using the json parameter in the request will change the Content-Type to application/json.
                slack_message = slack_templates.get_slack_notification_message(subgraph_name=subgraph_name,
                                                                               subgraph_version='current')
                # Send notification to Slack
                requests.post(url=slack_incoming_webhook,
                              json=slack_message,
                              timeout=2)
            else:
                logging.debug(f'Subgraph {subgraph_name} CURRENT version is OK')

            if not thegraph_service.is_pending_subgraph_version_ok():
                # Using the json parameter in the request will change the Content-Type  to application/json.
                slack_message = slack_templates.get_slack_notification_message(subgraph_name=subgraph_name,
                                                                               subgraph_version='pending')
                # Send notification to Slack
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
