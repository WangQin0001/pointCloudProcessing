import axios from 'axios'

export function request(config) {
    const instance = axios.create({
        baseURL: '/api',
        timeOut: 5000
    })
    //因为instance(config)的返回值本身就是一个promise,所以不再需要promise封装
    return instance(config)
}
