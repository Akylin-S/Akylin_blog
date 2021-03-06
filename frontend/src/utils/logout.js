// frontend/src/utils/authorization.js


async function logout() {
    const storage = localStorage;

    storage.clear();
        let hasLogin = false;

     let username = storage.getItem('username.myblog');
    let isSuperuser = storage.getItem('isSuperuser.myblog');
    return [hasLogin, username,isSuperuser]
}

export default logout;