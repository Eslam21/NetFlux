from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    user = {'firstname': 'Harry', 'lastname': 'Potter', "Age":[18,27,33,88,5]}
    x = 10
    return render_template("Java_script.html", user= user , x = type(x))


if __name__ == '__main__':
    app.run(debug=True)