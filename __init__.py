"""PytSite Auth HTTP API Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.t_js(__name__)
        assetman.js_module('auth-http-api', __name__ + '@js/auth-http-api')

    return assetman


def plugin_install():
    _register_assetman_resources().build(__name__)


def plugin_load():
    _register_assetman_resources()


def plugin_load_uwsgi():
    from plugins import http_api
    from . import _controllers, _eh

    # Access token HTTP API
    http_api.handle('POST', 'auth/access-token/<driver>', _controllers.PostAccessToken, 'auth@post_access_token')
    http_api.handle('GET', 'auth/access-token/<token>', _controllers.GetAccessToken, 'auth@get_access_token')
    http_api.handle('DELETE', 'auth/access-token/<token>', _controllers.DeleteAccessToken, 'auth@delete_access_token')
    http_api.handle('POST', 'auth/sign-in/<driver>', 'auth@post_access_token', 'auth@post_sign_in')
    http_api.handle('POST', 'auth/sign-out/<token>', 'auth@delete_access_token', 'auth@post_sign_out')

    # User HTTP API
    http_api.handle('GET', 'auth/is_anonymous', _controllers.IsAnonymous, 'auth@is_anonymous')
    http_api.handle('GET', 'auth/user/<uid>', _controllers.GetUser, 'auth@get_user')
    http_api.handle('GET', 'auth/users', _controllers.GetUsers, 'auth@get_users')
    http_api.handle('PATCH', 'auth/user/<uid>', _controllers.PatchUser, 'auth@patch_user')

    # Following HTTP API
    http_api.handle('GET', 'auth/follows/<uid>', _controllers.GetFollowsOrFollowers, 'auth@get_follows')
    http_api.handle('GET', 'auth/followers/<uid>', _controllers.GetFollowsOrFollowers, 'auth@get_followers')
    http_api.handle('POST', 'auth/follow/<uid>', _controllers.PostFollow, 'auth@post_follow')
    http_api.handle('DELETE', 'auth/follow/<uid>', _controllers.DeleteFollow, 'auth@delete_follow')

    # Block users HTTP API
    http_api.handle('POST', 'auth/block_user/<uid>', _controllers.PostBlockUser, 'auth@post_block_user')
    http_api.handle('DELETE', 'auth/block_user/<uid>', _controllers.DeleteBlockUser, 'auth@delete_block_user')
    http_api.handle('GET', 'auth/blocked_users/<uid>', _controllers.GetBlockedUsers, 'auth@get_blocked_users')

    http_api.on_pre_request(_eh.http_api_pre_request)
