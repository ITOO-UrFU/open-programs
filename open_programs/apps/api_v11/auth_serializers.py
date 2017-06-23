from rest_framework import serializers, parsers, renderers, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from rest_framework_jwt.settings import api_settings

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model

from django.utils.translation import ugettext_lazy as _

from persons.serializers import PersonSerializer
from persons.models import Person

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def validate_email_custom(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if validate_email_custom(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active and settings.NEED_ACTIVATE:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        payload = jwt_payload_handler(user)

        attrs['user'] = user
        attrs["token"] = jwt_encode_handler(payload)
        return attrs


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_serializer = PersonSerializer
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']

        content = {
            'token': token,
            'person': user_serializer(Person.objects.get(user=user)).data
        }

        return Response(content)

obtain_jwt_token = ObtainAuthToken.as_view()