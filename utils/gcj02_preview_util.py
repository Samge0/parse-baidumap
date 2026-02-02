
# 高德地图sdk的围栏展示模板
from utils import fileutil


MAP_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>高德地图围栏展示-GCJ02</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        #map {
            width: 100%;
            height: 100%;
        }
    </style>
    <script type="text/javascript">
        window._AMapSecurityConfig = {
            securityJsCode: "TAG_SECURITY_CODE",
        };
    </script>
    <script src="https://webapi.amap.com/loader.js"></script>
</head>
<body>

<div id="map"></div>

<script type="text/javascript">
    // 示例 JSON 字符串（可以从服务器动态获取）
    var jsonString = `TAG_GEO_JSON`;

    // 解析 JSON 字符串为 JavaScript 对象
    var fenceData = JSON.parse(jsonString);

    console.log("fenceData:", fenceData);

    // 初始化地图
    AMapLoader.load({
        key: "TAG_APP_KEY", // 申请好的Web端开发者 Key，调用 load 时必填
        version: "2.0", // 指定要加载的 JS API 的版本，缺省时默认为 1.4.15
        plugins: ["AMap.Polygon", "AMap.Marker", "AMap.InfoWindow"] // 需要使用的的插件列表
    }).then((AMap) => {
        var center, marker;

        // 判断是否有中心点
        if (fenceData.features[0].properties.center && fenceData.features[0].properties.center.length === 2) {
            // 有中心点
            center = new AMap.LngLat(fenceData.features[0].properties.center[0], fenceData.features[0].properties.center[1]);
            // 创建地图实例
            var map = new AMap.Map("map", {
                viewMode: "2D",  // 使用2D视图
                zoom: 18,
                center: center,
                pitch: 0,  // 地图俯视角度
                rotation: 0  // 地图旋转角度
            });

            // 在中心点添加一个标记
            marker = new AMap.Marker({
                position: center,
                title: "围栏中心"
            });
            map.add(marker);
        } else {
            // 没有中心点则使用第一个多边形的第一个点
            var point = fenceData.features[0].geometry.coordinates[0][0];
            center = new AMap.LngLat(point[0], point[1]);
            // 创建地图实例
            var map = new AMap.Map("map", {
                viewMode: "2D",  // 使用2D视图
                zoom: 18,
                center: center,
                pitch: 0,  // 地图俯视角度
                rotation: 0  // 地图旋转角度
            });
        }

        // 设置地图状态，启用鼠标滚轮缩放
        map.setStatus({
            showIndoorMap: false,  // 关闭室内地图
            doubleClickZoom: true,  // 双击放大
            scrollWheel: true  // 鼠标滚轮缩放
        });

        // 添加地图控件
        AMap.plugin([
            "AMap.ToolBar",
            "AMap.Scale"
        ], function() {
            // 在图面添加工具条控件，工具条控件集成了缩放、平移、定位等功能按钮在内的组合控件
            map.addControl(new AMap.ToolBar({
                position: {
                    top: "110px",
                    right: "40px"
                }
            }));

            // 在图面添加比例尺控件，展示地图在当前层级和纬度下的比例尺
            map.addControl(new AMap.Scale());
        });

        // 获取围栏的坐标 - 这里默认只处理一个多边形的情况，可以根据实际情况进行修改
        var fenceCoordinates = fenceData.features[0].geometry.coordinates[0];
        console.log("fenceCoordinates:", fenceCoordinates);

        // 将围栏数据转为高德地图的坐标点
        var fencePath = fenceCoordinates.map(function(coord) {
            return new AMap.LngLat(coord[0], coord[1]);
        });
        console.log("fencePath:", fencePath);

        // 绘制多边形（围栏）
        var fencePolygon = new AMap.Polygon({
            path: fencePath,
            strokeColor: "#00D3FC",
            strokeWeight: 2,
            strokeOpacity: 0.8,
            fillColor: "#1791fc",
            fillOpacity: 0.3
        });
        map.add(fencePolygon);
        console.log("Polygon added to map");

        // 设置地图视野以适应多边形
        map.setFitView([fencePolygon]);

        // 添加提示框（如果有marker）
        if (marker && fenceData.features[0].properties.name) {
            var infoWindow = new AMap.InfoWindow({
                content: "<div style='padding:5px;'>" + fenceData.features[0].properties.name + "</div>",
                offset: new AMap.Pixel(0, -30)
            });

            marker.on("click", function() {
                infoWindow.open(map, marker.getPosition());
            });

            // 默认打开信息窗体
            infoWindow.open(map, center);
        }
    }).catch((e) => {
        console.error(e); //加载错误提示
    });
</script>

</body>
</html>
"""

# 生成GCJ02地图预览的html
def get_amap_preview_with_gcj02(app_key, security_code, geo_json) -> str:
    """生成高德地图预览HTML

    Args:
        app_key: 高德地图应用Key
        security_code: 高德地图安全密钥
        geo_json: GeoJSON格式的围栏数据

    Returns:
        HTML字符串
    """
    return (MAP_TEMPLATE
            .replace("TAG_APP_KEY", app_key)
            .replace("TAG_SECURITY_CODE", security_code)
            .replace("TAG_GEO_JSON", geo_json))


def save_preview_html(html_name, app_key, security_code, geo_str):
    """保存预览HTML文件

    Args:
        html_name: HTML文件名
        app_key: 高德地图应用Key
        security_code: 高德地图安全密钥
        geo_str: GeoJSON格式的围栏数据
    """
    # 生成地图
    html_str = get_amap_preview_with_gcj02(app_key, security_code, geo_str)
    html_save_path = fileutil.preview_dir + "/" + html_name
    fileutil.save(html_str, html_save_path)
