from calendar import timegm
import datetime
import jwt


def get_jwt_payload(token_type, user, session_key, expiry_seconds):
    print('expiry_seconds = {}'.format(expiry_seconds))
    now = datetime.datetime.utcnow()
    payload = {
        u'type': token_type,
        u'username': user.username,
        u'email': user.email,
        u'orig_iat': timegm(now.utctimetuple()),
        u'exp': now + datetime.timedelta(seconds=expiry_seconds),
        u'session_key': session_key
    }
    return payload


def get_edraak_refresh_token(user, session_key):
    token = jwt.encode(
        get_jwt_payload(
            token_type='refresh',
            user=user,
            session_key=session_key,
            expiry_seconds=datetime.timedelta(days=14).total_seconds()
        ),
        'my secret key',
        'HS256'
    ).decode('utf-8')

    return token
