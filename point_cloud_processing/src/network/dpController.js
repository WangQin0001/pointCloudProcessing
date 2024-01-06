import { request } from './request.js'

export function uploadFiles(formData) {
    return request({
        url: '/upload',  // 替换为您的文件上传服务器端点
        method: 'post',
        data: formData,  // 包含文件数据的 FormData 对象
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}
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