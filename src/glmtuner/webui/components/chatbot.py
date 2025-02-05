from typing import Dict, Optional, Tuple

import gradio as gr
from gradio.blocks import Block
from gradio.components import Component

from glmtuner.webui.chat import WebChatModel


def create_chat_box(
    chat_model: WebChatModel,
    visible: Optional[bool] = False
) -> Tuple[Block, Component, Component, Dict[str, Component]]:
    with gr.Box(visible=visible) as chat_box:
        chatbot = gr.Chatbot()

        with gr.Row():
            with gr.Column(scale=4):
                prefix = gr.Dropdown(show_label=False)
                query = gr.Textbox(show_label=False, lines=8)
                submit_btn = gr.Button(variant="primary")

            with gr.Column(scale=1):
                clear_btn = gr.Button()
                max_length = gr.Slider(
                    10, 2048, value=chat_model.generating_args.max_length, step=1, interactive=True
                )
                top_p = gr.Slider(0.01, 1, value=chat_model.generating_args.top_p, step=0.01, interactive=True)
                temperature = gr.Slider(
                    0.01, 1.5, value=chat_model.generating_args.temperature, step=0.01, interactive=True
                )

    history = gr.State([])

    submit_btn.click(
        chat_model.predict,
        [chatbot, query, history, prefix, max_length, top_p, temperature],
        [chatbot, history],
        show_progress=True
    ).then(
        lambda: gr.update(value=""), outputs=[query]
    )

    clear_btn.click(lambda: ([], []), outputs=[chatbot, history], show_progress=True)

    return chat_box, chatbot, history, dict(
        prefix=prefix,
        query=query,
        submit_btn=submit_btn,
        clear_btn=clear_btn,
        max_length=max_length,
        top_p=top_p,
        temperature=temperature
    )
