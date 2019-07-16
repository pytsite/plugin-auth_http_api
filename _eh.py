"""PytSite Auth HTTP API Plugin Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router, http
from plugins import auth


def http_api_pre_request():
    access_token = None
    auth_header = router.request().headers.get('Authorization', '').split(' ')

    if len(auth_header) == 2 and auth_header[0].lower() == 'token':
        access_token = auth_header[1].strip()

    if not access_token:
        return

    try:
        # Authorize user by access token
        auth.switch_user(auth.get_user(access_token=access_token))
        auth.prolong_access_token(access_token)

    except (auth.error.InvalidAccessToken, auth.error.UserNotFound, auth.error.AuthenticationError) as e:
        raise http.error.Forbidden(response=http.JSONResponse({'error': str(e)}))
