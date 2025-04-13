from flask import Blueprint,request
from src.java.app_java import generate_comments_java

java_ep = Blueprint("java_ep",__name__)


@java_ep.route("/java")
def get_java_code():
    code_snippet = request.args.get("code")
    return generate_comments_java(code_snippet)