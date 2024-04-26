package com.wq.pointCloudProcessing_server.controller;

import com.wq.pointCloudProcessing_server.service.TempMonitorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class TempMonitorController {

    @Autowired
    private TempMonitorService tempMonitorService;
    @GetMapping("/tempMonitor")
    public ResponseEntity<?> getTemperature() {
        try {
            String temperature = tempMonitorService.getCpuTemperature();
            return ResponseEntity.ok(temperature);
        } catch (RuntimeException e) {
            // 捕捉到服务层抛出的异常，并返回内部服务器错误状态
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }
//    @GetMapping("/tempMonitor")
//    public double getTemperature() {
//        try {
//            double temperature = 15.0;
//            return temperature;
//        } catch (RuntimeException e) {
//            // 捕捉到服务层抛出的异常，并返回内部服务器错误状态
//            return 1.0;
//        }
//    }
}
//我用vue作为前端springboot作为后端，vue发送请求给后端，然后后端将请求转发给python程序，python程序再依次调用摄像头获取照片、然后将照片传给pytorch进行深度学习计算出点云模型，然后再计算好的点云模型进行降噪后呈现在vue前端上，我现在需要在前端做一个进度条来监控整个项目的进度，该怎么办？
