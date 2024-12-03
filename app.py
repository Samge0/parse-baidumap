#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import gradio as gr
import uvicorn
from tabs import tab_of_baidumap, tab_of_custom_preview, tab_of_about
import threading

from utils import fileutil

app = FastAPI()

# 添加静态文件服务
preview_dir = fileutil.preview_dir
os.makedirs(preview_dir, exist_ok=True)
app.mount("/preview", StaticFiles(directory=preview_dir), name="preview")

# 创建 Gradio 界面
with gr.Blocks(title="百度围栏解析") as iface:
    gr.Markdown("# 百度围栏解析")
    
    # 创建标签页
    with gr.Tabs():
        tab_of_baidumap.create_parser_tab()
        tab_of_custom_preview.create_parser_tab()
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
