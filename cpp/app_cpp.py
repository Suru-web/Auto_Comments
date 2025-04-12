import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

# Load pre-trained model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("../cpp/model/model_cpp_small")
    model = AutoModelForSeq2SeqLM.from_pretrained("../cpp/model/model_cpp_small")
    return tokenizer, model

tokenizer, model = load_model()

# Function to generate comments for C++ code
def generate_comments(code_snippet):
    # Preprocess the code - extract method signatures, etc.
    # This is a simplified version; you might need more sophisticated parsing
    methods = re.findall(r'(\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\})', code_snippet)
    
    commented_code = code_snippet
    
    for method in methods:
        # Tokenize the method
        inputs = tokenizer(method, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate comment
        with torch.no_grad():
            output_ids = model.generate(
                inputs["input_ids"],
                max_length=150,
                num_beams=4,
                early_stopping=True
            )
        
        comment = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        # Add the comment above the method in the original code
        commented_method = f"\n// {comment}\n{method}"
        commented_code = commented_code.replace(method, commented_method)
    
    return commented_code

# Streamlit UI
st.title("C++ Code Comment Generator")
st.write("Enter C++ code snippet to generate appropriate comments")

code_input = st.text_area("C++ Code", height=300, 
                          placeholder="Paste your C++ code here...")

if st.button("Generate Comments"):
    if code_input:
        with st.spinner("Generating comments..."):
            commented_code = generate_comments(code_input)
        
        st.subheader("Generated Comments:")
        st.code(commented_code, language="cpp")
    else:
        st.warning("Please enter some C++ code first.")
