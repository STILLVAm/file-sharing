<template>
  <div class="file-list-container">
    <el-card>
      <div class="header-actions">
        <div class="search-filter">
          <el-input
            v-model="searchQuery"
            placeholder="搜索文件名"
            prefix-icon="el-icon-search"
            clearable
            @clear="searchFiles"
            @keyup.enter="searchFiles"
          />
          <el-select v-model="sortOption" placeholder="排序方式" @change="sortFiles">
            <el-option label="按名称 (A-Z)" value="name-asc"></el-option>
            <el-option label="按名称 (Z-A)" value="name-desc"></el-option>
            <el-option label="按大小 (小-大)" value="size-asc"></el-option>
            <el-option label="按大小 (大-小)" value="size-desc"></el-option>
            <el-option label="按日期 (新-旧)" value="created-desc"></el-option>
            <el-option label="按日期 (旧-新)" value="created-asc"></el-option>
          </el-select>
          <el-select v-model="filterOption" placeholder="文件类型" multiple collapse-tags @change="filterFiles">
            <el-option
              v-for="type in fileTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            ></el-option>
          </el-select>
        </div>
        <el-button type="primary" @click="refreshFiles">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>

      <el-table 
        v-loading="loading"
        :data="filteredFiles"
        border
        style="width: 100%"
        empty-text="没有文件数据"
      >
        <el-table-column label="文件名" min-width="200">
          <template #default="{row}">
            <div class="file-cell">
              <i :class="getFileIcon(row.name)" class="file-icon"></i>
              <div class="file-name">
                {{ row.name }}
                <div class="file-info">
                  <el-tag size="mini" effect="plain">{{ getFileType(row.name) }}</el-tag>
                  <el-tag size="mini" type="info">{{ formatFileSize(row.size) }}</el-tag>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="created" label="上传时间" width="180">
          <template #default="{row}">
            {{ formatTime(row.created) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template #default="{row}">
            <el-button 
              type="text" 
              icon="el-icon-download"
              @click="downloadFile(row)"
            >下载</el-button>
            <el-button 
              type="text" 
              icon="el-icon-delete" 
              style="color:#f56c6c"
              @click="deleteFile(row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          background
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredTotal"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data() {
    return {
      searchQuery: '',
      sortOption: 'created-desc',
      filterOption: [],
      pagination: {
        currentPage: 1,
        pageSize: 20
      },
      fileTypes: [
        { value: 'image', label: '图片' },
        { value: 'video', label: '视频' },
        { value: 'document', label: '文档' },
        { value: 'audio', label: '音频' },
        { value: 'archive', label: '压缩文件' },
        { value: 'other', label: '其他' }
      ]
    }
  },
  computed: {
    ...mapGetters(['fileList', 'isLoading']),
    loading() {
      return this.isLoading
    },
    filteredFiles() {
      let files = [...this.fileList]
      
      // 应用搜索
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        files = files.filter(file => 
          file.name.toLowerCase().includes(query)
        )
      }
      
      // 应用过滤
      if (this.filterOption.length > 0) {
        files = files.filter(file => {
          const type = this.getFileType(file.name)
          return this.filterOption.includes(type)
        })
      }
      
      // 应用分页
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      return files.slice(start, start + this.pagination.pageSize)
    },
    filteredTotal() {
      return this.fileList.length
    }
  },
  mounted() {
    this.fetchFiles()
  },
  methods: {
    ...mapActions(['getFiles', 'deleteFile']),
    fetchFiles(params = {}) {
      const options = {
        ...params,
        limit: this.pagination.pageSize,
        offset: (this.pagination.currentPage - 1) * this.pagination.pageSize,
        sort: this.sortOption
      }
      this.getFiles(options)
    },
    refreshFiles() {
      this.fetchFiles()
    },
    searchFiles() {
      this.pagination.currentPage = 1
      this.fetchFiles()
    },
    filterFiles() {
      this.pagination.currentPage = 1
      this.fetchFiles()
    },
    sortFiles() {
      this.fetchFiles()
    },
    handleSizeChange(size) {
      this.pagination.pageSize = size
      this.fetchFiles()
    },
    handleCurrentChange(page) {
      this.pagination.currentPage = page
      this.fetchFiles()
    },
    downloadFile(file) {
      window.open(`/api/download/${encodeURIComponent(file.name)}`, '_blank')
    },
    deleteFile(file) {
      this.$confirm(`确定删除文件 "${file.name}" 吗?`, '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.deleteFile(file.name)
        this.$message.success('文件已删除')
      }).catch(() => {})
    },
    formatTime(timestamp) {
      const date = new Date(timestamp * 1000)
      return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
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
      const icons = {
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
        '7z': 'el-icon-folder-opened',
        jpg: 'el-icon-picture',
        jpeg: 'el-icon-picture',
        png: 'el-icon-picture',
        gif: 'el-icon-picture',
        bmp: 'el-icon-picture',
        svg: 'el-icon-picture',
        mp4: 'el-icon-video-camera',
        mov: 'el-icon-video-camera',
        avi: 'el-icon-video-camera',
        mkv: 'el-icon-video-camera',
        wmv: 'el-icon-video-camera',
        flv: 'el-icon-video-camera',
        mp3: 'el-icon-headset',
        wav: 'el-icon-headset',
        ogg: 'el-icon-headset',
        flac: 'el-icon-headset'
      }
      return icons[ext] || 'el-icon-document'
    },
    getFileType(filename) {
      const ext = filename.split('.').pop().toLowerCase()
      const types = {
        // 图片
        jpg: 'image', jpeg: 'image', png: 'image', gif: 'image', bmp: 'image', svg: 'image', webp: 'image',
        // 文档
        pdf: 'document', doc: 'document', docx: 'document', txt: 'document', 
        rtf: 'document', xls: 'document', xlsx: 'document', ppt: 'document', pptx: 'document',
        // 视频
        mp4: 'video', mov: 'video', avi: 'video', mkv: 'video', wmv: 'video', flv: 'video',
        // 音频
        mp3: 'audio', wav: 'audio', ogg: 'audio', flac: 'audio',
        // 压缩文件
        zip: 'archive', rar: 'archive', '7z': 'archive', tar: 'archive', gz: 'archive'
      }
      return types[ext] || 'other'
    }
  }
}
</script>

<style scoped>
.file-list-container {
  max-width: 1200px;
  margin: 0 auto;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-filter {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.el-select {
  width: 150px;
}

.el-table {
  margin-top: 15px;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.file-cell {
  display: flex;
  align-items: center;
}

.file-icon {
  font-size: 24px;
  margin-right: 10px;
  color: #606266;
}

.file-name {
  font-weight: normal;
}

.file-info {
  margin-top: 5px;
}

.file-info .el-tag {
  margin-right: 5px;
}

@media (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .search-filter {
    flex-wrap: wrap;
  }
  
  .el-select {
    width: 100%;
  }
}
</style>