## 百度地图围栏参数解析-docker镜像

### 构建api正式包
```shell
docker build . -t samge/parse-baidumap -f docker/Dockerfile
```

### 上传
```shell
docker push samge/parse-baidumap
```

### 运行docker镜像
```shell
docker run -d \
--name parse-baidumap \
-p 7863:7863 \
--pull=always \
--restart always \
--memory=0.5G \
samge/parse-baidumap:latest
```