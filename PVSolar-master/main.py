from flask import Flask
from flask import request
from flask import render_template, url_for, jsonify
from models.database import Database
import json
import datetime
import dateutil.parser
from urllib.parse import quote, unquote
app = Flask(__name__)


@app.route('/')
def index():
    return view("index.html", name = "SolarPV")

""" @app.route('/Energy')
def energy():
    return view("Energy.html")

@app.route('/GetEnergyData/<userid>/<datestr>')
def get_energy_data(userid, datestr):
    date = dateutil.parser.parse(datestr)

    data = db.energy_detail(userid, date, date + datetime.timedelta(days = 1))
    
    return jsonify(result = data) """

@app.route('/Energy')
def energy():
    return view("Energy.html")

@app.route('/GetEnergyData/<userid>/<datestr>')
def get_energy_data(userid, datestr):
    print("start to get energy data")
    date = dateutil.parser.parse(datestr)
    db = Database()
    data = db.energy_detail(userid, date, date + datetime.timedelta(days = 1))
    
    return jsonify(result = data)
    

@app.route('/FeedInPrice')
def feedin_price():
    return view("FeedInPrice.html")

@app.route('/GetPriceData/<datestr>')
def get_price_data(datestr):
    date = dateutil.parser.parse(datestr)
    db = Database()
    data = db.price_detail(date, date + datetime.timedelta(days = 1))
    
    return jsonify(result = data)

@app.route('/DSP')
def dsp():
    return view("DSP.html")


@app.route("/Upload", methods = ["GET", "POST"])
def upload():
    print("Aaaaa")
    data : str = request.form.get("data", "")
    print('hhh')
    print(data)
    db = Database()
    db.upload(request.data)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
  
    
@app.route('/GetDSPData/<datestr>')
def get_dsp_data(datestr):
    date = dateutil.parser.parse(datestr)
    db = Database()
    data = db.dsp_detail(date, date + datetime.timedelta(days = 1))
    
    return jsonify(result = data)

@app.route('/Cost')
def cost():
    return view("Cost.html")

@app.route('/GetCostData/<userid>/<datestr>')
def get_cost_data(userid, datestr):

    print("start to get cost data")
    db = Database()
    date = dateutil.parser.parse(datestr)
    data = db.cost_detail(userid, date, date + datetime.timedelta(days = 1))
    print('ddd')
    
    return jsonify(result = data)

def view(page : str, **context) -> str:
    content = render_template(page, **context)

    return render_template("_Layout.html", content = content)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8000, debug = True)