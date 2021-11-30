// frontend/src/utils/authorization.js

import axios from 'axios';

async function authorization() {
    const storage = localStorage;

    let hasLogin = false;
    let username = storage.getItem('username.myblog');
    let isSuperuser = storage.getItem('isSuperuser.myblog');
    if (isSuperuser === 'true')
            isSuperuser=true
    else
            isSuperuser=false

    const expiredTime = Number(storage.getItem('expiredTime.myblog'));
    const current = (new Date()).getTime();
    const refreshToken = storage.getItem('refresh.myblog');
    // 初始 token 未过期
    if (expiredTime > current) {
        hasLogin = true;
        console.log('authorization access')
    }
    // 初始 token 过期
    // 申请刷新 token
    else if (refreshToken !== null) {
        try {
            let response = await axios.post('/api/token/refresh/', { refresh: refreshToken });
            hasLogin = true;

            const nextExpiredTime = Date.parse(response.headers.date) + 360000;

            storage.setItem('access.myblog', response.data.access);
            storage.setItem('expiredTime.myblog', nextExpiredTime);
            storage.removeItem('refresh.myblog');


            console.log('authorization refresh')
        }
        catch (err) {
            storage.clear();
            hasLogin = false;

            console.log('authorization err')
        }
    }
    // 无任何有效 token
    else {
        storage.clear();
        hasLogin = false;
        console.log('authorization exp')
    }

    return [hasLogin, username,isSuperuser]
}

export default authorization;