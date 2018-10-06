const httpApi = require('@pytsite/http-api');

function me() {
    return httpApi.get('auth/me');
}

export {me};

