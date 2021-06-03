from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from datetime import date, datetime, timedelta
from flight_search import FlightSearch
from flight_data import FlightData
from custom_validator import CustomFieldsValidator


app = Flask(__name__)
app.config['SECRET_KEY'] = "pepe"
Bootstrap(app)

fs = FlightSearch()
fd = FlightData()
cfv = CustomFieldsValidator()

@app.route("/", methods=["GET", "POST"])
def home():

    return render_template("index.html")



@app.route("/prices", methods=["GET", "POST"])
def check_routes():

    max_price = int(request.form["max_price"])
    city_from = [request.form["from"]]
    cities_to_received = request.form["to"].split(",")
    cities_to = [city.strip() for city in cities_to_received]
    depart_date = request.form["depart"][:2] + "/" + request.form["depart"][3:5] + "/20" + request.form["depart"][-2:]
    return_date = request.form["return"][:2] + "/" + request.form["return"][3:5] + "/20" + request.form["return"][-2:]
    day_margin = int(request.form["margin"])
    min_days = int(request.form["min_days"])
    max_days = int(request.form["max_days"])

    if cfv.fields_validator(city_from=city_from, cities_to_received=cities_to_received, depart_date=depart_date,
                            return_date=return_date,day_margin=day_margin,max_price=max_price,
                            min_days=min_days,max_days=max_days):
        print(city_from, cities_to, depart_date, return_date, day_margin)
        from_city_code = fs.check_IATA_code(city_from)
        to_city_codes = fs.check_IATA_code(cities_to)
        results =[]
        for city_code in to_city_codes:
            flight = fs.check_flights(city_from=from_city_code[0][0], city_to=city_code[0], max_price=max_price, date_from=depart_date, date_to=return_date, min_days=min_days, max_days=max_days)
            results.append([city_code[1],flight])

        final_data = fd.arrange_data(results)

        return render_template('deals.html', city_from=city_from[0].title(), final_data=final_data, not_found=fs.not_found)
    else:
        return render_template("index.html")


@app.context_processor
def inject_today_date():
    return {'today_date': date.today().strftime("%Y"),
            'plus_7_days': (date.today()+ timedelta(days=7)).strftime("%d/%m/%y"),
            'plus_187_days': (date.today() + timedelta(days=187)).strftime("%d/%m/%y")}


if __name__ == '__main__':
    app.run(debug=True)