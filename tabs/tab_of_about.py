#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：

import os
import gradio as gr
from utils import fileutil


def create_about_tab():
    with gr.Tab("关于"):
        gr.Markdown(fileutil.read(os.path.join(fileutil.project_dir, "DEMO.md")))