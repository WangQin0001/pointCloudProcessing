package com.wq.pointCloudProcessing_server.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.wq.pointCloudProcessing_server.pojo.User;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Repository
@Mapper
public interface UserMapper extends BaseMapper<User> {
    //mybatisplus的BaseMapper中已经提供了CRUD，不用再像mybatis一样自己去写
    User searchByemail(String email);
}
