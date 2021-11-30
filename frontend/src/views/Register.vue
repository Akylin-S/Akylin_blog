<template>
  <BlogHeader />

    <div id="signup">
      <h3>注册账号</h3>
      <form>
        <div class="form-elem">
          <span>账号：</span>
          <input v-model="Register_Name" type="text" placeholder="输入用户名" />
        </div>
        <div class="form-elem">
          <span>密码：</span>
          <input v-model="Register_Pwd" type="password" placeholder="输入密码" />
        </div>
        <div class="form-elem-confirm">
          <span>确认密码：</span>
          <input v-model="Register_Pwd_confirm" type="password" placeholder="输入密码" />
        </div>
        <div class="form-elem">
          <router-link   to="/login" class="login-link">已有账号，去登录</router-link>
          <button class="form-register" v-on:click.prevent="Register_up">提交</button>
        </div>
      </form>
    </div>
  <BlogFooter />
</template>

<script>
import axios from "axios";
import BlogHeader from "@/components/BlogHeader.vue";
import BlogFooter from "@/components/BlogFooter.vue";

export default {
  name: "Register",
  components: { BlogHeader, BlogFooter },
  data: function () {
    return {
      Register_Name: "",
      Register_Pwd: "",
      Register_Response: null,
    };
  },
  methods: {
    Register_up() {
      const that = this;
      if (this.Register_Pwd != this.Register_Pwd_confirm)
      {
        alert("两次输入的密码不相同，请确认");
        return
      }
      axios

        .post("/api/user/", {
          username: this.Register_Name,
          password: this.Register_Pwd,
        })
        .then(function (response) {
          // 路由跳转修改到这里
          that.$router.push({ name: "Home" });
          that.Register_Response = response.data;
          alert("用户注册成功，快去登录吧！");
        })
        .catch(
            function (error) {
              console.log(error)
              alert('用户名已被注册：');
          // Handling Error here...
          // https://github.com/axios/axios#handling-errors
        });
    },
  },
};
</script>

<style scoped>

#signup {
  text-align: center;
}
.form-elem {
  padding: 10px;
}
.form-elem-confirm {
  padding: 10px 40px 10px 10px;
}
input {
  height: 25px;
  padding-left: 10px;
}

.form-register {
 margin-left:50px;
}

button {
  height: 35px;
  cursor: pointer;
  border: none;
  outline: none;
  background: gray;
  color: whitesmoke;
  border-radius: 5px;
  width: 60px;
}

.login-link {
  color: black;
}
</style>