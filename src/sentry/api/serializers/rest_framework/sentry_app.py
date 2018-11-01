from __future__ import absolute_import

from rest_framework import serializers
from rest_framework.serializers import Serializer, ValidationError

from sentry.models import ApiScopes


class ApiScopesField(serializers.WritableField):
    def validate(self, data):
        valid_scopes = ApiScopes()
        if data is None:
            raise ValidationError('Must provide scopes')

        for scope in data:
            if scope not in valid_scopes:
                raise ValidationError(u'{} not a valid scope'.format(scope))


class SentryAppSerializer(Serializer):
    name = serializers.CharField()
    scopes = ApiScopesField()
<<<<<<< HEAD
<<<<<<< HEAD
    webhookUrl = serializers.URLField()
    redirectUrl = serializers.URLField(required=False)
=======
    webhook_url = serializers.URLField()
    redirect_url = serializers.URLField(required=False)
>>>>>>> add redirect_url and overview to ui and letter avatar
=======
    webhookUrl = serializers.URLField()
    redirectUrl = serializers.URLField(required=False)
>>>>>>> camel case webhook url and redirect url
    overview = serializers.CharField(required=False)
