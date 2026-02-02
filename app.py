#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：

import os
import time
from typing import Literal, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import gradio as gr
import uvicorn
from tabs import tab_of_baidumap, tab_of_custom_preview_wgs84, tab_of_custom_preview_bd09, tab_of_custom_preview_gcj02, tab_of_about
import threading

from utils import fileutil, maputil, bd09_preview_util, gcj02_preview_util

app = FastAPI()

# 添加静态文件服务
preview_dir = fileutil.preview_dir
os.makedirs(preview_dir, exist_ok=True)
app.mount("/preview", StaticFiles(directory=preview_dir), name="preview")


# ========== FastAPI 接口 ==========

@app.get("/preview_geo")
async def preview_geo_map(
    geo_str: str = Query(..., description="百度地图返回的原始geo字符串"),
    md5: str = Query(..., description="用于生成唯一html文件名的md5值"),
    map_type: Literal["WGS84", "BD09", "GCJ02"] = Query("WGS84", description="坐标类型"),
    name: str = Query("", description="自定义地域名称"),
    adcode: str = Query("", description="自定义区域编码"),
    app_key: str = Query("", description="百度地图AK，仅BD09类型预览需要；高德Key，仅GCJ02类型预览需要"),
    security_code: str = Query("", description="高德地图安全密钥，仅GCJ02类型预览需要")
):
    """
    解析geo字符串并生成地图预览（GET方式）

    根据md5值生成指定的html文件名，访问后自动重定向到预览页面

    Args:
        geo_str: 百度地图返回的原始geo字符串
        md5: 用于生成唯一html文件名的md5值
        map_type: 坐标类型，可选 WGS84/BD09/GCJ02
        name: 自定义地域名称
        adcode: 自定义区域编码
        app_key: 百度地图AK，仅BD09类型预览需要；高德Key，仅GCJ02类型预览需要
        security_code: 高德地图安全密钥，仅GCJ02类型预览需要

    Returns:
        重定向到地图预览页面
    """
    if not geo_str:
        raise HTTPException(status_code=400, detail="geo参数不能为空")

    # 获取API基础URL
    api_base_url = os.environ.get("API_BASE_URL", "http://localhost:7862")

    try:
        if map_type == "WGS84":
            # 根据md5生成唯一文件名
            html_name = f"{md5}_wgs84_map.html"
            maputil.generate_wgs84_map_html(
                geo_str,
                maputil.get_map_html_path(html_name),
                name=name,
                adcode=adcode,
                output_map_type="WGS84"
            )
            preview_url = f"{api_base_url}/preview/{html_name}"

        elif map_type == "BD09":
            # 生成BD09地图预览
            if not app_key:
                raise HTTPException(status_code=400, detail="百度地图AK不能为空")

            # 解析geo数据
            bbox_result = maputil.parse_bbox_data(geo_str, "BD09")
            bbox_list = maputil.get_lat_lng_list(bbox_result)

            coordinates_result = maputil.parse_coordinates_data(geo_str, "BD09")
            coordinates_list = maputil.get_lat_lng_list(coordinates_result)

            center_point = maputil.calculate_center_point(bbox_list)
            result_json = maputil.export_json(coordinates_list, bbox_list, center_point, name, adcode)

            # 根据md5生成唯一文件名
            html_name = f"{md5}_bd09_map.html"
            bd09_preview_util.save_preview_html(html_name, app_key, result_json)
            preview_url = f"{api_base_url}/preview/{html_name}"

        elif map_type == "GCJ02":
            # 生成GCJ02地图预览
            if not app_key:
                raise HTTPException(status_code=400, detail="高德地图Key不能为空")

            if not security_code:
                raise HTTPException(status_code=400, detail="高德地图安全密钥不能为空")

            # 解析geo数据
            bbox_result = maputil.parse_bbox_data(geo_str, "GCJ02")
            bbox_list = maputil.get_lat_lng_list(bbox_result)

            coordinates_result = maputil.parse_coordinates_data(geo_str, "GCJ02")
            coordinates_list = maputil.get_lat_lng_list(coordinates_result)

            center_point = maputil.calculate_center_point(bbox_list)
            result_json = maputil.export_json(coordinates_list, bbox_list, center_point, name, adcode)

            # 根据md5生成唯一文件名
            html_name = f"{md5}_gcj02_map.html"
            gcj02_preview_util.save_preview_html(html_name, app_key, security_code, result_json)
            preview_url = f"{api_base_url}/preview/{html_name}"

        else:
            raise HTTPException(status_code=400, detail=f"不支持的地图类型: {map_type}")

        preview_url = f"{preview_url}?t={int(time.time() * 1000)}"

        # 重定向到预览页面
        return RedirectResponse(url=preview_url, status_code=302)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成地图预览失败: {str(e)}")


@app.get("/api/geo/parse")
async def parse_geo_map(
    geo_str: str = Query(..., description="百度地图返回的原始geo字符串"),
    map_type: Literal["WGS84", "BD09", "GCJ02"] = Query("WGS84", description="坐标类型"),
    name: str = Query("", description="自定义地域名称"),
    adcode: str = Query("", description="自定义区域编码")
):
    """
    解析geo字符串并返回JSON格式数据（GET方式）

    Args:
        geo_str: 百度地图返回的原始geo字符串
        map_type: 坐标类型，可选 WGS84/BD09/GCJ02
        name: 自定义地域名称
        adcode: 自定义区域编码

    Returns:
        解析后的GeoJSON格式数据
    """
    if not geo_str:
        raise HTTPException(status_code=400, detail="geo参数不能为空")

    try:
        # 解析坐标数据
        coordinates_result = maputil.parse_coordinates_data(geo_str, map_type)

        # 解析bbox数据
        bbox_result = maputil.parse_bbox_data(geo_str, map_type)

        # 转换为列表格式
        coordinates_list = maputil.get_lat_lng_list(coordinates_result)
        bbox_list = maputil.get_lat_lng_list(bbox_result)

        # 计算中心点
        center_point = maputil.calculate_center_point(bbox_list)

        # 导出为GeoJSON格式
        result_json = maputil.export_json(coordinates_list, bbox_list, center_point, name, adcode)

        return {
            "success": True,
            "data": result_json,
            "map_type": map_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析geo数据失败: {str(e)}")


# ========== Gradio 界面 ==========
with gr.Blocks(title="百度围栏解析") as iface:
    gr.Markdown("# 百度围栏解析")
    
    # 创建标签页
    with gr.Tabs():
        tab_of_baidumap.create_parser_tab()
        tab_of_custom_preview_wgs84.create_parser_tab()
        tab_of_custom_preview_bd09.create_parser_tab()
        tab_of_custom_preview_gcj02.create_parser_tab()
        tab_of_about.create_about_tab()

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=7862)

def run_gradio():
    iface.launch(server_name="0.0.0.0", server_port=7863)

if __name__ == "__main__":
    # 创建两个线程分别运行 FastAPI 和 Gradio
    fastapi_thread = threading.Thread(target=run_fastapi)
    gradio_thread = threading.Thread(target=run_gradio)
    
    # 启动线程
    fastapi_thread.start()
    gradio_thread.start()
    
    # 等待两个线程结束
    fastapi_thread.join()
    gradio_thread.join()
