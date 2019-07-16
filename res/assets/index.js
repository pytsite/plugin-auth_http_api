import httpApi from '@pytsite/http-api';

function signIn(data) {
    return httpApi.post('auth/sign-in', data)
}

function signUp(data) {
    return httpApi.post('auth/sign-up', data)
}

function signOut(data) {
    return httpApi.post('auth/sign-out', data)
}

function me() {
    return httpApi.get('auth/me');
}

const api = {
    signIn: signIn,
    signUp: signUp,
    signOut: signOut,
    me: me,
};

export default api;
