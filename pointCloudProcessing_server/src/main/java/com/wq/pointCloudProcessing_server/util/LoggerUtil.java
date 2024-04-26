package com.wq.pointCloudProcessing_server.util;

import java.io.IOException;
import java.io.File;

import java.util.HashMap;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;
import java.util.logging.Level;

public class LoggerUtil {
    private static final HashMap<String, Logger> loggers = new HashMap<>();

    public static Logger getLogger(String className, String logFileName) {
        Logger logger = loggers.get(className);
        if (logger == null) {
            try {
                // 确保 logs 文件夹存在
                new File("logs").mkdirs();  // 尝试创建 logs 文件夹（如果不存在）

                // 使用相对路径的示例
                String logFilePath = "logs/" + logFileName;  // "./logs/" 也可以

                // 这将只创建一个日志文件，文件大小上限设为非常大
                FileHandler fileHandler = new FileHandler(logFilePath, Integer.MAX_VALUE, 1, true);

                fileHandler.setFormatter(new SimpleFormatter());
                logger = Logger.getLogger(className);
                logger.addHandler(fileHandler);
                logger.setLevel(Level.INFO);
                logger.setUseParentHandlers(false); // 不输出到控制台
                loggers.put(className, logger);
            } catch (IOException e) {
                System.err.println("Failed to setup logger for class " + className + ": " + e.getMessage());
            }
        }
        return logger;
    }
}
