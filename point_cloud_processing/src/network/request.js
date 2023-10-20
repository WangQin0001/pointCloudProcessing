import axios from 'axios'

export function request(config) {
    // 创建axios实例
    const instance = axios.create({
        baseURL: 'http://localhost:8080/api', // 你的基础URL
        timeout: 20000 // 注意这里是timeout不是timeOut
    })

    // 请求拦截器
    instance.interceptors.request.use(config => {
        // 在发送请求之前做些什么（如果需要的话，比如添加token到headers）
        return config
    }, error => {
        // 对请求错误做些什么
        return Promise.reject(error)
    })

    // 响应拦截器
    instance.interceptors.response.use(response => {
        // 对响应数据做点什么
        return response.data
    }, error => {
        // 对响应错误做点什么
        return Promise.reject(error)
    })

    // 发送网络请求
    return instance(config)
}
