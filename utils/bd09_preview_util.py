

# 百度sdk的围栏展示模板
from utils import fileutil


MAP_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>百度地图围栏展示-BD09</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;  /* 确保父容器占满整个浏览器 */
        }
        #map {
            width: 100%;   /* 宽度占满整个容器 */
            height: 100vh; /* 高度占满视口 */
        }
    </style>
    <script type="text/javascript" src="https://api.map.baidu.com/api?v=3.0&ak=TAG_APP_KEY"></script>
</head>
<body>

<div id="map"></div>

<script type="text/javascript">
    // 示例 JSON 字符串（可以从服务器动态获取）
    var jsonString = `TAG_GEO_JSON`;

    // 解析 JSON 字符串为 JavaScript 对象
    var fenceData = JSON.parse(jsonString);

    // 初始化地图，设置中心点和缩放级别
    var map = new BMap.Map("map");
    var center = new BMap.Point(fenceData.features[0].properties.center[0], fenceData.features[0].properties.center[1]);
    map.centerAndZoom(center, 16);

    // 启用鼠标滚轮缩放
    map.enableScrollWheelZoom();
    
    // 获取围栏的坐标
    var fenceCoordinates = fenceData.features[0].geometry.coordinates[0];

    // 将围栏数据转为百度地图的坐标点
    var fencePath = fenceCoordinates.map(function(coord) {
        return new BMap.Point(coord[0], coord[1]);
    });

    // 绘制多边形（围栏）
    var fencePolygon = new BMap.Polygon(fencePath, {
        strokeColor: "blue",
        strokeWeight: 2,
        strokeOpacity: 0.5,
        fillColor: "blue",
        fillOpacity: 0.3
    });
    map.addOverlay(fencePolygon);

    // 在中心点添加一个标记
    var marker = new BMap.Marker(center);
    map.addOverlay(marker);

    // 添加提示框
    var infoWindow = new BMap.InfoWindow(fenceData.features[0].properties.name, { width: 200, height: 100, title: "围栏中心" });
    marker.addEventListener("click", function() {
        this.openInfoWindow(infoWindow);
    });
</script>

</body>
</html>
"""

# 生成BD09地图预览的html
def get_baidu_map_preview_with_bd09(app_key, geo_json) -> str:
    return MAP_TEMPLATE.replace("TAG_APP_KEY", app_key).replace("TAG_GEO_JSON", geo_json)


def save_preview_html(html_name, app_key, geo_str):
    # 生成地图
    html_str = get_baidu_map_preview_with_bd09(app_key, geo_str)
    html_save_path = fileutil.preview_dir + "/" + html_name
    fileutil.save(html_str, html_save_path)