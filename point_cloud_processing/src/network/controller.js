import { request } from './request.js'

export function offsetPosition() {
    return request({
        url: '/controlRaspberryPi/go_to_offset_angle',
        method: 'get',
    })
}

export function captureCurrentImage() {
    return request({
        url: '/controlRaspberryPi/capture_single_image',
        method: 'get',
    })
}

export function captureSurroundingImage() {
    return request({
        url: '/controlRaspberryPi/capture_image_full',
        method: 'get',
    })
}

export function manualRotate() {
    return request({
        url: '/controlRaspberryPi/rotate_platform',
        method: 'get',
    })
}
