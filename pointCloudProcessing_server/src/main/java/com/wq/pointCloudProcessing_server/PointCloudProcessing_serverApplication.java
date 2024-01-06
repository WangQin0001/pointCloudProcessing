package com.wq.pointCloudProcessing_server;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {"com.wq.pointCloudProcessing_server.controller"})
@ComponentScan(basePackages = {"com.wq.pointCloudProcessing_server.service"})
@MapperScan("com.wq.pointCloudProcessing_server.mapper")//扫描mapper包
public class PointCloudProcessing_serverApplication {

    public static void main(String[] args) {
        SpringApplication.run(PointCloudProcessing_serverApplication.class, args);
    }

}
