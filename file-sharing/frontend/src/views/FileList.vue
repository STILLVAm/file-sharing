<template>
  <div class="container">
    <h2>文件列表</h2>
    
    <div v-if="loading">
      <p>加载中...</p>
    </div>
    
    <div v-else>
      <div v-if="files.length === 0">
        <p>没有找到文件</p>
      </div>
      
      <div v-else>
        <table>
          <thead>
            <tr>
              <th>文件名</th>
              <th>大小</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="file in files" :key="file.name">
              <td>{{ file.name }}</td>
              <td>{{ formatFileSize(file.size) }}</td>
              <td>
                <button class="btn" @click="downloadFile(file)">下载</button>
                <button class="btn btn-danger" @click="deleteFile(file)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      files: [],
      loading: true
    };
  },
  mounted() {
    this.fetchFiles();
  },
  methods: {
    async fetchFiles() {
      try {
        const response = await fetch("http://localhost:5000/api/files");
        const data = await response.json();
        this.files = data;
      } catch (error) {
        console.error("获取文件列表失败:", error);
      } finally {
        this.loading = false;
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },
    downloadFile(file) {
      window.location.href = file.url;
    },
    async deleteFile(file) {
      if (confirm(`确定要永久删除 ${file.name} 吗？此操作不可撤销。`)) {
        try {
          const response = await fetch(`/api/files/${encodeURIComponent(file.name)}`, {
            method: "DELETE"
          });
          
          if (response.ok) {
            this.files = this.files.filter(f => f.name !== file.name);
            this.$notify({
              title: '成功',
              message: '文件已永久删除',
              type: 'success'
            });
          } else {
            const errorData = await response.json();
            throw new Error(errorData.error || '删除失败');
          }
        } catch (error) {
          console.error("删除文件失败:", error);
          this.$notify({
            title: '错误',
            message: '删除文件失败: ' + error.message,
            type: 'error'
          });
        }
      }
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

tr:hover {
  background-color: #f5f5f5;
}

th {
  background-color: #42b983;
  color: white;
}

.btn {
  margin-right: 5px;
}
</style>