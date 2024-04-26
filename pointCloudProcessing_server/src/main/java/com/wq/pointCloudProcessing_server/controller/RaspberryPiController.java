
package com.wq.pointCloudProcessing_server.controller;

import com.wq.pointCloudProcessing_server.dto.RaspberryPiDto;
import com.wq.pointCloudProcessing_server.service.RaspberryPiService;
import com.wq.pointCloudProcessing_server.util.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.context.annotation.RequestScope;

@RestController
public class RaspberryPiController {

    private final RaspberryPiService raspberryPiService;

    @Autowired
    public RaspberryPiController(RaspberryPiService raspberryPiService) {
        this.raspberryPiService = raspberryPiService;
    }

    @RequestMapping("/api/controlRaspberryPi")
    public Result controlRaspberryPi(@RequestBody RaspberryPiDto raspberryPiDto){
        return raspberryPiService.controlRaspberryPi(raspberryPiDto);
    }
}
