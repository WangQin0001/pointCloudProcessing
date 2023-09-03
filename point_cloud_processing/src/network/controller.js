import { request } from './request.js'

export function offsetPosition() {
    return request({
        url: '/offsetPosition',
        method: 'get',
    })
}

export function captureCurrentImage() {
    return request({
        url: '/captureCurrentImage',
        method: 'get',
    })
}

export function captureSurroundingImage() {
    return request({
        url: '/captureSurroundingImage',
        method: 'get',
    })
}

export function manualRotate() {
    return request({
        url: '/manualRotate',
        method: 'get',
    })
}
