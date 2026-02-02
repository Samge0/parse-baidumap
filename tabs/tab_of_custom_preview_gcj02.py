#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：高德地图围栏预览tab页

import os
import time
import gradio as gr
from utils import gcj02_preview_util, maputil

def create_parser_tab():

    with gr.Tab("GCJ02预览"):
        with gr.Column():
            geo_input = gr.Textbox(label="输入自定义的GCJ02围栏GeoJSON", value="", lines=17)
            app_key = gr.Textbox(label="输入高德地图的应用Key", value="", lines=1)
            security_code = gr.Textbox(label="输入高德地图的安全密钥", value="", lines=1)
            preview_btn = gr.Button("预览")
            preview_link = gr.HTML()

        preview_btn.click(
            fn=preview_map,
            inputs=[app_key, security_code, geo_input],
            outputs=[preview_link]
        )

def preview_map(app_key, security_code, geo_str):
    """生成GCJ02地图预览的html

    Args:
        app_key: 高德地图应用Key
        security_code: 高德地图安全密钥
        geo_str: GeoJSON格式的围栏数据

    Returns:
        预览链接HTML字符串
    """
    if not geo_str:
        return "自定义的GCJ02地图围栏GeoJSON不能为空"

    if not app_key:
        return "高德地图应用Key不能为空"

    if not security_code:
        return "高德地图安全密钥不能为空"

    # fastapi的基础url
    api_base_url = os.environ.get("API_BASE_URL", "http://127.0.0.1:7862")

    # 生成地图
    html_name: str = "amap_map_gcj02.html"
    gcj02_preview_util.save_preview_html(html_name, app_key, security_code, geo_str)

    # 返回预览链接
    preview_url = f"{api_base_url}/preview/{html_name}?t={time.time()}"
    return f'<a href="{preview_url}" target="_blank">点击查看GCJ02高德地图预览>></a>'
