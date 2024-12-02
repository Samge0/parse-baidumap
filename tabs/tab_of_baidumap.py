import gradio as gr
from utils import maputil

def create_parser_tab():
    with gr.Tab("百度围栏解析"):
        gr.Markdown("输入百度接口返回的geo参数字符串，点击提交则解析百度地图的围栏坐标。")
        
        with gr.Row():
            with gr.Column():
                geo_input = gr.Textbox(label="输入geo字符串", value="", lines=16)
                json_format = gr.Checkbox(label="输出JSON格式", value=True)
                submit_btn = gr.Button("提交")
            output = gr.Textbox(label="解析结果", lines=16)
        
        submit_btn.click(
            fn=parse_geo,
            inputs=[geo_input, json_format],
            outputs=output,
        )

# geo参数解析
def parse_geo(geo_input, json_format):
    if not geo_input:
        return "geo参数不能为空"
    
    coordinates_result = maputil.parse_coordinates_data(geo_input)
    if json_format is False:
        return coordinates_result
    
    # 导出为GeoJSON格式
    bbox_result = maputil.parse_bbox_data(geo_input)
    return maputil.export_json(get_lat_lng_list(coordinates_result), get_lat_lng_list(bbox_result))

# 获取坐标列表
def get_lat_lng_list(value: str) -> list:
    result_list = []
    for item in value.split(';'):
        if not item or "," not in item:
            continue
        item_splits = item.split(',')
        result_list.append([float(item_splits[0]), float(item_splits[1])])
    return result_list
