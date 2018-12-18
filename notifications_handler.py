"""
Handlers for notifications
"""


def alert(event, _):
    """
    alert due to new influencing twitter
    """
    print(f'received event = {event}')
