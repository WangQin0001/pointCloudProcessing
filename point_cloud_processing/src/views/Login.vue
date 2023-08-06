<template>
  <div class="login" clearfix>
    <top></top>
    <div class="login-wrap">
      <el-row type="flex" justify="center">
        <el-form ref="loginFormRef" :model="user" :rules="rules" status-icon label-width="80px" @submit.prevent>
          <h3>Login Page</h3>
          <hr>
          <el-form-item prop="email" label="email">
            <el-input v-model="user.email" placeholder="Please enter email" prefix-icon></el-input>
          </el-form-item>
          <el-form-item id="password" prop="password" label="passsword">
            <el-input v-model="user.password" show-password placeholder="Please enter password"></el-input>
          </el-form-item>
          <br>
          <el-form-item>
            <el-button type="primary" icon="el-icon-upload" @click="doLogin" @keyup.enter="doLogin">Login</el-button>
            <router-link to="/register" style="margin-left: 50px;">Register</router-link>
          </el-form-item>
        </el-form>
      </el-row>
    </div>
  </div>
</template>
 
<script>
import {login} from '../network/loginAndRegister.js'
import top from './Top.vue'
export default {
  name: "login",
  components:{
    top
  },
  data() {
    return {
      user: {
        email: "",
        password: ""
      },
      rules: {
        //定义验证用户名的规则
        email: [{
          required: true,
          message: 'Email is required! ',
          trigger: 'blur'
        },
          {
            type: 'email',
            message: 'check your email type',
            trigger: ['blur', 'change']
          },
        ],
        //定义验证密码的规则
        password: [{
          required: true,
          message: 'Password is required',
          trigger: 'blur'
        },
          {
            min: 6,
            max: 20,
            message: 'between 6 and 20 characters',
            trigger: 'blur'
          },
        ],
      },
    };
  },
  created() { },
  methods: {
    doLogin() {
      this.$refs.loginFormRef.validate(valid => {
        if (!valid) {
          this.$message.error("Input is invalid, please check!")
        } else {
          login(this.user.email, this.user.password).then(res => {
            this.$message.success("login sucess!")
            this.$router.push('/home')
            console.log(res)
          }).catch(error => {
            console.log(error)
          })
        }
      })
      this.$nextTick(() => {
        this.$refs.button.focus()
      })
    }
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login {
  width: 100%;
  height: 740px;
  /* background: url("../assets/images/bg1.png") no-repeat; */
  background-size: cover;
  overflow: hidden;
}

.login-wrap {
  /* background: url("../assets/images/login_bg.png") no-repeat; */
  background-size: cover;
  width: 400px;
  height: 300px;
  margin: 215px auto;
  overflow: hidden;
  padding-top: 10px;
  line-height: 40px;
}

#password {
  margin-bottom: 5px;
}

h3 {
  color: #0babeab8;
  font-size: 24px;
}

hr {
  background-color: #444;
  margin: 20px auto;
}

a {
  text-decoration: none;
  color: #aaa;
  font-size: 15px;
}

a:hover {
  color: coral;
}

.el-button {
  width: 80%;
  margin-left: -50px;
}
</style>