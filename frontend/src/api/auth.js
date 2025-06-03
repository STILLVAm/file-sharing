import axios from 'axios'
import store from '../store'

const API_BASE = process.env.VUE_APP_API_BASE_URL || '/api'

const instance = axios.create({
  baseURL: API_BASE,
  headers: {
    'X-API-Key': process.env.VUE_APP_API_KEY
  }
})

// 设置认证头部
instance.interceptors.request.use(config => {
  const token = store.state.token
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

export const login = async (credentials) => {
  try {
    const response = await instance.post('/login', credentials)
    return response.data
  } catch (error) {
    throw error.response?.data?.error || '登录失败'
  }
}