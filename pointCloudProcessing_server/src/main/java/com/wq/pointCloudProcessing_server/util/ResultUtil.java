package com.wq.pointCloudProcessing_server.util;

/**
 * @author wangqin
 * @date Created in 2022/9/27 9:34
 */
public class ResultUtil {
    /**
     * 成功且带数据
     **/
    public static Result success(Object object) {
        Result result = new Result();
        result.setCode(ResultCode.SUCCESS.getCode());
        result.setMsg(ResultCode.SUCCESS.getMsg());
        result.setData(object);
        return result;
    }

    /**
     * 成功但不带数据
     **/
    public static Result success() {

        return success(null);
    }

    /**
     * 失败 自定义错误信息
     **/
    public static Result error(Object object) {
        Result result = new Result();
        result.setCode(ResultCode.ERROR.getCode());
        result.setMsg(ResultCode.ERROR.getMsg());
        result.setData(object);
        return result;
    }
}
