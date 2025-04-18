import streamlit as st
import base64
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part
import os
import json

from agents.design_agent import DesignAgent
from agents.component_agent import ComponentAgent
from agents.branding_agent import BrandingAgent
from agents.code_agent import CodeAgent
from agents.logic_agent import LogicAgent
from agents.export_agent import ExportAgent

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './snap-code.json'
project_id = "snapcode-434710"
aiplatform.init(project=project_id)

st.set_page_config(layout="wide")
st.markdown("""<style> .block-container {padding: 2rem;} ... </style>""", unsafe_allow_html=True)
st.markdown("""<div class="main-header"><h1>UI Automation Tool</h1><p>Turn images into code with the power of AI</p></div>""", unsafe_allow_html=True)

def download_button(code, filename="generated_code.html"):
    b64 = base64.b64encode(code.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-btn">Download the generated code</a>'
    st.markdown(href, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2.5, 1], gap="medium")

with col1:
    st.markdown("### Technology Selection")
    frontend_options = [
        "HTML5 + Tailwind", "HTML5 + CSS", "HTML5 + Bootstrap5",
        "React + Tailwind", "Ionic + Tailwind", "Vz Brand"
    ]
    selected_frontend = st.selectbox("Select Technology:", frontend_options)
    apply_branding = st.checkbox("Apply Branding Guidelines")
    submit = st.button("Submit")

with col2:
    st.markdown("### Upload Screenshot and Generate Code")
    uploaded_image = st.file_uploader("Upload a screenshot (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Screenshot", use_column_width=True)

    if uploaded_image and submit:
        try:
            image_bytes = uploaded_image.read()
            mime_type = uploaded_image.type

            # 1. Design Agent
            design_agent = DesignAgent(image_bytes, mime_type)
            layout_info = design_agent.run()
            st.markdown("#### DesignAgent Output:")
            st.code(layout_info)
            if not layout_info:
                st.error("DesignAgent did not return any output.")
                st.stop()

            # 2. Component Agent
            component_agent = ComponentAgent(layout_info)
            components = component_agent.run()
            st.markdown("#### ComponentAgent Output:")
            st.code(components)
            if not components:
                st.error("ComponentAgent did not return any output.")
                st.stop()

            branding = None
            # 3. Branding Agent (optional)
            if apply_branding:
                branding_agent = BrandingAgent(components)
                branding = branding_agent.run()
                st.markdown("#### BrandingAgent Output:")
                st.code(branding)
                if not branding:
                    st.error("BrandingAgent did not return any output.")
                    st.stop()

            # 4. Code Agent
            code_agent = CodeAgent(selected_frontend, branding)
            code_result = code_agent.run(components)
            st.markdown("#### CodeAgent Prompt Used:")
            st.code(code_agent.get_prompt(components), language="markdown")
            st.markdown("#### Generated Code:")
            st.code(code_result, language='html' if 'HTML5' in selected_frontend else 'jsx')
            if not code_result:
                st.error("CodeAgent did not return any output.")
                st.stop()

            # 5. Logic Agent
            logic_agent = LogicAgent(selected_frontend)
            enhanced_code = logic_agent.run(code_result)
            st.markdown("#### Enhanced Code with Logic:")
            st.code(enhanced_code, language='html' if 'HTML5' in selected_frontend else 'jsx')
            if not enhanced_code:
                st.error("LogicAgent did not return any output.")
                st.stop()

            # 6. Export Agent
            export_agent = ExportAgent()
            download_link = export_agent.run(enhanced_code)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.balloons()

with col3:
    st.markdown("### Actions")
    if 'enhanced_code' in locals() and enhanced_code:
        download_button(enhanced_code)