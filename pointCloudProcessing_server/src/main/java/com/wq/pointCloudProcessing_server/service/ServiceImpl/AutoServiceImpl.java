package com.wq.pointCloudProcessing_server.service.ServiceImpl;

import com.wq.pointCloudProcessing_server.controller.AutoController;
import com.wq.pointCloudProcessing_server.service.AutoService;
import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class AutoServiceImpl implements AutoService {
    @Override
    public Result autoControl() {
        try {
            String scriptPath = "F:\\repo\\point_cloud_processing\\raspberryPi\\auto.py";
            String pythonExecutable = "D:\\dev\\anaconda\\envs\\point_cloud_processing\\python.exe";

            List<String> command = new ArrayList<>();
            command.add(pythonExecutable);
            command.add(scriptPath);

            ProcessBuilder processBuilder = new ProcessBuilder(command);
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8));

            StringBuilder output = new StringBuilder();
            String line;
            final int totalSteps = 8; // 正确地设置总步骤数
            Pattern stepPattern = Pattern.compile("STEP (\\d+) STARTED");

            AutoController.resetProgress();  // 任务开始前重置进度

            while ((line = reader.readLine()) != null) {
                System.out.println(line);
                output.append(line).append("\n");
                Matcher matcher = stepPattern.matcher(line);
                if (matcher.find()) {
                    int stepCompleted = Integer.parseInt(matcher.group(1));
                    AutoController.updateProgress((int) ((stepCompleted / (float) totalSteps) * 100));
                }
            }

            int exitCode = process.waitFor();
            AutoController.updateProgress(100); // 确保在结束时进度为100%

            if (exitCode == 0) {
                return ResultUtil.success(output.toString());
            } else {
                return ResultUtil.error("Script execution failed with exit code: " + exitCode);
            }
        } catch (Exception e) {
            AutoController.resetProgress(); // 出现异常时重置进度
            e.printStackTrace();
            return ResultUtil.error("Error occurred while executing Python script: " + e.getMessage());
        }
    }
}
