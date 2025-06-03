import jwtDecode from 'jwt-decode'

// 从token中解析用户信息
export const getUserFromToken = (token) => {
  if (!token) return null
  try {
    const decoded = jwtDecode(token)
    return decoded.sub
  } catch (e) {
    return null
  }
}

// 检查token是否有效
export const isTokenValid = (token) => {
  if (!token) return false
  try {
    const decoded = jwtDecode(token)
    const now = Date.now() / 1000
    return decoded.exp > now
  } catch (e) {
    return false
  }
}

// 设置token
export const setToken = (token) => {
  localStorage.setItem('authToken', token)
}

// 获取token
export const getToken = () => {
  return localStorage.getItem('authToken')
}

// 清除token
export const clearToken = () => {
  localStorage.removeItem('authToken')
}