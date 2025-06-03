<template>
  <div class="upload-container">
    <el-card class="upload-card">
      <h2>文件上传</h2>
      <p class="upload-tip">最大支持10GB文件上传</p>
      
      <BigFileUploader @upload-success="handleUploadSuccess" />
      
      <div class="upload-history">
        <h3>最近上传</h3>
        <el-table :data="recentFiles" v-loading="loading">
          <el-table-column prop="name" label="文件名" />
          <el-table-column prop="size" label="大小">
            <template #default="{row}">
              {{ formatFileSize(row.size) }}
            </template>
          </el-table-column>
          <el-table-column prop="created" label="上传时间">
            <template #default="{row}">
              {{ new Date(row.created * 1000).toLocaleString() }}
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="{row}">
              <el-button type="text" @click="downloadFile(row)">下载</el-button>
              <el-button type="text" @click="deleteFile(row)" style="color:#f56c6c">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import BigFileUploader from '@/components/BigFileUploader.vue'

export default {
  components: { BigFileUploader },
  setup() {
    const store = useStore()
    const recentFiles = ref([])
    const loading = ref(false)
    
    // 获取最近上传的文件
    const fetchRecentFiles = async () => {
      loading.value = true
      try {
        const files = await store.dispatch('files/getFiles', { limit: 5 })
        recentFiles.value = files
      } catch (error) {
        ElMessage.error('获取文件列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 处理上传成功事件
    const handleUploadSuccess = () => {
      fetchRecentFiles()
      ElMessage.success('文件上传成功!')
    }
    
    // 下载文件
    const downloadFile = (file) => {
      window.open(`/api/download/${encodeURIComponent(file.name)}`, '_blank')
    }
    
    // 删除文件
    const deleteFile = (file) => {
      ElMessageBox.confirm(`确定删除文件 "${file.name}" 吗?`, '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await store.dispatch('files/deleteFile', file.name)
          ElMessage.success('文件已删除')
          fetchRecentFiles()
        } catch (error) {
          ElMessage.error('删除文件失败')
        }
      }).catch(() => {})
    }
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    onMounted(fetchRecentFiles)
    
    return {
      recentFiles,
      loading,
      handleUploadSuccess,
      downloadFile,
      deleteFile,
      formatFileSize
    }
  }
}
</script>

<style scoped>
.upload-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.upload-card {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.upload-tip {
  color: #606266;
  margin-bottom: 25px;
}

.upload-history {
  margin-top: 40px;
}

.el-table {
  margin-top: 15px;
}
</style>