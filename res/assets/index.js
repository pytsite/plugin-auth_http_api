import httpApi from '@pytsite/http-api';

function me() {
    return httpApi.get('auth/me');
}

const api = {
    me: me,
};

export default api;
