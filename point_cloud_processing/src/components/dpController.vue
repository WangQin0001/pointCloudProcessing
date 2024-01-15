<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <br>
    <el-upload
        class="upload-demo"
        action="http://localhost:8080/api/dp/uploadAndStart"
        :on-change="handleZipFileSelection"
        :before-upload="beforeZipUpload"
        :show-file-list="false"
        :on-success="handleZipFileUploadSuccess"
        accept=".zip">
    <el-button slot="trigger" size="small" type="primary">choose zip file to upload</el-button>
    <div slot="tip" class="el-upload__tip">only can upload ZIP file</div>
    </el-upload>
    <br>
    <!-- 使用 :disabled 属性来控制按钮的可点击状态 -->
    <el-link type="primary" :disabled="disabled1" @click="startDp(folderPath)">{{ message1 }}</el-link>
  </div>
</template>


<script>

import {startDp} from "@/network/dpController";

export default {
  components: {},
  data() {
    return {
      zipFile: null,  // 存储选择的文件
      message1: 'start calculate new point cloud model',
      disabled1: false, // 控制按钮是否可以被点击
      disabled2: false, // 控制按钮是否可以被点击
    }
  },
  methods: {
    // 处理 ZIP 文件的选择
    handleZipFileSelection(file) {
      this.zipFile = file.raw;
    },
    // 在上传之前的钩子函数
    beforeZipUpload(file) {
      // 可以在这里添加上传前的检查逻辑，比如文件大小限制等
      return file.name.slice(-4) === '.zip';
    },
    handleZipFileUploadSuccess(response, file, fileList){
      console.log('Upload Success:', response, file, fileList);
      this.$message.success('file '+file.name+' upload success, under processing!');
    },

    startDp(folderPath = null) {
      if (this.disabled1) return; // 如果按钮被禁用，则不执行任何操作
      this.disabled1 = true; // 禁用按钮
      this.message1 = "Processing... please wait, usually takes 2 minutes"; // 更新显示的消息
      startDp(folderPath).then(res => {
        if (res.code === 200) {
          this.message1 = 'start calculate new point cloud model'; // 如果成功，恢复原始文本
          this.$message.success("Calculate Finished!");
        }
        this.disabled1 = false; // 重新启用按钮
      }).catch(error => {
        this.message = 'Error occurred'; // 如果发生错误，显示错误信息
        this.disabled1 = false; // 重新启用按钮
      });
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
