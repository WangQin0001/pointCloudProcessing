package com.wq.pointCloudProcessing_server.service;

import com.wq.pointCloudProcessing_server.util.Result;
import org.springframework.web.multipart.MultipartFile;


public interface DenoiseService {
    Result upload(MultipartFile file);
    Result executeDenoiseScripts(String filePath);
}
