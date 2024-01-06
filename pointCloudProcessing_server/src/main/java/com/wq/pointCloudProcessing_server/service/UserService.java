package com.wq.pointCloudProcessing_server.service;

import com.wq.pointCloudProcessing_server.pojo.User;

/**
 * @author 大白菜
 * @date Created in 2022/9/27 9:31
 */
public interface UserService {

    public User loginService(String email, String password);

    public String registerService(User user);
}
