package com.wq.pointCloudProcessing_server.service.ServiceImpl;

import com.wq.pointCloudProcessing_server.dto.RaspberryPiDto;
import com.wq.pointCloudProcessing_server.service.RaspberryPiService;
import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;
import org.apache.ibatis.jdbc.Null;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Service
public class RaspberryPiServiceImpl implements RaspberryPiService {
    @Override
    public Result controlRaspberryPi(RaspberryPiDto raspberryPiDto){
        try {

            String scriptPath = "F:\\OneDrive\\100_work\\repo\\point_cloud_processing\\raspberryPi\\main.py";
//            String scriptPath = "F:\\OneDrive\\100_work\\repo\\point_cloud_processing\\pythonProjectTest\\main.py";

            // 这里用的是Windows系统的Python路径，注意根据您的实际安装路径进行修改
            String pythonExecutable = "D:\\dev\\anaconda\\envs\\point_cloud_processing\\python.exe";

            List<String> command = new ArrayList<>();
            command.add(pythonExecutable);
            command.add(scriptPath);
            command.add(String.valueOf(raspberryPiDto.getMethodName())); // 总是添加方法名

            if (raspberryPiDto.getStep() != null) command.add(String.valueOf(raspberryPiDto.getStep()));
            if (raspberryPiDto.getDir() != null) command.add(String.valueOf(raspberryPiDto.getDir()));
            if (raspberryPiDto.getAngle() != null) command.add(String.valueOf(raspberryPiDto.getAngle()));

            System.out.println("methodName: "+raspberryPiDto.getMethodName());
            System.out.println("step: "+raspberryPiDto.getStep());
            System.out.println("dir: "+raspberryPiDto.getDir());
            System.out.println("angle: "+ raspberryPiDto.getAngle());
            ProcessBuilder processBuilder = new ProcessBuilder(command);
            processBuilder.redirectErrorStream(true); // 这一步很重要，它确保错误输出也会被捕获

            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8));
            StringBuilder stringBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                stringBuilder.append(line).append("\n");
            }
            System.out.println(stringBuilder);//控制台打印输出python执行信息
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                return ResultUtil.success(stringBuilder.toString());
            } else {
                return ResultUtil.error("Script execution failed with exit code: " + exitCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResultUtil.error("Error occurred while executing Python script: " + e.getMessage());
        }
    }
}
