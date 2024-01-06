package com.wq.pointCloudProcessing_server.service.ServiceImpl;


import org.springframework.stereotype.Service;
import com.wq.pointCloudProcessing_server.service.DpService;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;
import java.io.File;
import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;


@Service
public class DpServiceImpl implements DpService {
    private static final String SCRIPT_ROOT = "F:\\OneDrive\\100_work\\repo\\point_cloud_processing\\3D-Model-Monocular-Vision-main";
    private static final String PYTHON_EXECUTABLE = "D:\\dev\\anaconda\\envs\\point_cloud_processing\\python.exe";

    @Override
    public Result executeDpScripts(String... args) {
        StringBuilder result = new StringBuilder();
        System.out.println("Start to run DP");
        try {
            List<String> scripts = new ArrayList<>();
            scripts.add("match_images.py");
            scripts.add("sanity_panorama.py");
            scripts.add("search_point_in_panorama.py");
            scripts.add("solve_param_each_part.py");
            scripts.add("match_difference.py");
            scripts.add("calib_pcd_panorama.py");

            String folderPath = args.length > 0 ? args[0] : null;

            for (int i = 0; i < scripts.size(); i++) {
                String script = scripts.get(i);
                List<String> commandWithArgs = new ArrayList<>();
                commandWithArgs.add(PYTHON_EXECUTABLE);
                commandWithArgs.add(SCRIPT_ROOT + "\\" + script);

                // 仅对第一个脚本添加文件夹路径（如果提供了）
                if (i == 0 && folderPath != null) {
                    commandWithArgs.add("-i");  // 输入参数标志
                    commandWithArgs.add(folderPath);  // 文件夹路径
                    // 可能还需要添加其他与路径相关的参数
                }

                ProcessBuilder processBuilder = new ProcessBuilder(commandWithArgs);
                processBuilder.directory(new File(SCRIPT_ROOT));
                processBuilder.redirectErrorStream(true);

                Process process = processBuilder.start();

                // 读取和处理输出
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    result.append(line).append("\n");
                }

                int exitVal = process.waitFor();
                if (exitVal != 0) {
                    throw new RuntimeException("Abnormal script execution for script: " + script + ". Error: " + result.toString());
                }
            }
            return ResultUtil.success(result.toString());
        } catch (Exception e) {
            e.printStackTrace();
            return ResultUtil.error("Error executing script: " + e.getMessage() + ". Output: " + result.toString());
        }
    }


    @Override
    public Result executeDenoiseScripts(String... args){
        StringBuilder result = new StringBuilder();
        System.out.println("start to denoise");
        try {
            // 添加 denoise.py 脚本
            List<String> commandWithArgs = new ArrayList<>();
            commandWithArgs.add(PYTHON_EXECUTABLE); // 使用 Python 的完整路径
            commandWithArgs.add(SCRIPT_ROOT + "\\denoise.py"); // 添加脚本路径
            if (args != null) {
                commandWithArgs.addAll(Arrays.asList(args)); // 添加参数
            }

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

