package com.wq.pointCloudProcessing_server.service.ServiceImpl;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.wq.pointCloudProcessing_server.service.TempMonitorService;
import org.springframework.stereotype.Service;
import java.io.InputStream;
import java.util.Properties;

@Service
public class TempMonitorServiceImpl implements TempMonitorService {
    private String host = "192.168.1.81";
    private String username = "root";
    private String password = "root";
    private static final int SSH_PORT = 22;//大多数SSH应用的默认端口号是22
    private static final String TEMPERATURE_COMMAND = "cat /sys/class/thermal/thermal_zone0/temp";
    @Override
    public String getCpuTemperature() {
        try {
            double temperature = executeRemoteCommand(TEMPERATURE_COMMAND) / 1000.0;
            return String.format("%.2f", temperature);
        } catch (Exception e) {
            throw new RuntimeException("Failed to fetch temperature from Raspberry Pi", e);
        }
    }

    private int executeRemoteCommand(String command) throws Exception {
        JSch jsch = new JSch();
        Session session = jsch.getSession(username, host, SSH_PORT);
        session.setPassword(password);

        // Avoid asking for key confirmation
        Properties prop = new Properties();
        prop.put("StrictHostKeyChecking", "no");
        session.setConfig(prop);

        session.connect();

        ChannelExec channel = (ChannelExec) session.openChannel("exec");
        channel.setCommand(command);
        channel.setInputStream(null);
        InputStream in = channel.getInputStream();
        channel.connect();

        // Fetch the output from input stream
        int temperature = 0;
        byte[] tmp = new byte[1024];
        while (true) {
            while (in.available() > 0) {
                int i = in.read(tmp, 0, 1024);
                if (i < 0) break;
                temperature = Integer.parseInt(new String(tmp, 0, i).trim());
            }
            if (channel.isClosed()) {
                if (in.available() > 0) continue;
                break;
            }
            try {
                Thread.sleep(1000);
            } catch (Exception ee) {
                Thread.currentThread().interrupt();
            }
        }
        channel.disconnect();
        session.disconnect();
        return temperature;
    }
}
