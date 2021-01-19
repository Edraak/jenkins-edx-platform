from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
import logging
import jwt
import datetime

log = logging.getLogger(__name__)


class EdrrakAccessTokenView(APIView):
    def post(self, request):
        request_access_token = request.POST.get('request_access_token', None)
        if request_access_token is None:
            raise ValueError('Bad request_access_token token')

        edraak_refresh_token = jwt.decode(
            request_access_token,
            'my secret key',
            True,
            options={'verify_exp': True},
            algorithms=['HS256']
        )
        edraak_refresh_token = edraak_refresh_token['refresh_token']

        new_payload = jwt.decode(
            edraak_refresh_token,
            'my secret key',
            True,
            options={'verify_exp': True},
            algorithms=['HS256']
        )

        new_payload[u'exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        new_payload[u'type'] = 'access'
        new_token = jwt.encode(
            new_payload,
            'my secret key',
            'HS256'
        ).decode('utf-8')

        response = JsonResponse({
            'token': new_token
        })
        return response
