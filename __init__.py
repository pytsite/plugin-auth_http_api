"""PytSite Auth HTTP API Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from pytsite import lang
    from plugins import assetman

    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_js(__name__, babelify=True)
    assetman.js_module('auth-http-api', __name__ + '@js/auth-http-api')


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)
    assetman.build_translations()


def plugin_load_uwsgi():
    from plugins import http_api
    from . import _controllers, _eh

    # Sign-up, sign-in, sign-out
    http_api.handle('POST', 'auth/sign-up', _controllers.PostSignUp,
                    'auth_http_api@post_sign_up')
    http_api.handle('POST', 'auth/sign-in', _controllers.PostSignIn,
                    'auth_http_api@post_sign_in')
    http_api.handle('DELETE', 'auth/sign-in', _controllers.DeleteSignIn,
                    'auth_http_api@delete_sign_in')

    # # User HTTP API
    http_api.handle('GET', 'auth/users', _controllers.GetUsers,
                    'auth_http_api@get_users')
    http_api.handle('GET', 'auth/users/<uid>', _controllers.GetUser,
                    'auth_http_api@get_user')
    http_api.handle('PATCH', 'auth/users/<uid>', _controllers.PatchUser,
                    'auth_http_api@patch_user')
    http_api.handle('GET', 'auth/users/<uid>/follows', _controllers.GetUserFollowsOrFollowers,
                    'auth_http_api@get_user_follows')
    http_api.handle('GET', 'auth/users/<uid>/followers', _controllers.GetUserFollowsOrFollowers,
                    'auth_http_api@get_user_followers')

    # Me HTTP API
    http_api.handle('GET', 'auth/me', _controllers.GetMe,
                    'auth_http_api@get_me')
    http_api.handle('PATCH', 'auth/me', _controllers.PatchMe,
                    'auth_http_api@patch_me')
    http_api.handle('GET', 'auth/me/follows>', _controllers.GetMeFollows,
                    'auth_http_api@get_me_follows')
    http_api.handle('POST', 'auth/me/follows/<uid>', _controllers.PostMeFollows,
                    'auth_http_api@post_me_follows')
    http_api.handle('DELETE', 'auth/me/follows/<uid>', _controllers.DeleteMeFollows,
                    'auth_http_api@delete_me_follows')
    http_api.handle('GET', 'auth/me/blocked_users', _controllers.GetMeBlockedUsers,
                    'auth_http_api@get_me_blocked_users')
    http_api.handle('POST', 'auth/me/blocked_users/<uid>', _controllers.PostMeBlockedUsers,
                    'auth_http_api@post_me_blocked_users')
    http_api.handle('DELETE', 'auth/me/blocked_users/<uid>', _controllers.DeleteMeBlockedUsers,
                    'auth_http_api@delete_me_blocked_users')

    http_api.on_pre_request(_eh.http_api_pre_request)
