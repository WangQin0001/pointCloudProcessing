import { request } from './request.js'

export function getCatpcha(email) {
	return request({
		url: '/user/getCatpcha',
		method: 'post',
		data:{    // 使用 'data' 而不是 'params'，这是发送POST请求的请求体
			email:email
		}
	})
}

export function register(username, email, captcha, password, repassword) {
	return request({
		url: '/user/register',
		method: 'post',
		data: {
			username:username,
			email:email,
			captcha:captcha,
			password:password,
			repassword:repassword
		}
	})
}

export function login(email, password) {
	return request({
		url: '/user/login',
		method: 'post',
		data: {
			email:email,
			password:password
		}
	})
}

export function logout(){
	return request({
		url:'/user/logout'
	})
}

export function getUsername(){
	return request({
		url:'/user/getUsername'
	})
}