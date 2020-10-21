

def get_slack_current_subgraph_notification_message(subgraph_name: str, subgraph_version: str,
                                                    subgraph_network: str, subgraph_last_block_number: str,
                                                    infura_last_block_number: str):
    """
    Get slack message template with defined values
    :param subgraph_name:
    :param subgraph_version:
    :return:
    """

    main_title = ":rotating_light: `Subgraph status is NOT OK`"

    message = {
        'text': 'Subgraph is NOT OK status',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': main_title
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*Subgraph name:*\n {subgraph_name}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Version (current|pending):*\n `current`'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Subgraph last block:*\n {subgraph_last_block_number}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Infura last block:*\n {infura_last_block_number}'
                    }
                ]
            }
        ]
    }

    return message


def get_slack_pending_subgraph_notification_message(subgraph_name: str):
    """
    Get slack message template with defined values
    :param subgraph_name:
    :param subgraph_version:
    :return:
    """

    main_title = ":warning: `Subgraph status is NOT OK`"

    message = {
        'text': 'Subgraph is NOT OK status',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': main_title
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*Subgraph name:*\n {subgraph_name}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*Version (current|pending):*\n `pending`'
                    }
                ]
            }
        ]
    }

    return message
