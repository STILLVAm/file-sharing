<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">文件管理系统</h2>
      
      <el-form ref="loginForm" :model="form" :rules="rules" @submit.prevent="login">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" show-password>
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" class="login-btn">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

export default {
  components: {
    User,
    Lock
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const form = ref({
      username: '',
      password: ''
    })
    
    const rules = ref({
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    })
    
    const loading = ref(false)
    
    const login = async () => {
      try {
        loading.value = true
        
        // 调用登录API
        const response = await store.dispatch('auth/login', form.value)
        
        if (response.success) {
          ElMessage.success('登录成功')
          router.push('/dashboard')
        } else {
          ElMessage.error(response.error || '登录失败')
        }
      } catch (error) {
        ElMessage.error('登录过程中发生错误')
        console.error('Login error:', error)
      } finally {
        loading.value = false
      }
    }
    
    return { form, rules, loading, login }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1e5799, #207cca);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-card {
  width: 380px;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
  background: rgba(255, 255, 255, 0.95);
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.login-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
  margin-top: 15px;
  letter-spacing: 2px;
}
</style>