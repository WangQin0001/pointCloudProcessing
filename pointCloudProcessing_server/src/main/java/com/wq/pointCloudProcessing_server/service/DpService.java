package com.wq.pointCloudProcessing_server.service;
import com.wq.pointCloudProcessing_server.util.Result;

public interface DpService {
    Result executeDpScripts(String... args);
    Result executeDenoiseScripts(String... args);
}
