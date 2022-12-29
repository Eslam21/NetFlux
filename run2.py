from flask import Flask, render_template, json 
 
app2 = Flask(__name__,template_folder="Front-End/templates") 
 
 
@app2.route('/') 
def index2(): 
    return render_template('Java_script.html') 
 

@app2.route('/api/<name>/') 
def api_get_name(name): 
    return json.jsonify({ 
        'name': name 
    }) 
 
if __name__ == '__main__': 
    app2.run(debug=True) 
