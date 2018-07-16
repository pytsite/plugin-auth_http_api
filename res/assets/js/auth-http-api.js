define(['http-api'], function (httpApi) {
    function me() {
        return httpApi.get('auth/me');
    }

    return {
        me: me
    }
});
