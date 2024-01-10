package com.wq.pointCloudProcessing_server.service;
import com.wq.pointCloudProcessing_server.util.Result;
import org.springframework.web.multipart.MultipartFile;

public interface DpService {
    Result executeDpScripts(String... args);
    Result handleZipUpload(MultipartFile file);
}
