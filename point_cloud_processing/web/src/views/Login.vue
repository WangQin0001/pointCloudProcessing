<!-- this is login page -->

<template>
  <div>
    <h1>Login</h1>
    <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="demo-ruleForm">
      <el-form-item label="UserName" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="Password" prop="password">
        <el-input type="password" v-model="form.password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Login</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
  
<script>
export default {
  data() {
    return {
      form: {
        name: 'wangqin',
        password: '123'
      },
      rules: {
        name: [
          { required: true, message: 'type in userName', trigger: 'blur' }
        ],
        password: [
          { required: true, message: 'type in password', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$message.success('Login success')
          this.$router.push('/home')
        } else {
          this.$message.error('Login failed')
          return false
        }
      })
    }
  }
}
</script>
  
<style>
.demo-ruleForm {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>