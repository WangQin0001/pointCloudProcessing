<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <br>
    <input type="file" @change="handleZipFileSelection" accept=".zip">
    <el-button type="primary" @click="uploadZipToServer">上传 ZIP 文件到服务器</el-button>
    <br>
    <br>
    <!-- 使用 :disabled 属性来控制按钮的可点击状态 -->
    <el-link type="primary" :disabled="disabled1" @click="startDp(folderPath)">{{ message1 }}</el-link>
    <br>
    <br>
    <el-link type="primary" :disabled="disabled2" @click="startDenoise">{{ message2 }}</el-link>
    <br>
    <br>
    <el-upload
        ref="upload"
        action="#"
        :auto-upload="false"
        :show-file-list="false"
        :on-change="handleFileChange"
    >
      <el-button size="small" type="primary">选择点云文件</el-button>
    </el-upload>
  </div>
</template>


<script>

import {uploadFiles,startDp,startDenoise} from "@/network/dpController";

export default {
  components: {},
  data() {
    return {
      zipFile: null,  // 存储选择的文件
      message1: 'start calculate new point cloud model',
      message2: 'start denoise point cloud model',
      disabled1: false, // 控制按钮是否可以被点击
      disabled2: false, // 控制按钮是否可以被点击
    }
  },
  methods: {
    // 处理 ZIP 文件的选择
    handleZipFileSelection(event) {
      this.zipFile = event.target.files[0];
    },

    // 上传 ZIP 文件到服务器
    uploadZipToServer() {
      if (!this.zipFile) {
        this.$message.error('请先选择一个 ZIP 文件');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.zipFile);

      uploadFiles(formData).then(res => {
        this.$message.success('ZIP 文件上传成功');
        // 处理响应
      }).catch(error => {
        this.$message.error('ZIP 文件上传失败');
        // 处理错误
      });
    },





    handleFileChange(file) {
      this.$emit('file-selected', file.raw); // 发射事件
      return false; // 这将阻止 el-upload 组件尝试上传文件
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

    startDenoise(){
      if (this.disabled2) return;
      this.disabled2 = true;
      this.message2 = "Processing... please wait, usually takes 10 seconds";
      startDenoise().then(res => {
        if(res.code === 200){
          this.message2 = "start denoise the point cloud model"
          this.$message.success("Denoise Success!");
        }
        this.disabled2 = false;
        res.data = res.data.replace(/\n/g, '<br>')// 将 \n 替换为 HTML 的 <br>
        // 同样，假设响应中包含消息
        this.$notify({
          message: res.data, // 显示从后端接收到的消息
          type: 'success',
          dangerouslyUseHTMLString: true,//允许解析html：换行
          position: 'bottom-left' // 消息出现在左下角
        });
      }).catch(error => {
        this.$message.error('An error occurred: ' + error.message);
        this.disabled2 = false; // 重新启用按钮
      });
    }
  }
}
</script>

<style scoped>
.container{
  margin-left: 10px;
}
</style>
