import gradio as gr
from chatbot import Chatbot


def toggle_sidebar(state):
        """
        Toggle the visibility state of a UI component.

        Parameters:
            state: The current state of the UI component.

        Returns:
            Tuple: A tuple containing the updated UI component state and the new state.
        """
        state = not state
        return gr.update(visible=state), state

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("DOUNIA-GPT"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                with gr.Column(visible=False) as reference_bar:
                    ref_output = gr.Markdown()
                    

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        bubble_full_width=False,
                        height=500,
                        avatar_images=(
                            ("images/AI_RT.png"), "images/openai_.png"),
                        # render=False
                    )
            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Enter text and press enter",
                    container=False,
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit text")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(
                    value="References")
                btn_toggle_sidebar.click(toggle_sidebar, [sidebar_state], [
                    reference_bar, sidebar_state])
                
                temperature_bar = gr.Slider(minimum=0, maximum=1, value=0, step=0.1,
                                            label="Temperature", info="Choose between 0 and 1")
                rag_with_dropdown = gr.Dropdown(
                    label="RAG with", choices=["Preprocessed doc", "Upload doc: Give Full summary"], value="Preprocessed doc")
                clear_button = gr.ClearButton([input_txt, chatbot])
            ##############
            
            txt_msg = input_txt.submit(fn=Chatbot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown, temperature_bar],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=Chatbot.respond,
                                            inputs=[chatbot, input_txt,
                                                    rag_with_dropdown, temperature_bar],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)
            

demo.launch()
