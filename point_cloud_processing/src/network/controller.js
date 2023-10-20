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
