import { request } from './request.js'

export function startDp() {
    return request({
        url: '/dp/startDp',
        method: 'get',
        timeout:600000
    })
}
