
package com.wq.pointCloudProcessing_server.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import com.wq.pointCloudProcessing_server.service.ServiceImpl.DenoiseServiceImpl;
import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;

@RestController
@RequestMapping("/api/denoise")
public class DenoiseController {

    @Autowired
    DenoiseServiceImpl denoiseService;

    @PostMapping("/upload")
    public Result upload(@RequestParam("file") MultipartFile file) {
        try {
            denoiseService.upload(file);
            return ResultUtil.success("File uploaded and processed successfully: " + file.getOriginalFilename());
        } catch (Exception e) {
            return ResultUtil.error("Failed to upload and process file: " + file.getOriginalFilename() + "; Error: " + e.getMessage());
        }
    }
}
