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
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

@RestController
@RequestMapping("/api/dp")
public class DpController {

    @Autowired
    private DpService dpService;
    @Autowired
    public DpController(DpService dpService) {
        this.dpService = dpService;
    }

    @PostMapping("uploadAndStart")
    public Result handleZipUpload(@RequestParam("file") MultipartFile file) {
        return dpService.handleZipUpload(file);
    }
    @GetMapping("/startDp")
    public Result startDp(@RequestParam(required = false) String[] args) {
        if (args == null) {
            args = new String[] {};  // 确保 args 不是 null，而是一个空数组
        }
        return dpService.executeDpScripts(args);
    }
}