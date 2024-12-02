#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-12-02 23:35
# describe：文件相关工具

import os
import threading

# 项目根目录
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace(os.sep, "/")

# 预览目录
preview_dir = os.path.join(project_dir, "preview")
os.makedirs(preview_dir, exist_ok=True)


lock = threading.Lock()


def save(_txt: str, _path: str, _type: str = 'w+') -> bool:
    """保存文件"""
    lock.acquire()  
    try:
        with open(_path, _type, encoding='utf-8') as f:
            f.write(_txt)
            f.flush()
            f.close()
        return True
    except:
        return False
    finally:
        lock.release()  


def read(_path: str) -> str:
    """读取文件"""
    if not _path or os.path.exists(_path) is False:
        return ''
    with open(_path, "r", encoding='utf-8') as f:
        txt = f.read()
        f.close()
        return txt or ''