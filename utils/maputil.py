import json
import math
import os
import folium

pi = 3.1415926535897932384626

def Yr(lnglat,b):
    """
    坐标转换的内部辅助函数
    Args:
        lnglat: 包含经纬度的列表 [经度, 纬度]
        b: 转换参数数组
    Returns:
        转换后的坐标列表
    """
    if b!='':
        c=b[0]+b[1]*abs(lnglat[0])
        d=abs(lnglat[1]/b[9])
        d=b[2]+b[3]*d+b[4]*d*d+b[5]*d*d*d+b[6]*d*d*d*d+b[7]*d*d*d*d*d+b[8]*d*d*d*d*d*d
        if 0>lnglat[0]:
            bd=-1*c
        else:
            bd=c
        lnglat[0]=bd
        if 0 > lnglat[0]:
            bd2 = -1 * d
        else:
            bd2 = d
        lnglat[1] = bd2
        return lnglat
    return

def Mecator2BD09(lng,lat):
    """
    墨卡托坐标转百度坐标(BD09)
    Args:
        lng: 经度
        lat: 纬度
    Returns:
        转换后的BD09坐标列表 [经度, 纬度]
    """
    lnglat=[0,0]
    Au=[[1.410526172116255E-8, 8.98305509648872E-6, -1.9939833816331, 200.9824383106796, -187.2403703815547,
          91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 1.73379812E7],
         [- 7.435856389565537E-9, 8.983055097726239E-6, -0.78625201886289, 96.32687599759846, -1.85204757529826,
          -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 1.026014486E7],
         [- 3.030883460898826E-8, 8.98305509983578E-6, 0.30071316287616, 59.74293618442277, 7.357984074871,
          -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
         [- 1.981981304930552E-8, 8.983055099779535E-6, 0.03278182852591, 40.31678527705744, 0.65659298677277,
          -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
         [3.09191371068437E-9, 8.983055096812155E-6, 6.995724062E-5, 23.10934304144901, -2.3663490511E-4,
          -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
         [2.890871144776878E-9, 8.983055095805407E-6, -3.068298E-8, 7.47137025468032, -3.53937994E-6, -0.02145144861037,
          -1.234426596E-5, 1.0322952773E-4, -3.23890364E-6, 826088.5]]
    Sp=[1.289059486E7, 8362377.87, 5591021, 3481989.83, 1678043.12, 0 ]
    lnglat[0]=math.fabs(lng)
    lnglat[1] =abs(lat)
    for d in range(0,6):
        if lnglat[1]>=Sp[d]:
            c=Au[d]
            break
    lnglat=Yr(lnglat,c)
    return lnglat

def BD092WGS84(lnglat):
    """
    百度坐标(BD09)转WGS84坐标
    Args:
        lnglat: BD09坐标列表 [经度, 纬度]
    Returns:
        WGS84坐标列表 [经度, 纬度]
    """
    #bd09-gcj

    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    pi = 3.1415926535897932384626  # π
    a = 6378245.0  # 长半轴
    ee = 0.00669342162296594323  # 扁率
    x = lnglat[0] - 0.0065
    y = lnglat[1] - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    lnglat[0] = z * math.cos(theta)
    lnglat[1] = z * math.sin(theta)

    dlat = tranlat1(lnglat[0] - 105.0, lnglat[1] - 35.0)
    dlng = tranlng1(lnglat[0] - 105.0, lnglat[1] - 35.0)
    radlat = lnglat[1] / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lnglat[1] + dlat
    mglng = lnglat[0] + dlng
    return [lnglat[0]* 2 - mglng, lnglat[1] * 2 - mglat]

def tranlat1(lng, lat):
    """
    纬度转换辅助函数
    Args:
        lng: 经度
        lat: 纬度
    Returns:
        转换后的纬度值
    """
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def tranlng1(lng, lat):
    """
    经度转换辅助函数
    Args:
        lng: 经度
        lat: 纬度
    Returns:
        转换后的经度值
    """
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def parse_map_data(point: list):
    """
    解析百度地图返回的地理数据字符串
    Args:
        geo_str: 百度地图返回的地理数据字符串
    Returns:
        转换后的坐标点字符串，格式为: "lng1,lat1;lng2,lat2;..."
    """
    point_transform=[]
    for i in range(int(len(point)/2)):#全部点的坐标，分别是x,y,的形式
        if "-" in point[2*i]:
            point[2*i] = point[2*i].split("-")[1]
        point[2*i+1] = point[2*i+1].replace(";", "")
        point_Mecator2BD09 = Mecator2BD09(float(point[2*i]),float(point[2*i+1]))
        point_BD092WGS84 = BD092WGS84(point_Mecator2BD09)
        point_transform.append(point_BD092WGS84)
        point_str = '' #这是创建一个文本存储
    for j in range(len(point_transform)):
        point_str = point_str+(str(point_transform[j])).replace(' ','')[1:-1]+';'
    return point_str

def parse_coordinates_data(geo_str: str):
    """
    解析百度地图返回的地理数据字符串
    Args:
        geo_str: 百度地图返回的地理数据字符串
    Returns:
        转换后的坐标点字符串，格式为: "lng1,lat1;lng2,lat2;..."
    """
    geo_str = geo_str.split('|')
    point = geo_str[2].split(",")
    return parse_map_data(point)


def parse_bbox_data(geo_str: str):
    """
    解析百度地图的边界坐标
    Args:
        geo_str: 百度地图返回的地理数据字符串
    Returns:
        转换后的坐标点字符串，格式为: "lng1,lat1;lng2,lat2;..."
    """
    geo_str = geo_str.split('|')
    point = geo_str[1].replace(";", ",").split(",")
    return parse_map_data(point)

def calculate_center_point(bbox) -> list:
    """
    计算地图中心点

    Args:
        bbox: bbox是一个包含两个顶点坐标的列表
                每个顶点坐标是一个包含经度和纬度的列表
                例如：bbox = [[114.03077380624964, 22.66439081064176], [114.0318688927557, 22.665754600064943]]

    Returns:
        list: 返回中心点坐标 [经度, 纬度]
    """
    # 获取两个顶点的坐标
    point1, point2 = bbox
    
    # 分别计算经度和纬度的中心点
    center_longitude = (point1[0] + point2[0]) / 2
    center_latitude = (point1[1] + point2[1]) / 2
    
    return [center_longitude, center_latitude]


def get_lat_lng_list(value: str) -> list:
    """获取坐标列表

    Args:
        value (str): 字符串格式的坐标， 例如："114.03077380624964, 22.66439081064176;114.0318688927557, 22.665754600064943"

    Returns:
        list: 列表格式的坐标， 例如：[[114.03077380624964, 22.66439081064176], [114.0318688927557, 22.665754600064943]]
    """
    result_list = []
    for item in value.split(';'):
        if not item or "," not in item:
            continue
        item_splits = item.split(',')
        result_list.append([float(item_splits[0]), float(item_splits[1])])
    return result_list

def export_json(coordinates: list, bbox: list, center: list, name: str = "", adcode: str = ""):
    """
    将坐标数据导出为GeoJSON格式
    Args:
        coordinates: 多边形坐标列表
        bbox: 边界框坐标列表
    Returns:
        GeoJSON格式的字符串
    """
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": name or "",
                    "adcode": adcode or "",
                    "center": center,
                    "coordinates": [coordinates or []]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": coordinates or []
                },
                "id": 0,
                "bbox": bbox or []
            }
        ]
    }
    return json.dumps(geojson_data, indent=4, ensure_ascii=False)

# 获取预览html的路径
def get_preview_dir() -> str:
    return os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace(os.sep, "/")

# 获取预览html的路径
def get_map_html_path(name: str = "baidu_map.html") -> str:
    return f"{get_preview_dir()}/{name}"

# 生成地图预览的html
def generate_map_html(geo_str, output_path=None):
    output_path = output_path or get_map_html_path()
    
    # 提取百度坐标
    coordinates = parse_coordinates_data(geo_str)

    coord_list = coordinates.split(";")
    coords_bd09 = []
    for coord in coord_list:
        if not coord:
            continue
        lon, lat = map(float, coord.split(","))
        bd_lon, bd_lat = lon, lat
        coords_bd09.append([bd_lat, bd_lon])

    # 使用 folium 绘制地图
    m = folium.Map(location=[coords_bd09[0][0], coords_bd09[0][1]], zoom_start=16)

    # 绘制路径
    folium.PolyLine(coords_bd09, color="blue", weight=2.5, opacity=1).add_to(m)

    # 添加标记
    for coord in coords_bd09:
        folium.Marker([coord[0], coord[1]], popup="Point").add_to(m)
        
    # 计算地图中心点
    bbox_data_str = parse_bbox_data(geo_str)
    bbox_data_list = get_lat_lng_list(bbox_data_str)
    center_point = calculate_center_point(bbox_data_list)
    cneter_latitude = center_point[1]
    cneter_longitude = center_point[0]
    folium.Marker([cneter_latitude, cneter_longitude], popup="Center").add_to(m)

    # 保存为 HTML 文件
    m.save(output_path)
    return output_path


if __name__ == "__main__":
    map_data = "4|12695276.107214,2575246.898054;12695398.766886,2575408.625579|1-12695366.8658416,2575392.4618367,12695367.3246584,2575392.0480759,12695368.4074447,2575390.9608554,12695369.4343485,2575389.8146679,12695370.4053700,2575388.6095128,12695371.3205166,2575387.3573857,12695372.1797883,2575386.0582861,12695397.7638376,2575339.7124229,12695398.3327817,2575338.5265863,12695398.6782887,2575337.2487992,12695398.7668862,2575335.9396425,12695398.6097571,2575334.6229071,12695398.2181190,2575333.3823636,12695397.5919924,2575332.2540005,12695396.7649118,2575331.2852001,12695348.9226943,2575285.3288418,12695308.9148051,2575248.2334993,12695307.9985057,2575247.5424643,12695306.9594709,2575247.0935888,12695305.8423856,2575246.8980542,12695304.7142875,2575246.9906245,12695303.6198486,2575247.3584884,12695302.6372439,2575247.9762260,12695301.7999631,2575248.8072372,12695287.8775657,2575260.4698876,12695286.9511486,2575261.7104263,12695286.0582476,2575262.9623498,12695285.1988759,2575264.2496494,12695284.3618573,2575265.5605335,12695283.5695314,2575266.8945930,12695282.7995587,2575268.2522367,12695282.0631090,2575269.6332599,12695278.3251837,2575276.8393202,12695277.6780816,2575278.1947241,12695277.1427051,2575279.5960647,12695276.7190543,2575281.0433413,12695276.3959528,2575282.5247627,12695276.1957270,2575284.0159273,12695276.1072138,2575285.5290356,12695276.1415697,2575287.0398912,12695276.7617220,2575297.3690089,12695276.8966192,2575298.8900195,12695277.1096994,2575300.3976010,12695277.4121322,2575301.8915488,12695277.7927410,2575303.3600721,12695278.2515258,2575304.8031711,12695278.7884796,2575306.2088502,12695279.4036022,2575307.5771098,12695304.2864520,2575359.4604241,12695327.7812998,2575405.4450230,12695328.5303430,2575406.5710279,12695329.4580052,2575407.5378364,12695330.5307559,2575408.3100713,12695331.1899549,2575408.6255789,12695333.8332612,2575407.7138068,12695338.8930213,2575405.7252990,12695346.2508582,2575402.7246921,12695352.9139473,2575399.7632265,12695352.9150642,2575399.7632063,12695359.7322373,2575396.7475041,12695362.2869830,2575395.3613163,12695365.9804929,2575393.1112346,12695366.8658416,2575392.4618367;"
    print(parse_map_data(map_data))    