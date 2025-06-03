<template>
  <div class="big-uploader">
    <el-upload
      class="upload-area"
      drag
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleFileSelect"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击选择文件</em></div>
      <div class="el-upload__tip">支持最大10GB文件上传</div>
    </el-upload>
    
    <div v-if="selectedFile" class="file-info">
      <div class="file-name">{{ selectedFile.name }}</div>
      <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
      
      <div v-if="progress === 0" class="upload-action">
        <el-button type="primary" @click="startUpload">开始上传</el-button>
        <el-button @click="cancelUpload">取消</el-button>
      </div>
      
      <div v-else-if="progress < 100" class="upload-progress">
        <el-progress 
          :percentage="progress" 
          :status="uploadStatus"
          :stroke-width="18"
          striped
          striped-flow
        />
        <el-button @click="pauseUpload" :disabled="isPaused">
          {{ isPaused ? '已暂停' : '暂停上传' }}
        </el-button>
        <el-button @click="cancelUpload">取消</el-button>
      </div>
      
      <div v-else class="upload-complete">
        <el-result icon="success" title="上传成功">
          <template #extra>
            <el-button type="primary" @click="resetUpload">上传新文件</el-button>
          </template>
        </el-result>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadChunk } from '@/api/upload'

const CHUNK_SIZE = 100 * 1024 * 1024; // 100MB分片

export default {
  setup() {
    const selectedFile = ref(null)
    const progress = ref(0)
    const uploadStatus = ref('')
    const isPaused = ref(false)
    const fileId = ref('')
    const totalChunks = ref(0)
    const uploadedChunks = ref(0)
    const controller = ref(null)

    const handleFileSelect = (file) => {
      if (file.size > 10 * 1024 * 1024 * 1024) {
        ElMessage.error('文件大小不能超过10GB')
        return
      }
      
      resetUpload()
      selectedFile.value = file.raw
    }
    
    const startUpload = async () => {
      try {
        // 初始化上传
        const response = await uploadChunk('init', {
          filename: selectedFile.value.name,
          size: selectedFile.value.size
        })
        
        fileId.value = response.file_id
        totalChunks.value = response.chunks
        uploadedChunks.value = 0
        controller.value = new AbortController()
        
        // 开始上传分片
        uploadStatus.value = ''
        isPaused.value = false
        await uploadChunks()
        
      } catch (error) {
        ElMessage.error('上传初始化失败: ' + error.message)
        resetUpload()
      }
    }
    
    const uploadChunks = async () => {
      for (let i = uploadedChunks.value; i < totalChunks.value; i++) {
        if (isPaused.value) return;
        
        const start = i * CHUNK_SIZE;
        const end = Math.min((i + 1) * CHUNK_SIZE, selectedFile.value.size);
        const chunk = selectedFile.value.slice(start, end);
        
        const formData = new FormData();
        formData.append('file_id', fileId.value);
        formData.append('chunk_index', i);
        formData.append('chunk', chunk, `${selectedFile.value.name}.part${i}`);
        
        try {
          await uploadChunk('chunk', formData, controller.value);
          uploadedChunks.value++;
          progress.value = Math.round((uploadedChunks.value / totalChunks.value) * 100);
        } catch (error) {
          uploadStatus.value = 'exception';
          ElMessage.error(`分片${i}上传失败: ${error.message}`);
          return;
        }
      }
      
      // 所有分片上传完成，合并文件
      try {
        await uploadChunk('complete', {
          file_id: fileId.value,
          filename: selectedFile.value.name
        });
        uploadStatus.value = 'success';
        progress.value = 100;
        ElMessage.success('文件上传成功');
      } catch (error) {
        uploadStatus.value = 'exception';
        ElMessage.error('文件合并失败: ' + error.message);
      }
    }
    
    const pauseUpload = () => {
      isPaused.value = !isPaused.value
      if (!isPaused.value) {
        uploadChunks()
      }
    }
    
    const cancelUpload = () => {
      if (controller.value) {
        controller.value.abort()
      }
      resetUpload()
    }
    
    const resetUpload = () => {
      selectedFile.value = null
      progress.value = 0
      uploadStatus.value = ''
      isPaused.value = false
      fileId.value = ''
      controller.value = null
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadChunk } from '@/api/upload'

const CHUNK_SIZE = 100 * 1024 * 1024; // 100MB分片

export default {
  setup() {
    const selectedFile = ref(null)
    const progress = ref(0)
    const uploadStatus = ref('')
    const isPaused = ref(false)
    const fileId = ref('')
    const totalChunks = ref(0)
    const uploadedChunks = ref(0)
    const controller = ref(null)

    const handleFileSelect = (file) => {
      if (file.size > 10 * 1024 * 1024 * 1024) {
        ElMessage.error('文件大小不能超过10GB')
        return
      }
      
      resetUpload()
      selectedFile.value = file.raw
    }
    
    const startUpload = async () => {
      try {
        // 初始化上传
        const response = await uploadChunk('init', {
          filename: selectedFile.value.name,
          size: selectedFile.value.size
        })
        
        fileId.value = response.file_id
        totalChunks.value = response.chunks
        uploadedChunks.value = 0
        controller.value = new AbortController()
        
        // 开始上传分片
        uploadStatus.value = ''
        isPaused.value = false
        await uploadChunks()
        
      } catch (error) {
        ElMessage.error('上传初始化失败: ' + error.message)
        resetUpload()
      }
    }
    
    const uploadChunks = async () => {
      for (let i = uploadedChunks.value; i < totalChunks.value; i++) {
        if (isPaused.value) return;
        
        const start = i * CHUNK_SIZE;
        const end = Math.min((i + 1) * CHUNK_SIZE, selectedFile.value.size);
        const chunk = selectedFile.value.slice(start, end);
        
        const formData = new FormData();
        formData.append('file_id', fileId.value);
        formData.append('chunk_index', i);
        formData.append('chunk', chunk, `${selectedFile.value.name}.part${i}`);
        
        try {
          await uploadChunk('chunk', formData, controller.value);
          uploadedChunks.value++;
          progress.value = Math.round((uploadedChunks.value / totalChunks.value) * 100);
        } catch (error) {
          uploadStatus.value = 'exception';
          ElMessage.error(`分片${i}上传失败: ${error.message}`);
          return;
        }
      }
      
      // 所有分片上传完成，合并文件
      try {
        await uploadChunk('complete', {
          file_id: fileId.value,
          filename: selectedFile.value.name
        });
        uploadStatus.value = 'success';
        progress.value = 100;
        ElMessage.success('文件上传成功');
      } catch (error) {
        uploadStatus.value = 'exception';
        ElMessage.error('文件合并失败: ' + error.message);
      }
    }
    
    const pauseUpload = () => {
      isPaused.value = !isPaused.value
      if (!isPaused.value) {
        uploadChunks()
      }
    }
    
    const cancelUpload = () => {
      if (controller.value) {
        controller.value.abort()
      }
      resetUpload()
    }
    
    const resetUpload = () => {
      selectedFile.value = null
      progress.value = 0
      uploadStatus.value = ''
      isPaused.value = false
      fileId.value = ''
      controller.value = null
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    return {
      selectedFile,
      progress,
      uploadStatus,
      isPaused,
      handleFileSelect,
      startUpload,
      pauseUpload,
      cancelUpload,
      formatFileSize
    }
  }
}
</script>

<style scoped>
.big-uploader {
  margin: 20px auto;
  max-width: 800px;
}

.upload-area {
  margin: 20px 0;
  padding: 40px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  text-align: center;
  background: #fafafa;
  transition: all 0.3s;
}

.upload-area:hover {
  border-color: #409eff;
}

.file-info {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fff;
}

.file-name {
  font-weight: bold;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  color: #909399;
  margin-top: 5px;
}

.upload-action, .upload-progress {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.upload-progress {
  flex-direction: column;
  align-items: stretch;
}
</style>