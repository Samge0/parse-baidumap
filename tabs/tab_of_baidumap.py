#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：

import os
import tempfile
import time
import gradio as gr
from utils import bd09_preview_util, maputil

def create_parser_tab():
    with gr.Tab("解析"):
        
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    name_input = gr.Textbox(label="自定义name", value="", lines=1)
                    adcode_input = gr.Textbox(label="自定义adcode", value="", lines=1)
                geo_input = gr.Textbox(label="输入geo字符串", value="", lines=16, max_lines=16)
                
                with gr.Row():
                    json_format = gr.Checkbox(label="输出JSON格式", value=True)
                    output_map_type = gr.Dropdown(label="坐标系统选择", choices=["WGS84", "BD09", "GCJ02"], value="WGS84")  # 默认选择WGS84
                    app_key = gr.Textbox(label="百度地图AK", value="", lines=1, placeholder="仅BD09类型预览需要输入AK")
                
                with gr.Row():
                    submit_btn = gr.Button("提交")
                    preview_btn = gr.Button("预览")
                
                with gr.Row():
                    blank_block = gr.HTML() # 占位空白块
                    preview_link = gr.HTML()
            
            with gr.Column():
                output = gr.Textbox(label="解析结果", lines=30)
                download_file = gr.File(label="解析结果文件下载", visible=False)
        
        submit_btn.click(
            fn=parse_geo,
            inputs=[geo_input, json_format, name_input, adcode_input, output_map_type],
            outputs=[output, download_file],
        )

        preview_btn.click(
            fn=preview_map,
            inputs=[geo_input, name_input, adcode_input, output_map_type, app_key],  # 假设您的坐标输入组件名为 geo_input
            outputs=[preview_link]
        )

def parse_geo(geo_input, json_format, name_input, adcode_input, output_map_type):
    """geo参数解析

    Args:
        geo_input (str): geo参数
        json_format (bool): 是否返回json格式
        name_input (str): 自定义地域名称
        adcode_input (str): 自定义区域编码
        output_map_type (str): 坐标类型

    Returns:
        _type_: str
    """
    if not geo_input:
        return "geo参数不能为空", None
    
    coordinates_result = maputil.parse_coordinates_data(geo_input, output_map_type)
    
    if json_format is False:
        suffix = ".txt"
        result_str = coordinates_result
    else:
        # 导出为GeoJSON格式
        suffix = ".json"
        bbox_result = maputil.parse_bbox_data(geo_input, output_map_type)
        coordinates_list = maputil.get_lat_lng_list(coordinates_result)
        bbox_list = maputil.get_lat_lng_list(bbox_result)
        center_point = maputil.calculate_center_point(bbox_list)
        result_str = maputil.export_json(coordinates_list, bbox_list, center_point, name_input, adcode_input)
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(result_str)
        file_path = tmp_file.name
        
    return result_str, gr.update(value=file_path, visible=True)

# 生成WGS84地图预览的html
def preview_map(geo_str, name_input, adcode_input, output_map_type, app_key):
    
    if output_map_type == "GCJ02":
        return "GCJ02坐标不支持预览"
    
    if not geo_str:
        return "geo参数不能为空"
    
    # fastapi的基础url
    api_base_url = os.environ.get("API_BASE_URL", "http://localhost:7862")
    
    if output_map_type == "WGS84":
        # 生成地图
        html_name: str = "wgs84_map.html"
        maputil.generate_wgs84_map_html(geo_str, maputil.get_map_html_path(html_name))
        
        # 返回预览链接
        preview_url = f"{api_base_url}/preview/{html_name}?t={time.time()}"
        return f'<a href="{preview_url}" target="_blank">点击查看WGS84地图预览>></a>'
    
    elif output_map_type == "BD09":
        
        if not app_key:
            return "百度地图AK不能为空"
        
        bbox_result = maputil.parse_bbox_data(geo_str, output_map_type)
        bbox_list = maputil.get_lat_lng_list(bbox_result)
        
        coordinates_result = maputil.parse_coordinates_data(geo_str, output_map_type)
        coordinates_list = maputil.get_lat_lng_list(coordinates_result)
        
        center_point = maputil.calculate_center_point(bbox_list)
        result_str = maputil.export_json(coordinates_list, bbox_list, center_point, name_input, adcode_input)
        
        # 生成地图
        html_name: str = "baidu_map_bd09.html"
        bd09_preview_util.save_preview_html(html_name, app_key, result_str)
        
        # 返回预览链接
        preview_url = f"{api_base_url}/preview/{html_name}?t={time.time()}"
        return f'<a href="{preview_url}" target="_blank">点击查看BD09地图预览>></a>'