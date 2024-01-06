package com.wq.pointCloudProcessing_server.controller;

import com.wq.pointCloudProcessing_server.service.DpService;
import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

@RestController
public class DpController {

    @Autowired
    private DpService dpService;

    private static final String FILE_SAVE_PATH = "F:\\OneDrive\\100_work\\pointCloudProcessing_server\\src\\main\\resources\\imgs"; // 替换为您的具体路径

    @PostMapping("/api/upload")
    public Result handleZipUpload(@RequestParam("file") MultipartFile file) {
        try {
            String fileName = file.getOriginalFilename();
            File destinationFile = new File(FILE_SAVE_PATH + File.separator + fileName);
            file.transferTo(destinationFile);

            // 解压 ZIP 文件并获取解压后的文件夹路径
            String extractedFolderPath = unzipFile(destinationFile, FILE_SAVE_PATH);

            // 调用处理 Python 脚本的服务，传递解压后的文件夹路径
            dpService.executeDpScripts(extractedFolderPath);

            return ResultUtil.success("ZIP file uploaded and processed successfully");
        } catch (Exception e) {
            e.printStackTrace();
            return ResultUtil.error("ZIP file upload and process failed: " + e.getMessage());
        }
    }

    private String unzipFile(File zipFile, String outputFolder) throws IOException {
        String fileNameWithoutExtension = zipFile.getName().substring(0, zipFile.getName().lastIndexOf('.'));
        File destDir = new File(outputFolder, fileNameWithoutExtension);

        if (!destDir.exists()) {
            destDir.mkdirs(); // 创建目录
        }

        try (ZipInputStream zis = new ZipInputStream(Files.newInputStream(zipFile.toPath()))) {
            ZipEntry zipEntry = zis.getNextEntry();
            while (zipEntry != null) {
                File newFile = newFile(destDir, zipEntry);
                if (zipEntry.isDirectory()) {
                    newFile.mkdirs();
                } else {
                    new File(newFile.getParent()).mkdirs();
                    Files.copy(zis, newFile.toPath());
                }
                zipEntry = zis.getNextEntry();
            }
            zis.closeEntry();
        }

        return destDir.getAbsolutePath(); // 返回解压文件夹的绝对路径
    }

    private File newFile(File destinationDir, ZipEntry zipEntry) throws IOException {
        File destFile = new File(destinationDir, zipEntry.getName());
        String destDirPath = destinationDir.getCanonicalPath();
        String destFilePath = destFile.getCanonicalPath();
        if (!destFilePath.startsWith(destDirPath + File.separator)) {
            throw new IOException("Entry is outside of the target dir: " + zipEntry.getName());
        }
        return destFile;
    }

    @GetMapping("/api/startDp")
    public Result startDp(@RequestParam(required = false) String[] args) {
        if (args == null) {
            args = new String[] {};  // 确保 args 不是 null，而是一个空数组
        }
        return dpService.executeDpScripts(args);
    }

    @GetMapping("/api/startDenoise")
    public Result startDenoise(@RequestParam(required = false) String[] args){
        return dpService.executeDenoiseScripts(args);
    }
}