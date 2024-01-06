package com.wq.pointCloudProcessing_server.service;

import com.wq.pointCloudProcessing_server.dto.RaspberryPiDto;
import com.wq.pointCloudProcessing_server.util.Result;

public interface RaspberryPiService {
    public Result controlRaspberryPi(RaspberryPiDto raspberryPiDto);
//    public Result controlRaspberryPi2(RaspberryPiDto raspberryPiDto);

}
