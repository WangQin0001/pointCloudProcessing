package com.wq.pointCloudProcessing_server.dto;

        import lombok.Data;
        import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class RaspberryPiDto {
    private String methodName;
    private Integer step;
    private Integer dir;
    private Integer angle;
}

