package com.wq.pointCloudProcessing_server.service.ServiceImpl;

import com.wq.pointCloudProcessing_server.service.DenoiseService;
import com.wq.pointCloudProcessing_server.util.Result;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;

import com.wq.pointCloudProcessing_server.util.ResultUtil;

import javax.annotation.PostConstruct;

@Service
public class DenoiseServiceImpl implements DenoiseService {

    private final Path rootLocation = Paths.get("F:\\repo\\point_cloud_processing\\server_files\\FilesToBeDenoised");
    private static final String SCRIPT_ROOT = "F:\\repo\\point_cloud_processing\\3D-Model-Monocular-Vision-main";
    private static final String PYTHON_EXECUTABLE = "D:\\dev\\anaconda\\envs\\point_cloud_processing\\python.exe";

    @PostConstruct
    public void init() {
        try {
            if (!Files.exists(rootLocation)) {
                Files.createDirectories(rootLocation);
            }
        } catch (IOException e) {
            throw new RuntimeException("Could not initialize storage!", e);
        }
    }

    @Override
    public Result upload(MultipartFile file) {
        System.out.println("denoise upload成功");
        try {
            if (file.isEmpty()) {
                throw new RuntimeException("Failed to process empty file " + file.getOriginalFilename());
            }
            Path destinationFile = this.rootLocation.resolve(Paths.get(file.getOriginalFilename()))
                    .normalize().toAbsolutePath();
            if (!destinationFile.getParent().equals(this.rootLocation.toAbsolutePath())) {
                throw new RuntimeException("Cannot store file outside current directory.");
            }
            // 使用 REPLACE_EXISTING 选项来覆盖已存在的文件
            Files.copy(file.getInputStream(), destinationFile, StandardCopyOption.REPLACE_EXISTING);

            // 调用降噪处理脚本，传入文件路径
            return executeDenoiseScripts(destinationFile.toString());
        } catch (IOException e) {
            e.printStackTrace();
            return ResultUtil.error("Failed to process file " + file.getOriginalFilename() + "; Error: " + e.getMessage());
        } catch (RuntimeException e) {
            e.printStackTrace();
            return ResultUtil.error(e.getMessage());
        }
    }


    @Override
    public Result executeDenoiseScripts(String filePath) {
        StringBuilder result = new StringBuilder();
        System.out.println("start to denoise");
        try {
            List<String> commandWithArgs = new ArrayList<>();
            commandWithArgs.add(PYTHON_EXECUTABLE); // 使用 Python 的完整路径
            commandWithArgs.add(SCRIPT_ROOT + "\\denoise.py"); // 添加脚本路径
            commandWithArgs.add(filePath); // 添加文件路径参数

            ProcessBuilder processBuilder = new ProcessBuilder(commandWithArgs);
            processBuilder.directory(new File(SCRIPT_ROOT)); // 设置工作目录

            processBuilder.redirectErrorStream(true); // 重定向错误输出到标准输出流

            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                result.append(line).append("\n");
            }
            int exitVal = process.waitFor();
            if (exitVal != 0) {
                throw new RuntimeException("Abnormal script execution for denoise.py. Error: " + result.toString());
            }
            return ResultUtil.success(result.toString());
        } catch (Exception e) {
            e.printStackTrace();
            return ResultUtil.error("Error executing denoise.py: " + e.getMessage() + ". Output: " + result.toString());
        }
    }
}
