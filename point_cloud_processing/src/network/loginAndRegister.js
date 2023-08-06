import { request } from './request.js'

export function getCatpcha(email) {
	return request({
		url: '/getCatpcha',
		method: 'get',
		params:{
			email:email
		}
	})
}
export function register(username, email, captcha, password, repassword) {
	const formData = new FormData()
	formData.append('username', username)
	formData.append('email', email)
	formData.append('captcha', captcha)
	formData.append('password', password)
	formData.append('password_confirm', repassword)

	return request({
		url: '/register',
		method: 'post',
		data: formData
	})
}

export function login(email, password) {
	const formData = new FormData()
	formData.append('email', email)
	formData.append('password', password)
	return request({
		url: '/login',
		method: 'post',
		data: formData
	})
}

export function logout(){
	return request({
		url:'/logout'
	})
}

export function getUsername(){
	return request({
		url:'/getUsername'
	})
}