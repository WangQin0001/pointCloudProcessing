package com.wq.pointCloudProcessing_server.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class RegisterDto {

    public String username;
    public String email;
    public String password;
    public String repassword;
    public String captcha;

    public RegisterDto(String username, String email, String password,String repassword,String captcha) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.repassword = repassword;
        this.captcha = captcha;
    }
}
