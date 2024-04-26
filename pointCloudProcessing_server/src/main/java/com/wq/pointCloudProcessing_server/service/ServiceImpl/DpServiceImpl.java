package com.wq.pointCloudProcessing_server.service.ServiceImpl;


import org.springframework.stereotype.Service;
import com.wq.pointCloudProcessing_server.service.DpService;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.*;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import com.wq.pointCloudProcessing_server.util.Result;
import com.wq.pointCloudProcessing_server.util.ResultUtil;
import org.springframework.web.multipart.MultipartFile;


@Service
public class DpServiceImpl implements DpService {

    private static final String SCRIPT_ROOT = "F:\\repo\\point_cloud_processing\\3D-Model-Monocular-Vision-main";
    private static final String PYTHON_EXECUTABLE = "D:\\dev\\anaconda\\envs\\point_cloud_processing\\python.exe";
    private static final String UNZIP_PATH = "F:\\repo\\point_cloud_processing\\server_files\\UNZIPFilesToDp";
    // 将脚本及其参数作为成员变量
    private final List<String> scripts = Arrays.asList(
            "match_images.py",
            "sanity_panorama.py",
            "search_point_in_panorama.py",
            "solve_param_each_part.py",
            "match_difference.py",
            "calib_pcd_panorama.py"
    );

    @Override
    public Result executeDpScripts(String... args) {

        String extractedFolderPath;
        String folderName;
        if (args.length == 0) {
            extractedFolderPath = "input";
            folderName = "00000000-1628";
        } else {
            // 假设第一个参数是解压后的文件夹路径
            extractedFolderPath = args[0];
            folderName = args[1];
        }
        // 用于存储所有脚本的执行结果
        StringBuilder result = new StringBuilder();

        for (String script : scripts) {
            List<String[]> scriptArgs = new ArrayList<>();
            // 根据脚本名称，准备相应的参数
            if (script.equals("match_images.py")) {
                scriptArgs.add(new String[]{"-i", extractedFolderPath});
                scriptArgs.add(new String[]{"-f", folderName}); // 此处替换为实际的文件夹名称
                scriptArgs.add(new String[]{"-o", "output/panorama"}); // 输出目录
            } else if (script.equals("sanity_panorama.py")) {
                scriptArgs.add(new String[]{"-m", "DPT_BEiT_L_384"});
                scriptArgs.add(new String[]{"-i", "output/panorama"}); // 假设这是上一个脚本的输出
                scriptArgs.add(new String[]{"-f", folderName}); // 文件夹名称
                scriptArgs.add(new String[]{"-o", "output"}); // 输出目录
                scriptArgs.add(new String[]{"-s", "170"}); // shift 参数
                scriptArgs.add(new String[]{"-d", "6"}); // divide 参数
            }else if(script.equals("search_point_in_panorama.py")){
                scriptArgs.add(new String[]{"-i", extractedFolderPath});
                scriptArgs.add(new String[]{"-f", folderName}); // 此处替换为实际的文件夹名称
                scriptArgs.add(new String[]{"-o", "output"}); // 输出目录
            }else if(script.equals("solve_param_each_part.py")){
                scriptArgs.add(new String[]{"-io", "output"});
                scriptArgs.add(new String[]{"-f", folderName}); // 文件夹名称
                scriptArgs.add(new String[]{"-df", "first_depth"}); // 输出目录
                scriptArgs.add(new String[]{"-s", "170"}); // shift 参数
                scriptArgs.add(new String[]{"-d", "6"}); // divide 参数
            }else if(script.equals("match_difference.py")){
                scriptArgs.add(new String[]{"-io", "output"});
                scriptArgs.add(new String[]{"-f", folderName}); // 文件夹名称
                scriptArgs.add(new String[]{"-df", "calib_param"}); // 输出目录
                scriptArgs.add(new String[]{"-s", "170"}); // shift 参数
                scriptArgs.add(new String[]{"-d", "6"}); // divide 参数
            }else if(script.equals("calib_pcd_panorama.py")){
                scriptArgs.add(new String[]{"-io", "output"});
                scriptArgs.add(new String[]{"-f", folderName}); // 文件夹名称
                scriptArgs.add(new String[]{"-df", "calib_param"}); // 输出目录
                scriptArgs.add(new String[]{"-s", "170"}); // shift 参数
                scriptArgs.add(new String[]{"-d", "6"}); // divide 参数
            }
            try {
                List<String> commandWithArgs = prepareScriptCommand(script, scriptArgs);
                Process process = executeScript(commandWithArgs);
                // 打印 Python 脚本的输出
                String scriptResult = readAndPrintProcessOutput(process); // 读取并打印输出
                result.append(script).append(": ").append(scriptResult).append("\n");

                int exitVal = process.waitFor();
                if (exitVal != 0) {
                    throw new RuntimeException("Abnormal script execution for script: " + script);
                }
                try {
                    Thread.sleep(50); // 等待
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt(); // 重新设置中断状态
                }
            } catch (Exception e) {
                e.printStackTrace();
                return ResultUtil.error("Error executing script: " + script + ". " + e.getMessage());
            }
        }
        return ResultUtil.success(result.toString());
    }

    private List<String> prepareScriptCommand(String script, List<String[]> scriptArgs) {
        List<String> commandWithArgs = new ArrayList<>();
        commandWithArgs.add(PYTHON_EXECUTABLE);
        commandWithArgs.add(new File(SCRIPT_ROOT, script).getAbsolutePath());

        for (String[] argPair : scriptArgs) {
            commandWithArgs.add(argPair[0]); // 参数名
            commandWithArgs.add(argPair[1]); // 参数值
        }

        return commandWithArgs;
    }





    private Process executeScript(List<String> commandWithArgs) throws IOException {
        System.out.println("Executing command: " + String.join(" ", commandWithArgs));
        ProcessBuilder processBuilder = new ProcessBuilder(commandWithArgs);
        processBuilder.directory(new File(SCRIPT_ROOT));
        processBuilder.redirectErrorStream(true);
        return processBuilder.start();
    }

    // 方法用于读取和打印流中的内容
    private String readAndPrintProcessOutput(Process process) throws IOException {
        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line); // 打印输出
                output.append(line).append("\n"); // 保存输出
            }
        }
        return output.toString();
    }


    @Override
    public Result handleZipUpload(MultipartFile file) {
        try {
            Files.createDirectories(Paths.get(UNZIP_PATH));
            String fileName = Objects.requireNonNull(file.getOriginalFilename());
            if (!fileName.toLowerCase().endsWith(".zip")) {
                return ResultUtil.error("Invalid file type. Only ZIP files are accepted.");
            }

            File destinationFile = new File(UNZIP_PATH, fileName);
            file.transferTo(destinationFile);

            String extractedFolderPath = unzipFile(destinationFile, UNZIP_PATH);
            String folderName = destinationFile.getName().substring(0, destinationFile.getName().lastIndexOf('.'));

            return executeDpScripts(UNZIP_PATH, folderName);
        } catch (Exception e) {
            e.printStackTrace();
            return ResultUtil.error("ZIP file upload and process failed: " + e.getMessage());
        }
    }
    private String unzipFile(File zipFile, String outputFolder) throws IOException {
        // 获取不带扩展名的文件名
        String folderNameWithoutExtension = zipFile.getName().substring(0, zipFile.getName().lastIndexOf('.'));
        // 创建一个新的目录，该目录以ZIP文件的名称命名
        File destDir = new File(outputFolder, folderNameWithoutExtension);

        if (!destDir.exists() && !destDir.mkdirs()) {
            throw new IOException("Could not create directory for unzipping.");
        }

        try (ZipInputStream zis = new ZipInputStream(Files.newInputStream(zipFile.toPath()))) {
            ZipEntry zipEntry = zis.getNextEntry();
            while (zipEntry != null) {
                // 获取条目的名称，并处理可能的顶层目录问题
                String entryName = zipEntry.getName();
                if (entryName.startsWith(folderNameWithoutExtension + "/")) {
                    entryName = entryName.substring(folderNameWithoutExtension.length() + 1);
                }
                File newFile = new File(destDir, entryName);

                if (zipEntry.isDirectory()) {
                    // 如果是目录，确保它被创建
                    if (!newFile.isDirectory() && !newFile.mkdirs()) {
                        throw new IOException("Could not create directory within ZIP structure.");
                    }
                } else {
                    // 如果是文件，确保其父目录存在，然后复制文件
                    File parentDir = newFile.getParentFile();
                    if (!parentDir.exists() && !parentDir.mkdirs()) {
                        throw new IOException("Could not create parent directory for file within ZIP structure.");
                    }
                    Files.copy(zis, newFile.toPath(), StandardCopyOption.REPLACE_EXISTING);
                }
                zipEntry = zis.getNextEntry();
            }
            zis.closeEntry();
        }

        // 返回新创建的目录的绝对路径
        return destDir.getAbsolutePath();
    }





    private File newFile(File destinationDir, ZipEntry zipEntry) throws IOException {
        File destFile = new File(destinationDir, zipEntry.getName());
        String destDirPath = destinationDir.getCanonicalPath();
        String destFilePath = destFile.getCanonicalPath();
        if (!destFilePath.startsWith(destDirPath + File.separator)) {
            throw new IOException("Entry is outside of the target dir: " + zipEntry.getName());
        }
        return destFile;
    }

}