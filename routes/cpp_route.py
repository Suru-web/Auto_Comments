from flask import Blueprint,request, jsonify
from src.cpp.app_cpp import generate_comments_cpp

cpp_ep = Blueprint("cpp_ep",__name__)


@cpp_ep.route("/cpp")
def get_java_code():
    code_snippet = request.args.get("code")
    return jsonify({"commented_code":generate_comments_cpp(code_snippet)})