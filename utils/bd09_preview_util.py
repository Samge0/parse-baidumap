

# 百度sdk的围栏展示模板
from utils import fileutil


MAP_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>百度地图围栏展示-BD09</title>
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
    <script type="text/javascript" src="https://api.map.baidu.com/api?v=1.0&type=webgl&ak=TAG_APP_KEY"></script>
</head>
<body>

<div id="map"></div>

<script type="text/javascript">
    // 示例 JSON 字符串（可以从服务器动态获取）
    var jsonString = `TAG_GEO_JSON`;

    // 解析 JSON 字符串为 JavaScript 对象
    var fenceData = JSON.parse(jsonString);

    // 初始化地图，设置中心点和缩放级别
    var map = new BMapGL.Map("map");
    var center, marker;

    if (fenceData.features[0].properties.center && fenceData.features[0].properties.center.length === 2) {
        // 有中心点
        center = new BMapGL.Point(fenceData.features[0].properties.center[0], fenceData.features[0].properties.center[1]);
        map.centerAndZoom(center, 18);
        // 在中心点添加一个标记
        marker = new BMapGL.Marker(center);
        map.addOverlay(marker);
    } else {
        // 没有中心点则使用第一个多边形的第一个点
        var point = fenceData.features[0].geometry.coordinates[0][0];
        center = new BMapGL.Point(point[0], point[1]);
        map.centerAndZoom(center, 18);
    }

    // 启用鼠标滚轮缩放
    map.enableScrollWheelZoom();

    // 设置地图类型为普通地图
    map.setMapType(BMAP_NORMAL_MAP);

    // 添加地图控件
    map.addControl(new BMapGL.NavigationControl());
    map.addControl(new BMapGL.ScaleControl());

    // 获取围栏的坐标 - 这里默认只处理一个多边形的情况，可以根据实际情况进行修改
    var fenceCoordinates = fenceData.features[0].geometry.coordinates[0];

    // 将围栏数据转为百度地图的坐标点
    var fencePath = fenceCoordinates.map(function(coord) {
        return new BMapGL.Point(coord[0], coord[1]);
    });

    // 绘制多边形（围栏）
    var fencePolygon = new BMapGL.Polygon(fencePath, {
        strokeColor: "blue",
        strokeWeight: 2,
        strokeOpacity: 0.5,
        fillColor: "#4285f4",
        fillOpacity: 0.3
    });
    map.addOverlay(fencePolygon);

    // 添加提示框（如果有marker）
    if (marker && fenceData.features[0].properties.name) {
        var infoWindow = new BMapGL.InfoWindow(fenceData.features[0].properties.name, {
            width: 200,
            height: 80,
            title: "围栏信息"
        });
        marker.addEventListener("click", function() {
            map.openInfoWindow(infoWindow, center);
        });
    }
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