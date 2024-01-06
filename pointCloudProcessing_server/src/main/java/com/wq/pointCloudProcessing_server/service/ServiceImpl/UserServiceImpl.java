package com.wq.pointCloudProcessing_server.service.ServiceImpl;

import com.wq.pointCloudProcessing_server.mapper.UserMapper;
import com.wq.pointCloudProcessing_server.pojo.User;
import com.wq.pointCloudProcessing_server.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


/**
 * @author 大白菜
 * @date Created in 2022/9/27 9:31
 */
@Service
public class UserServiceImpl implements UserService {
    @Autowired//注解，自动注入mapper中实例化的对象，没有这个注解userMapper为空
    UserMapper userMapper;

    @Override
    public User loginService(String email, String password) {
        User user = userMapper.searchByemail(email);
        if (user != null) {
            if (password.equals(user.getPassword())) {
                return user;
            } else {
                return null;
            }
        }
        return null;
    }

    @Override
    public String registerService(User user) {
        User userE = userMapper.searchByemail(user.getEmail());
        if (userE == null) {
            if ("".equals(user.getPassword())) {
                return "Please enter password";
            } else if ("".equals(user.getName())) {
                return "Please enter username";
            } else {
                userMapper.insert(user);
                return "SUCCESS";
            }
        }
        return "User already exists";
    }
}
