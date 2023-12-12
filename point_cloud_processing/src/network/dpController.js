import { request } from './request.js'

export function startDp() {
    return request({
        url: '/startDp',
        method: 'get',
    })
}
