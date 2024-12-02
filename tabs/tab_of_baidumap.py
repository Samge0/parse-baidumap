import os
import gradio as gr
from utils import maputil

def create_parser_tab():
    with gr.Tab("百度围栏解析"):
        gr.Markdown("请输入百度地图接口返回的geo参数字符串，点击提交，稍等片刻将解析出围栏坐标。")
        
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    name_input = gr.Textbox(label="自定义name", value="", lines=1)
                    adcode_input = gr.Textbox(label="自定义adcode", value="", lines=1)
                geo_input = gr.Textbox(label="输入geo字符串", value="", lines=16)
                json_format = gr.Checkbox(label="输出JSON格式", value=True)
                submit_btn = gr.Button("提交")
            
            with gr.Column():
                output = gr.Textbox(label="解析结果", lines=16)
                # 添加预览按钮和输出组件
                with gr.Row():
                    preview_btn = gr.Button("生成地图预览")
                    preview_link = gr.HTML()
        
        submit_btn.click(
            fn=parse_geo,
            inputs=[geo_input, json_format, name_input, adcode_input],
            outputs=output,
        )

        preview_btn.click(
            fn=preview_map,
            inputs=[geo_input],  # 假设您的坐标输入组件名为 geo_input
            outputs=[preview_link]
        )

def parse_geo(geo_input, json_format, name_input, adcode_input):
    """geo参数解析

    Args:
        geo_input (str): geo参数
        json_format (bool): 是否返回json格式
        name_input (str): 自定义地域名称
        adcode_input (str): 自定义区域编码

    Returns:
        _type_: str
    """
    if not geo_input:
        return "geo参数不能为空"
    
    coordinates_result = maputil.parse_coordinates_data(geo_input)
    if json_format is False:
        return coordinates_result
    
    # 导出为GeoJSON格式
    bbox_result = maputil.parse_bbox_data(geo_input)
    
    coordinates_list = maputil.get_lat_lng_list(coordinates_result)
    bbox_list = maputil.get_lat_lng_list(bbox_result)
    center_point = maputil.calculate_center_point(bbox_list)
    return maputil.export_json(coordinates_list, bbox_list, center_point, name_input, adcode_input)

# 生成地图预览的html
def preview_map(geo_str):
    if not geo_str:
        return "请先输入坐标数据"
    
    # fastapi的基础url
    api_base_url = os.environ.get("API_BASE_URL", "http://localhost:7862")
    
    # 生成地图
    html_name: str = "baidu_map.html"
    maputil.generate_map_html(geo_str, maputil.get_map_html_path(html_name))
    
    # 返回预览链接
    preview_url = f"{api_base_url}/preview/{html_name}"
    return f'<a href="{preview_url}" target="_blank">点击查看地图预览</a>'