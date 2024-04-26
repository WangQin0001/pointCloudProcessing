package com.wq.pointCloudProcessing_server.controller;

import com.wq.pointCloudProcessing_server.service.AutoService;
import com.wq.pointCloudProcessing_server.util.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.atomic.AtomicInteger;

@RestController
@RequestMapping("/api")
public class AutoController {

    private final AutoService autoService;
    private static final AtomicInteger progress = new AtomicInteger(0);

    @Autowired
    public AutoController(AutoService autoService) {
        this.autoService = autoService;
    }

    @GetMapping("/autoStart")
    public Result auto() {
        resetProgress();
        return autoService.autoControl();
    }

    @GetMapping("/progress")
    public int getProgress() {
        return progress.get();
    }
//    后端以及能够得到轮询更新进度的值，能输出value，可是现在前端无法获取
    public static void updateProgress(int value) {
        progress.set(value);
        System.out.println("renew progress："+value);
    }

    public static void resetProgress() {
        progress.set(0);
    }
}
