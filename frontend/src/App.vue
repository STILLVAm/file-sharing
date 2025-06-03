<template>
  <div id="app">
    <el-container class="layout-container">
      <!-- 头部导航 -->
      <el-header height="60px">
        <div class="header-container">
          <div class="logo">文件云存储</div>
          <el-menu 
            :default-active="activeMenu" 
            mode="horizontal" 
            :router="true"
          >
            <el-menu-item index="/">仪表盘</el-menu-item>
            <el-menu-item index="/upload">上传文件</el-menu-item>
            <el-menu-item index="/files">文件管理</el-menu-item>
          </el-menu>
          <div class="user-actions">
            <span v-if="currentUser" class="username">{{ currentUser.username }}</span>
            <el-button 
              v-if="isAuthenticated" 
              type="text" 
              @click="logout"
            >退出</el-button>
            <el-button 
              v-else 
              type="primary" 
              @click="goToLogin"
            >登录</el-button>
          </div>
        </div>
      </el-header>
      
      <!-- 主内容区 -->
      <el-main>
        <router-view />
      </el-main>
      
      <!-- 底部信息 -->
      <el-footer height="50px">
        <div class="footer-content">
          &copy; {{ new Date().getFullYear() }} 个人文件云存储系统
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isAuthenticated', 'currentUser']),
    activeMenu() {
      return this.$route.path
    }
  },
  methods: {
    ...mapActions(['logout']),
    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-container {
  height: 100%;
}

.el-header {
  background-color: #2c3e50;
  color: white;
  line-height: 60px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  padding: 0 20px;
}

.el-menu {
  border-bottom: none;
}

.el-menu--horizontal {
  background-color: transparent;
  height: 60px;
}

.el-menu--horizontal > .el-menu-item {
  color: #fff;
  height: 60px;
  line-height: 60px;
}

.el-menu--horizontal > .el-menu-item.is-active {
  border-bottom: 2px solid #409EFF;
  color: #409EFF;
}

.el-menu--horizontal > .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-actions {
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.username {
  margin-right: 15px;
  color: #c5cbd3;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.el-footer {
  background-color: #e9eef3;
  color: #606266;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

@media (max-width: 768px) {
  .header-container {
    flex-wrap: wrap;
  }
  .el-menu {
    order: 3;
    width: 100%;
    justify-content: space-around;
  }
  .logo {
    margin-right: auto;
  }
}
</style>