import gradio as gr


def create_about_tab():
    with gr.Tab("关于"):
        gr.Markdown("""
        # 关于解析器
        
        这是一个百度围栏的参数解析工具
        """)