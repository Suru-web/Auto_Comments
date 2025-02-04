import streamlit as st
import torch
import ast
from transformers import AutoTokenizer, T5ForConditionalGeneration

model_path = "/Users/surajmeharwade/Projects/Auto_Comments/model/trained-code-comment-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

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
    output = []

    for node in tree.body:
        try:
            node_code = ast.unparse(node)  # Convert AST node back into code
            comment = generate_comment(node_code)  # Generate a comment for each statement
            output.append(comment)
        except Exception as e:
            output.append(f"# [Error processing] {str(e)}\n{ast.dump(node)}")  # Handle any errors gracefully

    return "\n\n".join(output)  # Join the commented code for display


st.set_page_config(page_title="Python Code Comment Generator", layout="wide")
st.title("💬 Python Code Comment Generator")
st.write("Enter a Python code snippet, and the AI will generate a comment for it.")

code_input = st.text_area("📝 Paste your Python code here:", height=200)

if st.button("Generate Comment"):
    if code_input.strip():
        with st.spinner("Generating comment... ⏳"):
            comment = split_code(code_input)
        st.success("✅ Comment Generated!")
        st.code(comment, language="python")
    else:
        st.warning("⚠️ Please enter some Python code.")