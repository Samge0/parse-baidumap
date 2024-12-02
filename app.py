import gradio as gr
from tabs import tab_of_baidumap, tab_of_about


# 创建 Gradio 界面
with gr.Blocks(title="百度围栏解析") as iface:
    gr.Markdown("# 百度围栏解析")
    
    # 创建标签页
    with gr.Tabs():
        tab_of_baidumap.create_parser_tab()
        tab_of_about.create_about_tab()


if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7863)
