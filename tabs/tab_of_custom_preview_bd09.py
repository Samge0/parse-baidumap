#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：

import os
import time
import gradio as gr
from utils import bd09_preview_util, fileutil

def create_parser_tab():
        
    with gr.Tab("BD09预览"):
        with gr.Column():
            geo_input = gr.Textbox(label="输入自定义的百度BD09围栏json", value="", lines=17)
            app_key = gr.Textbox(label="输入百度地图的浏览器类型应用AK", value="", lines=1)
            preview_btn = gr.Button("预览")
            preview_link = gr.HTML()

        preview_btn.click(
            fn=preview_map,
            inputs=[app_key, geo_input], 
            outputs=[preview_link]
        )
        
# 生成BD09地图预览的html
def preview_map(app_key, geo_str):
    if not geo_str:
        return "自定义的BD09地图围栏json不能为空"
    
    # fastapi的基础url
    api_base_url = os.environ.get("API_BASE_URL", "http://localhost:7862")
    
    # 生成地图
    html_name: str = "baidu_map_bd09.html"
    bd09_preview_util.save_preview_html(html_name, app_key, geo_str)
    
    # 返回预览链接
    preview_url = f"{api_base_url}/preview/{html_name}?t={time.time()}"
    return f'<a href="{preview_url}" target="_blank">点击查看BD09地图预览>></a>'
