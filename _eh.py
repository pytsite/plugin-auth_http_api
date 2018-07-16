"""PytSite Auth HTTP API Plugin Events Handlers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router as _router, http as _http
from plugins import auth as _auth


def http_api_pre_request():
    access_token = None
    auth_header = _router.request().headers.get('Authorization', '').split(' ')

    if len(auth_header) == 2 and auth_header[0].lower() == 'token':
        access_token = auth_header[1].strip()

    if not access_token:
        return

    try:
        # Authorize user by access token
        _auth.switch_user(_auth.get_user(access_token=access_token))
        _auth.prolong_access_token(access_token)

    except (_auth.error.InvalidAccessToken, _auth.error.UserNotFound, _auth.error.AuthenticationError) as e:
        raise _http.error.Forbidden(response=_http.JSONResponse({'error': str(e)}))
