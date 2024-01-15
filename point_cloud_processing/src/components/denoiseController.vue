<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <br>
    <br>
    <el-upload
        class="upload-demo"
        action="http://localhost:8080/api/denoise/upload"
        multiple
        :limit="3"
        :on-exceed="handleExceed"
        :before-upload="beforeFileUpload"
        :on-success="handleUploadSuccess">
      <el-button size="small" type="primary">Click to upload the file for denoising</el-button>
      <div slot="tip" class="el-upload__tip">Only PCD files can be uploaded, the size cannot exceed 50MB</div>
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
    beforeFileUpload(file) {
      const isPCD = file.name.endsWith('.pcd');
      const isLt50M = file.size / 1024 / 1024 < 50; // 修改文件大小限制为 50MB
      if (!isPCD) {
        this.$message.error('You can only upload PCD file!');
        return false;
      }
      if (!isLt50M) {
        this.$message.error('File size cannot exceed 50MB!');
        return false;
      }
      return true;
    },
    handleExceed(files, fileList) {
      this.$message.warning(`You can only upload up to 3 files.`);
    },
    handleUploadSuccess(response, file, fileList) {
      this.$message.success('Upload PCD file successful!');
      this.clearFileList();
    },
    clearFileList() {
      if (this.$refs.upload) {
        this.$refs.upload.clearFiles();
      }
    },
  }
}
</script>

<style scoped>
.container{
  max-width: 400px;
  margin-left: 10px;
}
.upload-demo {
  max-width: 400px; /* 或者您希望的任何宽度 */
  margin-left: 0px;/* 使组件在容器中居中 */
}
</style>
