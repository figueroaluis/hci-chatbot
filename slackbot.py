#!/usr/bin/env python3
"""An interface to Slack for chatbots."""

from os import environ
from time import sleep

from slackclient import SlackClient

from oxycsbot import OxyCSBot # FIXME


def get_token():
    """Read the Slack API token from the environment.

    Returns:
        str: The Slack API token.

    Raises:
        NameError: If the TOKEN environment variable is not defined.
    """
    if 'TOKEN' in environ:
        return environ['TOKEN']
    raise NameError('"TOKEN" not defined in environment')


def connect_to_slack():
    """Connect to Slack's real-time messaging interface.

    Returns:
        SlackClient: A Slack API object.
        str: The ID of this client.

    Raises:
        ConnectionError: If the connection to Slack fails.
    """
    slack_client = SlackClient(get_token())
    if not slack_client.rtm_connect(with_team_state=False):
        raise ConnectionError('failed to connect to Slack RTM interface')
    bot_id = slack_client.api_call('auth.test')['user_id']
    return slack_client, bot_id


def get_at_message(event, bot_id):
    """Check if a Slack event is an @-message to the bot.

    Arguments:
        event (dict): Details of the Slack event.
        bot_id (str): The ID of the Slack client.

    Returns:
        str: The message, if it is an @-message directed at the bot. Returns
            None otherwise.
    """
    if event['type'] != 'message' or 'subtype' in event:
        return None
    if ' ' not in event['text']:
        return None
    user_id, message = event['text'].split(' ', maxsplit=1)
    if user_id != ('<@' + bot_id + '>'):
        return None
    return message.strip()


def run(bot_class):
    """Connect the chatbot to Slack.

    After connecting to Slack, this function will loop forever checking for
    messages from Slack. The current interface to Slack only lets through @-
    messages, _not_ direct messages.

    Arguments:
        bot_class (class): The class of the chatbot that will respond.
    """
    slack, bot_id = connect_to_slack()
    bot = bot_class()
    while True:
        for event in slack.rtm_read():
            print(event)
            message = get_at_message(event, bot_id)
            if message:
                channel = event['channel']
                response = bot.respond(message)
                slack.api_call('chat.postMessage', channel=channel, text=response)
        sleep(1)


if __name__ == '__main__':
    run(OxyCSBot) # FIXME
