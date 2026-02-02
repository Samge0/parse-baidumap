## 百度地图围栏坐标参数解析小工具


### 环境
```shell
conda create -n parse-baidumap -y python=3.10.13
```

### 安装依赖
```shell
pip install -r requirements.txt
```

### 运行
```shell
python app.py
```

### 解析示例
[点击查看解析示例数据>>](./DEMO.md)


### 相关截图

- geo字符串参考来源：
![image](https://github.com/user-attachments/assets/42dbf24a-c0f7-489c-9bf7-e9941d2846cc)


- gradio界面
![image](https://github.com/user-attachments/assets/c946cb85-2c73-42a0-9e85-92b2fcfdde49)


- 运行`main.py`后验证围栏坐标 / 点击查看WGS84地图预览>>
![image](https://github.com/user-attachments/assets/3a2e5e05-a378-446e-aef7-9b022fa37c4e)


### API 接口说明

#### 1. 地图预览接口 `/preview_geo`

解析百度地图geo字符串并生成地图预览页面（GET方式）

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| geo_str | string | 是 | 百度地图返回的原始geo字符串（需要URL编码） |
| md5 | string | 是 | 用于生成唯一html文件名的md5值 |
| map_type | string | 否 | 坐标类型，可选值：WGS84/BD09/GCJ02，默认：WGS84 |
| name | string | 否 | 自定义地域名称 |
| adcode | string | 否 | 自定义区域编码 |
| app_key | string | 条件必填 | BD09类型预览需要百度地图AK；GCJ02类型预览需要高德Key |
| security_code | string | 条件必填 | GCJ02类型预览需要高德地图安全密钥 |

**请求示例：**

```bash
# WGS84预览
curl "http://127.0.0.1:7862/preview_geo?geo_str=4%7C12695276.107214%2C2575246.898054%3B12695398.766886%2C2575408.625579%7C1-12695366.8658416%2C2575392.4618367...&md5=abc123&map_type=WGS84&name=测试区域&adcode=110101"

# BD09预览（需要百度地图AK）
curl "http://127.0.0.1:7862/preview_geo?geo_str=...&md5=abc123&map_type=BD09&app_key=YOUR_BAIDU_AK"

# GCJ02预览（需要高德Key和安全密钥）
curl "http://127.0.0.1:7862/preview_geo?geo_str=...&md5=abc123&map_type=GCJ02&app_key=YOUR_AMAP_KEY&security_code=YOUR_AMAP_SECURITY_CODE"
```

**返回结果：**
- 成功：302重定向到地图预览页面
- 失败：400错误，返回错误详情

---

#### 2. geo解析接口 `/api/geo/parse`

解析百度地图geo字符串并返回JSON格式数据（GET方式）

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| geo_str | string | 是 | 百度地图返回的原始geo字符串（需要URL编码） |
| map_type | string | 否 | 坐标类型，可选值：WGS84/BD09/GCJ02，默认：WGS84 |
| name | string | 否 | 自定义地域名称 |
| adcode | string | 否 | 自定义区域编码 |

**请求示例：**

```bash
curl "http://127.0.0.1:7862/api/geo/parse?geo_str=4%7C12695276.107214%2C2575246.898054%3B12695398.766886%2C2575408.625579%7C1-12695366.8658416%2C2575392.4618367...&map_type=WGS84&name=测试区域&adcode=110101"
```

**返回结果示例：**

```json
{
    "success": true,
    "data": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "测试区域",
                    "adcode": "110101",
                    "center": [116.397428, 39.90923]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[116.397428, 39.90923], ...]]
                },
                "id": 0,
                "bbox": [[116.397428, 39.90923], [116.398428, 39.91023]]
            }
        ]
    },
    "map_type": "WGS84"
}
```

---

### 服务端口

- **FastAPI服务**: `http://127.0.0.1:7862` (API接口)
- **Gradio界面**: `http://127.0.0.1:7863` (Web界面)
