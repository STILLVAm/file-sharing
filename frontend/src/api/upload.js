import instance from './auth'

export const initUpload = async (fileData) => {
  try {
    const response = await instance.post('/upload/init', fileData)
    return response.data
  } catch (error) {
    throw error.response?.data?.error || '上传初始化失败'
  }
}

export const uploadChunk = async (chunkData) => {
  try {
    const response = await instance.post('/upload/chunk', chunkData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error) {
    throw error.response?.data?.error || '分片上传失败'
  }
}

export const completeUpload = async (uploadData) => {
  try {
    const response = await instance.post('/upload/complete', uploadData)
    return response.data
  } catch (error) {
    throw error.response?.data?.error || '文件合并失败'
  }
}