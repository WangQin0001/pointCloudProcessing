<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <el-upload
        ref="upload"
        action="#"
        :auto-upload="false"
        :show-file-list="false"
        :on-change="handleFileChange"
    >
      <el-button size="small" type="primary">Select new PCD model for rendering</el-button>
    </el-upload>
  </div>
</template>
<script>

export default {
  components: {},
  data() {
    return {

    }
  },
  methods: {
    handleFileChange(file) {
      this.$emit('file-selected', file.raw); // 发射事件
      return false; // 这将阻止 el-upload 组件尝试上传文件
    },
  }
}
</script>

<style scoped>
.container{
  margin-left: 10px;
  max-width: 400px;
}
</style>
