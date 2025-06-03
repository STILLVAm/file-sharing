import instance from './auth'

export const getFiles = async (options = {}) => {
  try {
    const params = {
      limit: options.limit || 100,
      offset: options.offset || 0,
      sort: options.sort || 'created-desc'
    }
    const response = await instance.get('/files', { params })
    return response.data
  } catch (error) {
    throw error.response?.data?.error || '获取文件列表失败'
  }
}

export const deleteFile = async (filename) => {
  try {
    const response = await instance.delete(`/files/${encodeURIComponent(filename)}`)
    return response.data
  } catch (error) {
    throw error.response?.data?.error || '删除文件失败'
  }
}