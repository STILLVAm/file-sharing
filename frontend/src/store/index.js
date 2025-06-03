import { createStore } from 'vuex'
import { login } from '@/api/auth'
import { getFiles, deleteFile } from '@/api/files'
import { initUpload, uploadChunk, completeUpload } from '@/api/upload'

export default createStore({
  state: {
    token: localStorage.getItem('authToken') || null,
    user: null,
    files: [],
    loading: false
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      localStorage.setItem('authToken', token)
    },
    clearToken(state) {
      state.token = null
      localStorage.removeItem('authToken')
    },
    setUser(state, user) {
      state.user = user
    },
    setFiles(state, files) {
      state.files = files
    },
    setLoading(state, loading) {
      state.loading = loading
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        commit('setLoading', true)
        
        // 调用登录API
        const response = await login(credentials)
        
        if (response.success) {
          commit('setToken', response.token)
          commit('setUser', { username: credentials.username })
          return response
        }
        
        throw new Error('登录失败')
      } catch (error) {
        throw new Error(error.message || '登录过程中发生错误')
      } finally {
        commit('setLoading', false)
      }
    },
    async logout({ commit }) {
      commit('clearToken')
      commit('setUser', null)
    },
    async getFiles({ commit }, options = {}) {
      try {
        commit('setLoading', true)
        const files = await getFiles(options)
        commit('setFiles', files)
        return files
      } catch (error) {
        throw new Error('获取文件列表失败: ' + error.message)
      } finally {
        commit('setLoading', false)
      }
    },
    async deleteFile({ dispatch }, filename) {
      try {
        await deleteFile(filename)
        await dispatch('getFiles') // 刷新文件列表
        return true
      } catch (error) {
        throw new Error('删除文件失败: ' + error.message)
      }
    },
    async uploadInit({ commit }, fileData) {
      try {
        commit('setLoading', true)
        const response = await initUpload(fileData)
        return response
      } catch (error) {
        throw new Error('上传初始化失败: ' + error.message)
      } finally {
        commit('setLoading', false)
      }
    },
    async uploadChunk({ commit }, chunkData) {
      try {
        commit('setLoading', true)
        const response = await uploadChunk(chunkData)
        return response
      } catch (error) {
        throw new Error('分片上传失败: ' + error.message)
      } finally {
        commit('setLoading', false)
      }
    },
    async uploadComplete({ commit }, uploadData) {
      try {
        commit('setLoading', true)
        const response = await completeUpload(uploadData)
        return response
      } catch (error) {
        throw new Error('文件合并失败: ' + error.message)
      } finally {
        commit('setLoading', false)
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user,
    fileList: state => state.files,
    isLoading: state => state.loading
  }
})