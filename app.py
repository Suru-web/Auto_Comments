import streamlit as st
import torch
import ast
from transformers import AutoTokenizer, T5ForConditionalGeneration

# Load the trained model and tokenizer
model_path = "/Users/surajmeharwade/Projects/Auto_Comments/model/trained-code-comment-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Use MPS if available (for Mac)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

# Function to generate comments
def generate_comment(code_snippet, max_length=64):
    input_ids = tokenizer(
        code_snippet.strip(),
        return_tensors="pt",
        max_length=256,
        truncation=True,
        padding="max_length"
    ).input_ids.to(device)

    with torch.no_grad():
        output_ids = model.generate(input_ids, max_length=max_length, num_return_sequences=1)

    comment = "# " + tokenizer.decode(output_ids[0], skip_special_tokens=True) + "\n" + code_snippet
    return comment

def split_code(code_snippet):
    tree = ast.parse(code_snippet)  # Parse the code into an AST
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]  # Extract function nodes

    output = []
    for func in functions:
        func_code = ast.unparse(func)  # Convert the AST function node back into code
        comment = generate_comment(func_code)  # Generate a comment for the function
        output.append(comment)

    return "\n\n".join(output)  # Join the commented functions for display
# Streamlit UI
st.set_page_config(page_title="Python Code Comment Generator", layout="wide")
st.title("💬 Python Code Comment Generator")
st.write("Enter a Python code snippet, and the AI will generate a comment for it.")

# Text area for input
code_input = st.text_area("📝 Paste your Python code here:", height=200)

# Generate button
if st.button("Generate Comment"):
    if code_input.strip():
        with st.spinner("Generating comment... ⏳"):
            comment = split_code(code_input)
        st.success("✅ Comment Generated!")
        st.code(comment, language="python")
    else:
        st.warning("⚠️ Please enter some Python code.")