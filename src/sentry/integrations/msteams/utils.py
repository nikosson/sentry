from __future__ import absolute_import

from sentry.models import Integration
from sentry.utils.compat import filter
from sentry.utils.http import absolute_uri
from .client import MsTeamsClient

MSTEAMS_MAX_ITERS = 100


def channel_filter(channel, name):
    # the general channel has no name in the list
    # retrieved from the REST API call
    if channel.get("name"):
        return name == channel.get("name")
    else:
        return name == "General"


def get_channel_id(organization, integration_id, name):
    try:
        integration = Integration.objects.get(
            provider="msteams", organizations=organization, id=integration_id
        )
    except Integration.DoesNotExist:
        return None

    team_id = integration.external_id
    client = MsTeamsClient(integration)

    # handle searching for channels first
    channel_list = client.get_channel_list(team_id)
    filtered_channels = list(filter(lambda x: channel_filter(x, name), channel_list))
    if len(filtered_channels) > 0:
        return filtered_channels[0].get("id")

    # handle searching for users
    members = client.get_member_list(team_id, None)
    for i in range(MSTEAMS_MAX_ITERS):
        member_list = members.get("members")
        continuation_token = members.get("continuationToken")

        filtered_members = list(filter(lambda x: x.get("name") == name, member_list))
        if len(filtered_members) > 0:
            # TODO: handle duplicate username case
            user_id = filtered_members[0].get("id")
            tenant_id = filtered_members[0].get("tenantId")
            return client.get_user_conversation_id(user_id, tenant_id)

        if not continuation_token:
            return None

        members = client.get_member_list(team_id, continuation_token)

    return None


def build_welcome_card(signed_params):
    url = u"%s?signed_params=%s" % (absolute_uri("/extensions/msteams/configure/"), signed_params,)
    # TODO: Refactor message creation
    logo = {
        "type": "Image",
        "url": "https://sentry-brand.storage.googleapis.com/sentry-glyph-black.png",
        "size": "Medium",
    }
    welcome = {
        "type": "TextBlock",
        "weight": "Bolder",
        "size": "Large",
        "text": "Welcome to Sentry for Microsoft Teams",
        "wrap": True,
    }
    description = {
        "type": "TextBlock",
        "text": "You can use the Sentry app for Microsoft Teams to get notifications that allow you to assign, ignore, or resolve directly in your chat.",
        "wrap": True,
    }
    instruction = {
        "type": "TextBlock",
        "text": "If that sounds good to you, finish the setup process.",
        "wrap": True,
    }
    button = {
        "type": "Action.OpenUrl",
        "title": "Complete Setup",
        "url": url,
    }
    return {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {"type": "Column", "items": [logo], "width": "auto"},
                    {
                        "type": "Column",
                        "items": [welcome],
                        "width": "stretch",
                        "verticalContentAlignment": "Center",
                    },
                ],
            },
            description,
            instruction,
        ],
        "actions": [button],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2",
    }
