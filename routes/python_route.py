from flask import Blueprint, request
from src.python.app_python import split_code_python

python_ep = Blueprint("python_ep",__name__)

@python_ep.route("/python")
def get_python_code():
    code_snippet = request.args.get("code")
    return split_code_python(code_snippet)