from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def hello_world():

    xValues = ["Italy", "France", "Spain", "USA", "Argentina","Mystical"]
    yValues = [55, 49, 44, 24, 15,100]
    barColors = ["red", "green","blue","orange","brown","purple"]
    return render_template("visualize.html", xValues=xValues,yValues=yValues,barColors=barColors)


if __name__ == '__main__':
    app.run(debug=True)