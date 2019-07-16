"""PytSite Auth HTTP API Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import events, util, logger, routing, formatters, validation, lang, reg
from plugins import auth, http_api, query


def _get_access_token_info(token: str) -> dict:
    r = auth.get_access_token_info(token)
    r.update({
        'token': token,
        'created': util.w3c_datetime_str(r['created']),
        'expires': util.w3c_datetime_str(r['expires']),
    })

    return r


class SignUp(routing.Controller):
    """Sign Up Form Submit
    """

    def exec(self):
        # If the user is already authenticated
        if not auth.get_current_user().is_anonymous:
            raise self.forbidden(lang.t('auth_http_api@user_already_authenticated'))

        try:
            auth.sign_up(self.arg('driver'), self.args)
        except auth.error.SignupDisabled as e:
            raise self.forbidden(e)

        return {'status': True}


class SignIn(routing.Controller):
    """Sign In Form Submit
    """

    def exec(self) -> dict:
        # If the user is already authenticated
        if not auth.get_current_user().is_anonymous:
            raise self.forbidden(lang.t('auth_http_api@user_already_authenticated'))

        try:
            user = auth.sign_in(self.arg('driver'), self.args)

            r = {'status': True}
            if self.arg('access_token'):
                r['access_token'] = _get_access_token_info(auth.generate_access_token(user))

            return r

        # User account is not active
        except (auth.error.UserNotActive, auth.error.UserNotConfirmed) as e:
            raise self.warning(e, 401)

        # Any other exception
        except Exception as e:
            # Don't expose reason of error to the outer world
            logger.error(e)
            raise self.unauthorized(lang.t('auth_http_api@authentication_error'))


class SignOut(routing.Controller):
    """Sign out a user
    """

    def exec(self) -> dict:
        try:
            auth.sign_out(auth.get_current_user())

            if 'access_token' in self.args:
                auth.revoke_access_token(self.arg('access_token'))

            return {'status': True}

        except (auth.error.UserNotFound, auth.error.InvalidAccessToken) as e:
            raise self.forbidden(e)


class GetUsers(routing.Controller):
    """Get users
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('uids', formatters.JSONArray())
        self.args.add_formatter('exclude', formatters.JSONArray())
        self.args.add_formatter('search', formatters.Str())
        self.args.add_formatter('q', formatters.Str())  # Alias for 'search'
        self.args.add_formatter('skip', formatters.PositiveInt())
        self.args.add_formatter('limit', formatters.PositiveInt(10, 100))

    def exec(self) -> list:
        uids = self.arg('uids')
        exclude = self.arg('exclude')
        search = self.arg('search') or self.arg('q')

        r = []

        if uids:
            for uid in self.arg('uids'):
                try:
                    user = auth.get_user(uid=uid)
                    json = user.as_jsonable()
                    events.fire('auth_http_api@get_user', user=user, json=json)
                    r.append(json)

                except Exception as e:
                    # Any exception is ignored due to safety reasons
                    logger.warn(e)
        elif search and reg.get('auth_http_api.search', False):
            q = query.Query()
            q.add(query.Or([
                query.Regex('first_name', '^{}'.format(search), True),
                query.Regex('last_name', '^{}'.format(search), True),
            ]))

            if not auth.get_current_user().is_admin:
                q.add(query.Eq('is_public', True))

            if exclude:
                q.add(query.Nin('uid', exclude))

            for user in auth.find_users(q, limit=self.arg('limit'), skip=self.arg('skip')):
                r.append(user.as_jsonable())

        return r


class GetUser(routing.Controller):
    """Get information about a user
    """

    def exec(self) -> dict:
        try:
            user = auth.get_user(uid=self.arg('uid'))
            jsonable = user.as_jsonable()
            events.fire('auth_http_api@get_user', user=user, json=jsonable)

            return jsonable

        except auth.error.UserNotFound:
            raise self.not_found()


class PatchUser(routing.Controller):
    """Update user
    """

    def __init__(self):
        super().__init__()
        self.args.add_formatter('birth_date', formatters.DateTime())
        self.args.add_formatter('urls', formatters.JSONArray())
        self.args.add_formatter('is_public', formatters.Bool())

        self.args.add_validation('email', validation.rule.Email())
        self.args.add_validation('gender', validation.rule.Enum(values=('m', 'f')))

    def exec(self) -> dict:
        user = auth.get_current_user()

        # Check permissions
        if user.is_anonymous or (user.uid != self.arg('uid') and not user.is_admin):
            raise self.forbidden()

        allowed_fields = ('email', 'nickname', 'picture', 'first_name', 'last_name', 'description', 'birth_date',
                          'gender', 'phone', 'country', 'city', 'urls', 'is_public')

        for k, v in self.args.items():
            if k in allowed_fields:
                user.set_field(k, v)

        if user.is_modified:
            user.save()

        json = user.as_jsonable()

        events.fire('auth_http_api@get_user', user=user, json=json)

        return json


class GetUserFollowsOrFollowers(routing.Controller):
    """Get followed users or followers
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('skip', formatters.PositiveInt())
        self.args.add_formatter('count', formatters.AboveZeroInt(maximum=100))

    def exec(self) -> dict:
        current_user = auth.get_current_user()

        try:
            user = auth.get_user(uid=self.arg('uid'))
        except auth.error.UserNotFound:
            raise self.not_found()

        if user != current_user and not (current_user.is_admin or user.is_public):
            raise self.forbidden()

        skip = self.arg('skip', 0)
        count = self.arg('count', 10)

        if self.arg('_pytsite_http_api_rule_name') == 'auth_http_api@get_user_follows':
            users = [u.as_jsonable() for u in user.get_field('follows', skip=skip, count=count)]
            remains = user.follows_count - (skip + count)
            return {'result': users, 'remains': remains if remains > 0 else 0}
        elif self.arg('_pytsite_http_api_rule_name') == 'auth_http_api@get_user_followers':
            users = [u.as_jsonable() for u in user.get_field('followers', skip=skip, count=count)]
            remains = user.followers_count - (skip + count)
            return {'result': users, 'remains': remains if remains > 0 else 0}
        else:
            raise self.not_found()


class GetMe(routing.Controller):
    """Get information about an access token
    """

    def exec(self) -> dict:
        user = auth.get_current_user()
        if not user.is_anonymous:
            self.args['uid'] = user.uid
            return http_api.call('auth_http_api@get_user', self.args)
        else:
            raise self.forbidden()


class PatchMe(routing.Controller):
    """Patch me
    """

    def exec(self) -> dict:
        user = auth.get_current_user()
        if not user.is_anonymous:
            self.args['uid'] = user.uid
            return http_api.call('auth_http_api@patch_user', self.args)
        else:
            raise self.forbidden()


class GetMeFollows(routing.Controller):
    """Patch me
    """

    def exec(self) -> dict:
        user = auth.get_current_user()
        if not user.is_anonymous:
            self.args['uid'] = user.uid
            return http_api.call('auth_http_api@get_user_follows', self.args)
        else:
            raise self.forbidden()


class GetMeFollowers(routing.Controller):
    """Patch me
    """

    def exec(self) -> dict:
        user = auth.get_current_user()
        if not user.is_anonymous:
            self.args['uid'] = user.uid
            return http_api.call('auth_http_api@get_user_followers', self.args)
        else:
            raise self.forbidden()


class PostMeFollows(routing.Controller):
    """Follow a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to follow
        try:
            user = auth.get_user(uid=self.arg('uid'))
            auth.switch_user_to_system()
            current_user.add_follows(user).save()
        except auth.error.UserNotFound:
            raise self.not_found()
        finally:
            auth.restore_user()

        return {'status': True}


class DeleteMeFollows(routing.Controller):
    """Unfollow a user
    """

    def exec(self) -> dict:
        # Is current user authorized?
        current_user = auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to unfollow
        try:
            user = auth.get_user(uid=self.arg('uid'))
            auth.switch_user_to_system()
            current_user.remove_follows(user).save()
        except auth.error.UserNotFound:
            raise self.not_found()
        finally:
            auth.restore_user()

        return {'status': True}


class GetMeBlockedUsers(routing.Controller):
    """Get blocked users
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('skip', formatters.PositiveInt())
        self.args.add_formatter('count', formatters.AboveZeroInt(maximum=100))

    def exec(self):
        try:
            user = auth.get_user(uid=self.arg('uid'))
        except auth.error.UserNotFound:
            raise self.not_found()

        current_user = auth.get_current_user()

        if current_user.is_anonymous or not (current_user == user or current_user.is_admin):
            raise self.forbidden()

        skip = self.arg('skip', 0)
        count = self.arg('count', 10)
        users = [u.as_jsonable() for u in user.get_field('blocked_users', skip=skip, count=count)]
        remains = user.blocked_users_count - (skip + count)

        return {'result': users, 'remains': remains if remains > 0 else 0}


class PostMeBlockedUsers(routing.Controller):
    """Block a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to block
        try:
            user = auth.get_user(uid=self.arg('uid'))
            auth.switch_user_to_system()
            current_user.add_blocked_user(user).save()
        except auth.error.UserNotFound:
            raise self.not_found()
        finally:
            auth.restore_user()

        return {'status': True}


class DeleteMeBlockedUsers(routing.Controller):
    """Unblock a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to unblock
        try:
            user = auth.get_user(uid=self.arg('uid'))
            auth.switch_user_to_system()
            current_user.remove_blocked_user(user).save()
        except auth.error.UserNotFound:
            raise self.not_found()
        finally:
            auth.restore_user()

        return {'status': True}
