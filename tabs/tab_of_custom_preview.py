#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：

import os
import time
import gradio as gr
from utils import maputil

def create_parser_tab():
    with gr.Tab("预览"):
        
        with gr.Column():
            geo_input = gr.Textbox(label="输入自定义的百度围栏json", value="", lines=20)
            preview_btn = gr.Button("预览")
            preview_link = gr.HTML()

        preview_btn.click(
            fn=preview_map,
            inputs=[geo_input], 
            outputs=[preview_link]
        )

# 生成地图预览的html
def preview_map(geo_str):
    if not geo_str:
        return "自定义的百度围栏json不能为空"
    
    # fastapi的基础url
    api_base_url = os.environ.get("API_BASE_URL", "http://localhost:7862")
    
    # 生成地图
    html_name: str = "baidu_map.html"
    try:
        maputil.generate_map_html_by_json(geo_str, maputil.get_map_html_path(html_name))
    except Exception as e:
        return f"自定义的百度围栏json不符合要求，请参考示例进行调整。错误信息：${e}"
    
    # 返回预览链接
    preview_url = f"{api_base_url}/preview/{html_name}?t={time.time()}"
    return f'<a href="{preview_url}" target="_blank">点击查看地图预览>></a>'