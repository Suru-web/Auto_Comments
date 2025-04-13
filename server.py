from flask import Flask
from routes.main_route import main
from routes.python_route import python_ep
from routes.cpp_route import cpp_ep
from routes.java_route import java_ep

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(python_ep)
app.register_blueprint(cpp_ep)
app.register_blueprint(java_ep)

if __name__ == "__main__":
    app.run(debug=True)