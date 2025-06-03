<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- 统计卡片 -->
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="stat in stats" :key="stat.title">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" :style="{background: stat.color}">
              <i :class="stat.icon"></i>
            </div>
            <div class="stat-content">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">{{ stat.value }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard-row">
      <!-- 存储使用情况 -->
      <el-col :xs="24" :md="16">
        <el-card header="存储使用情况">
          <div class="storage-chart">
            <div class="storage-meters">
              <el-progress 
                type="dashboard" 
                :percentage="storagePercentage" 
                :color="storageColor"
                :width="120"
              >
                <template #default>
                  <div class="storage-text">
                    <div class="storage-value">{{ usedStorage }} GB</div>
                    <div class="storage-label">已用 / {{ totalStorage }} GB</div>
                  </div>
                </template>
              </el-progress>
            </div>
            <div class="storage-info">
              <el-table :data="storageData" height="180" style="width: 100%">
                <el-table-column prop="name" label="文件类型" width="120" />
                <el-table-column prop="count" label="数量" width="100" />
                <el-table-column prop="size" label="大小">
                  <template #default="{row}">
                    {{ formatFileSize(row.size) }}
                  </template>
                </el-table-column>
                <el-table-column prop="percentage" label="占比">
                  <template #default="{row}">
                    <el-progress :percentage="row.percentage" :stroke-width="14" :show-text="false" />
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 最近上传 -->
      <el-col :xs="24" :md="8">
        <el-card header="最近上传">
          <el-timeline>
            <el-timeline-item 
              v-for="file in recentFiles" 
              :key="file.name"
              :timestamp="formatTime(file.created)"
              placement="top"
            >
              <div class="recent-file">
                <div class="file-icon">
                  <i :class="getFileIcon(file.name)" />
                </div>
                <div class="file-info">
                  <div class="file-name">{{ file.name }}</div>
                  <div class="file-size">{{ formatFileSize(file.size) }}</div>
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard-row">
      <!-- 上传按钮 -->
      <el-col :span="24">
        <el-card shadow="never" body-style="padding:15px 20px;">
          <div class="upload-quick">
            <el-button type="primary" @click="goToUpload">上传新文件</el-button>
            <div class="quick-tip">支持最大10GB文件上传</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: [
        { title: '文件总数', value: '324', icon: 'el-icon-document', color: '#409EFF' },
        { title: '已用存储', value: '38.2/50 GB', icon: 'el-icon-data-line', color: '#67C23A' },
        { title: '7日上传', value: '18', icon: 'el-icon-upload2', color: '#E6A23C' },
        { title: '用户数', value: '1', icon: 'el-icon-user', color: '#F56C6C' }
      ],
      storageData: [
        { name: '文档', count: 86, size: 12844032, percentage: 15 },
        { name: '图片', count: 132, size: 201543168, percentage: 38 },
        { name: '视频', count: 24, size: 1856329728, percentage: 35 },
        { name: '其他', count: 82, size: 86204416, percentage: 12 }
      ],
      totalStorage: 50, // 总存储空间 (GB)
      usedStorage: 38.2, // 已用存储 (GB)
    }
  },
  computed: {
    ...mapState(['files']),
    recentFiles() {
      return [...this.files]
        .sort((a, b) => b.created - a.created)
        .slice(0, 5)
    },
    storagePercentage() {
      return Math.round((this.usedStorage / this.totalStorage) * 100)
    },
    storageColor() {
      const percentage = this.storagePercentage
      if (percentage < 50) return '#67C23A'
      if (percentage < 80) return '#E6A23C'
      return '#F56C6C'
    }
  },
  mounted() {
    this.fetchFiles()
  },
  methods: {
    ...mapActions(['getFiles']),
    fetchFiles() {
      this.getFiles({
        limit: 5,
        sort: 'created-desc'
      })
    },
    formatTime(timestamp) {
      const date = new Date(timestamp * 1000)
      return `${date.getFullYear()}/${date.getMonth()+1}/${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    getFileIcon(filename) {
      const ext = filename.split('.').pop().toLowerCase()
      const types = {
        pdf: 'el-icon-tickets',
        doc: 'el-icon-document',
        docx: 'el-icon-document',
        txt: 'el-icon-document',
        xls: 'el-icon-document',
        xlsx: 'el-icon-document',
        ppt: 'el-icon-picture-outline',
        pptx: 'el-icon-picture-outline',
        zip: 'el-icon-folder-opened',
        rar: 'el-icon-folder-opened',
        jpg: 'el-icon-picture',
        jpeg: 'el-icon-picture',
        png: 'el-icon-picture',
        gif: 'el-icon-picture',
        mp4: 'el-icon-video-camera',
        mov: 'el-icon-video-camera',
        avi: 'el-icon-video-camera',
        mp3: 'el-icon-headset',
        wav: 'el-icon-headset'
      }
      return types[ext] || 'el-icon-document'
    },
    goToUpload() {
      this.$router.push('/upload')
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-row {
  margin-top: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-icon i {
  font-size: 28px;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-title {
  color: #909399;
  font-size: 14px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-top: 5px;
}

.storage-chart {
  display: flex;
  padding: 10px 0;
}

.storage-meters {
  flex: 0 0 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.storage-text {
  text-align: center;
}

.storage-value {
  font-size: 20px;
  font-weight: bold;
  color: #606266;
}

.storage-label {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.storage-info {
  flex: 1;
  padding: 10px 15px;
}

.recent-file {
  display: flex;
  align-items: center;
  padding: 5px 0;
}

.file-icon {
  font-size: 28px;
  color: #909399;
  margin-right: 10px;
}

.file-info {
  flex: 1;
}

.file-name {
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  font-size: 12px;
  color: #909399;
}

.upload-quick {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-tip {
  font-size: 14px;
  color: #909399;
}

@media (max-width: 768px) {
  .storage-chart {
    flex-direction: column;
  }
  
  .storage-meters {
    margin-bottom: 20px;
  }
}
</style>