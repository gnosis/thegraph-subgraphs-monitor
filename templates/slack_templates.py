
def get_slack_notification_message(subgraph_name: str, subgraph_version: str):
    """
    Get slack message template with defined values
    :param subgraph_name:
    :param subgraph_version:
    :return:
    """

    # Subgraph version valid values
    assert(subgraph_version in ['current', 'pending']), 'Subgraph version type is not valid'

    # Different titles for each of subgraph version types
    if subgraph_version == 'current':
        main_title = ":rotating_light: `Subgraph status is NOT OK`"
    elif subgraph_version == 'pending':
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
                        'text': f'*Version (current|pending):*\n {subgraph_version}'
                    }
                ]
            }
        ]
    }

    return message
