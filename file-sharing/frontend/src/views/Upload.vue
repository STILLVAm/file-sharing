<template>
  <div class="container">
    <h2>上传文件</h2>
    <input type="file" @change="handleFileChange">
    <button class="btn" @click="uploadFile" :disabled="!selectedFile">上传</button>
    
    <div v-if="uploadStatus">
      <p :class="{'success': uploadSuccess, 'error': !uploadSuccess}">
        {{ uploadMessage }}
      </p>
    </div>
    
    <div class="instructions">
      <h3>支持的文件类型：</h3>
      <p>文档 (.txt, .pdf, .doc, .docx), 图片 (.png, .jpg, .jpeg, .gif)</p>
      <p>最大文件大小：50MB</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      uploadStatus: false,
      uploadSuccess: false,
      uploadMessage: ""
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) return;
      
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      
      try {
        const response = await fetch("http://localhost:5000/api/upload", {
          method: "POST",
          body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
          this.uploadSuccess = true;
          this.uploadMessage = `文件上传成功: ${data.filename}`;
          this.$emit('file-uploaded');
        } else {
          this.uploadSuccess = false;
          this.uploadMessage = `上传失败: ${data.error}`;
        }
      } catch (error) {
        this.uploadSuccess = false;
        this.uploadMessage = "网络错误: " + error.message;
      }
      
      this.uploadStatus = true;
      this.selectedFile = null;
      setTimeout(() => {
        this.uploadStatus = false;
      }, 5000);
    }
  }
};
</script>

<style scoped>
input[type="file"] {
  margin: 20px 0;
  display: block;
}

.success {
  color: #42b983;
  margin-top: 15px;
}

.error {
  color: #ff4757;
  margin-top: 15px;
}

.instructions {
  margin-top: 30px;
  color: #666;
}
</style>