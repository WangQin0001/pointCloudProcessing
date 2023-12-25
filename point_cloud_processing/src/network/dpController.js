import { request } from './request.js'

export function startDp() {
    return request({
        url: '/startDp',
        method: 'get',
        timeout:600000
    })
}
export function startDenoise() {
    return request({
        url: '/startDenoise',
        method: 'get',
        timeout:60000
    })
}