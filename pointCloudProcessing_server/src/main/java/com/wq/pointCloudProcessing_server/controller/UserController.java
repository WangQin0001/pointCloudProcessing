package com.wq.pointCloudProcessing_server.controller;

import com.wq.pointCloudProcessing_server.dto.EmailDto;
import com.wq.pointCloudProcessing_server.dto.RegisterDto;
import com.wq.pointCloudProcessing_server.pojo.User;
import com.wq.pointCloudProcessing_server.service.ServiceImpl.UserServiceImpl;
import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;
import com.wq.pointCloudProcessing_server.util.SendEmailUtils;
import com.wq.pointCloudProcessing_server.util.ValidateCodeUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.util.concurrent.TimeUnit;
import javax.servlet.http.HttpSession;
/**
 * @author 大白菜
 * @date Created in 2022/9/27 9:31
 */
@SuppressWarnings({"all"})
@RestController
@RequestMapping("/api/user")
public class UserController {
    @Autowired
    UserServiceImpl userServiceImpl;
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @PostMapping(value = "/login")
    public Result login(@RequestBody User user, HttpSession session) {
        User authenticatedUser = userServiceImpl.loginService(user.getEmail(), user.getPassword());
        if (authenticatedUser != null) {
            session.setAttribute("username", authenticatedUser.getName());
            return ResultUtil.success("Login success");
        } else {
            return ResultUtil.error("Emil or Password wrong");
        }
    }


    @RequestMapping("/getUsername")
    public Result getUsername(HttpSession session){
        // 从 session 中获取用户名
        String username = (String) session.getAttribute("username");
        // 检查用户名是否存在
        if(username == null || username.isEmpty()){
            return ResultUtil.error(null);
        }
        // 如果用户已登录，则返回用户名
        return ResultUtil.success(username);
    }
    @RequestMapping("/logout")
    public Result logout(HttpSession session){
        // 从 session 中获取用户名
        String username = (String) session.getAttribute("username");
        // 如果没有用户登录，返回错误
        if(username == null || username.isEmpty()){
            return ResultUtil.error("No user is logged in.");
        }
        // 使 session 无效
        session.invalidate();
        // 返回成功消息
        return ResultUtil.success("User has been successfully logged out.");
    }

    @RequestMapping("/getCatpcha")
    public Result getCatpcha(@RequestBody EmailDto emailDto){
        String email = emailDto.getEmail();
        if(email == null){
            return ResultUtil.error("Email is empty");
        }
        System.out.println("email:"+email);
        String catpcha = ValidateCodeUtils.generateValidateCode(4).toString();
        System.out.println("catpcha:"+catpcha);
        //发送邮件
        SendEmailUtils.sendCatpcha(email,catpcha);
        System.out.println("emailDto.getEmail"+emailDto.getEmail());
        //将验证码缓存到Redis(有效时间为1分钟)
        stringRedisTemplate.opsForValue().set("catpcha:"+emailDto.getEmail(),catpcha,1, TimeUnit.MINUTES);
        return ResultUtil.success("Email sent successfully");
    }

    @RequestMapping("/register")
    public Result register(@RequestBody RegisterDto registerDto){
        System.out.println("验证码："+ registerDto.getCaptcha()); // 注意：应该是getCaptcha()，如果你在DTO中定义了相应的getter方法
        System.out.println("用户名："+ registerDto.getUsername()); // 使用getter方法来访问属性
        String validationMsg = validateRegisterInput(registerDto);
        if (validationMsg != null) {
            return ResultUtil.error(validationMsg);
        }
        // 创建User对象实例
        User user = new User();
        user.setName(registerDto.getUsername());
        user.setPassword(registerDto.getPassword());
        user.setEmail(registerDto.getEmail());
        System.out.println(user);
        // 调用注册服务
        String msg = userServiceImpl.registerService(user);
        if ("SUCCESS".equals(msg)) {
            return ResultUtil.success("Register success");
        } else {
            return ResultUtil.error(msg);
        }
    }
    private String validateRegisterInput(RegisterDto registerDto) {
        // 检查密码是否一致
        if (!registerDto.getPassword().equals(registerDto.getRepassword())) {
            return "输入的两次密码不一致";
        }
        // 检查验证码是否正确（此处需要您实现验证码的获取和比较逻辑）
        System.out.println("registerDto.getEmail"+registerDto.getEmail());
        String correctCaptcha = stringRedisTemplate.opsForValue().get("catpcha:" + registerDto.getEmail()); // 从您的存储机制中获取正确的验证码
        System.out.println("correctCaptcha"+correctCaptcha);
        if (correctCaptcha == null || !registerDto.getCaptcha().equals(correctCaptcha)) {
            return "验证码错误";
        }
        return null; // 如果没有错误，返回null
    }
}
