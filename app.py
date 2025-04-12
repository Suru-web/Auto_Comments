import streamlit as st
import json
from python.app_python import split_code_python
from cpp.app_cpp import generate_comments_cpp
from java.app_java import generate_comments_java
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_lottie import st_lottie

st.title("Auto-Comment Generator using AI")

option = st.selectbox(
    label='Select the language you want to generate the comment for -',
    options=('Python','C++','Java'),
    placeholder='Select language...',
    index=None
)


if option:
    if option == 'Python':
        code_snippet = st.text_area(f"{option} Code", height=300, placeholder=f"Paste your {option} code here...")
        if st.button("Generate Comments"):
            if code_snippet:
                with st.spinner("Generating comments..."):
                    commented_code = split_code_python(code_snippet=code_snippet)
        
                st.subheader("Generated Comments:")
                st.code(commented_code, language="python")
            else:
                st.warning("Please enter some python code first.")
    elif option == 'C++':
        code_snippet = st.text_area(f"{option} Code", height=300, placeholder=f"Paste your {option} code here...")
        if st.button("Generate Comments"):
            if code_snippet:
                with st.spinner("Generating comments..."):
                    commented_code = generate_comments_cpp(code_snippet=code_snippet)
        
                st.subheader("Generated Comments:")
                st.code(commented_code, language="C++")
            else:
                st.warning("Please enter some C++ code first.")
    elif option == 'Java':
        code_snippet = st.text_area(f"{option} Code", height=300, placeholder=f"Paste your {option} code here...")
        if st.button("Generate Comments"):
            if code_snippet:
                with st.spinner("Generating comments..."):
                    commented_code = generate_comments_java(code_snippet=code_snippet)
        
                st.subheader("Generated Comments:")
                st.code(commented_code, language="Java")
            else:
                st.warning("Please enter some Java code first.")
else:
    @st.cache_resource
    def load_image_json(path):
        with open(path, 'r') as j:
            animation = json.loads(j.read())
        return animation
    add_vertical_space(10)
    lottie_json = load_image_json("static/type_lottie.json")
    left_col, center_col, right_col = st.columns([1, 2, 1])

    with center_col:
        st_lottie(
            lottie_json,
            key="lottie_animation",
            height=300,  # adjust as needed
            width=300
        )