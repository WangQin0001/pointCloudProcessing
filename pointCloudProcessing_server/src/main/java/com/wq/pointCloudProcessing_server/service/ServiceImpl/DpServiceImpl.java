package com.wq.pointCloudProcessing_server.service.ServiceImpl;


import org.springframework.stereotype.Service;
import com.wq.pointCloudProcessing_server.service.DpService;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.io.File;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;
import org.springframework.web.multipart.MultipartFile;


@Service
public class DpServiceImpl implements DpService {

    private static final String SCRIPT_ROOT = "F:\\OneDrive\\100_work\\repo\\point_cloud_processing\\3D-Model-Monocular-Vision-main";
    private static final String PYTHON_EXECUTABLE = "D:\\dev\\anaconda\\envs\\point_cloud_processing\\python.exe";

    @Override
    public Result executeDpScripts(String... args) {
        StringBuilder result = new StringBuilder();
        System.out.println("Start to run DP scripts");

        List<String> scripts = new ArrayList<>();
        scripts.add("match_images.py");
        // 注释掉其他脚本以便逐个测试
         scripts.add("sanity_panorama.py");
         scripts.add("search_point_in_panorama.py");
         scripts.add("solve_param_each_part.py");
         scripts.add("match_difference.py");
         scripts.add("calib_pcd_panorama.py");

        String fileName = args.length > 0 ? args[0] : null;

        for (String script : scripts) {
            try {
                List<String> commandWithArgs = new ArrayList<>();
                commandWithArgs.add(PYTHON_EXECUTABLE);
                commandWithArgs.add(new File(SCRIPT_ROOT, script).getAbsolutePath());
                if (fileName != null) {
                    commandWithArgs.add("-i");  // 输入参数标志
                    commandWithArgs.add(UNZIP_PATH);  // 文件夹路径
                    System.out.println("传给 Python 的路径：" + UNZIP_PATH+fileName);
                    commandWithArgs.add("-f");
                    commandWithArgs.add(fileName);
                }
                // 打印构建的命令行
                System.out.println("Executing script with command: " + commandWithArgs);
                ProcessBuilder processBuilder = new ProcessBuilder(commandWithArgs);
                processBuilder.directory(new File(SCRIPT_ROOT));
                processBuilder.redirectErrorStream(false); // 将错误流和输出流分开
                Process process = processBuilder.start();
                // 读取标准输出
                BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                while ((line = stdInput.readLine()) != null) {
                    System.out.println("Stdout: " + line);
                    result.append(line).append("\n");
                }
                // 读取标准错误
                BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                while ((line = stdError.readLine()) != null) {
                    System.out.println("Stderr: " + line);
                }
                // 检查进程的退出值
                int exitVal = process.waitFor();
                if (exitVal != 0) {
                    // 如果有错误，您可能希望在这里打印出错误信息
                    throw new RuntimeException("Abnormal script execution for script: " + script);
                }
            } catch (Exception e) {
                e.printStackTrace();
                return ResultUtil.error("Error executing script: " + script + ". " + e.getMessage());
            }
        }
        return ResultUtil.success(result.toString());
    }



    private static final String UNZIP_PATH = "F:\\OneDrive\\100_work\\repo\\point_cloud_processing\\server_files\\UNZIPFilesToDp";
    @Override
    public Result handleZipUpload(MultipartFile file) {
        try {
            // 确保解压路径存在
            Files.createDirectories(Paths.get(UNZIP_PATH));

            String fileName = file.getOriginalFilename();
            if (fileName == null || !fileName.toLowerCase().endsWith(".zip")) {
                return ResultUtil.error("Invalid file type. Only ZIP files are accepted.");
            }
            // 使用 REPLACE_EXISTING 选项来覆盖已存在的文件


            File destinationFile = new File(UNZIP_PATH, fileName);
            file.transferTo(destinationFile);

            // 解压 ZIP 文件并获取解压后的文件夹路径
            String extractedFolderPath = unzipFile(destinationFile, UNZIP_PATH);
            executeDpScripts(extractedFolderPath);
            return ResultUtil.success("ZIP file uploaded and processed successfully");
        } catch (Exception e) {
            e.printStackTrace();
            return ResultUtil.error("ZIP file upload and process failed: " + e.getMessage());
        }
    }

    private String unzipFile(File zipFile, String outputFolder) throws IOException {
        String fileNameWithoutExtension = zipFile.getName().substring(0, zipFile.getName().lastIndexOf('.'));
        File destDir = new File(outputFolder, fileNameWithoutExtension);

        if (!destDir.exists() && !destDir.mkdirs()) {
            throw new IOException("Could not create directory for unzipping.");
        }
        try (ZipInputStream zis = new ZipInputStream(Files.newInputStream(zipFile.toPath()))) {
            ZipEntry zipEntry = zis.getNextEntry();
            while (zipEntry != null) {
                File newFile = new File(destDir, zipEntry.getName());
                if (zipEntry.isDirectory()) {
                    if (!newFile.isDirectory() && !newFile.mkdirs()) {
                        throw new IOException("Could not create directory within ZIP structure.");
                    }
                } else {
                    // Create parent directories if they don't exist
                    File parentDir = newFile.getParentFile();
                    if (!parentDir.exists() && !parentDir.mkdirs()) {
                        throw new IOException("Could not create parent directory for file within ZIP structure.");
                    }
                    // Copy the file, replacing any existing file
                    Files.copy(zis, newFile.toPath(), StandardCopyOption.REPLACE_EXISTING);
                }
                zipEntry = zis.getNextEntry();
            }
            zis.closeEntry();
        }

        return destDir.getAbsolutePath(); // Return the absolute path of the unzipped folder
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

}

