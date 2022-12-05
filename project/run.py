from flask import Flask, render_template
app = Flask(__name__, static_folder='static')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/registration")
def registration():
    return render_template('registration.html')


if __name__ == "__main__":
    app.run(debug=True) 