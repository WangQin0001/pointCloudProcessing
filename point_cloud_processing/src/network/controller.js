import { request } from './request.js'

export function offsetPosition() {
    return request({
        url: '/controlRaspberryPi',
        method: 'post',
        data:{
            methodName:1,
        }
    })
}

export function captureCurrentImage() {
    return request({
        url: '/controlRaspberryPi',
        method: 'post',
        data:{
            methodName:2,
        }
    })
}

export function captureSurroundingImage(methodName,step,dir,angle) {
    return request({
        url: '/controlRaspberryPi',
        method: 'post',
        data:{
            methodName:methodName,
            step:step,
            dir:dir,
            angle:angle,
        }
    })
}

export function manualRotate(methodName,step,dir,angle) {
    return request({
        url: '/controlRaspberryPi',
        method: 'post',
        data:{
            methodName:methodName,
            step:step,
            dir:dir,
            angle:angle,
        }
    })
}

export function auto() {
    return request({
        url: '/autoStart',
        method: 'get',
    })
}

export function tempMonitor() {
    return request({
        url: '/tempMonitor',
        method: 'get',
    })
}

// Function to fetch the current progress
export function fetchProgress() {
    return request({
        url:'/progress',
        method:'get'
    })
}