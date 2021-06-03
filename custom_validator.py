from flask import flash

class CustomFieldsValidator:
    def __init__(self):
        pass

    def fields_validator(self, city_from, cities_to_received, depart_date, return_date, day_margin,
                         max_price, min_days, max_days):
        error = False
        if not max_price or max_price < 20:
            flash("Budget minimum €20")
            error = True
        if not isinstance(max_price, int):
            flash("Enter a number in your budget")
            error = True
        if not city_from[0]:
            flash("Enter city of departure")
            error = True
        if not cities_to_received[0]:
            flash("Enter at least one city of destination")
            error = True
        if not isinstance(max_days, int):
            flash("Enter max days of your trip")
            error = True
        if not isinstance(min_days, int):
            flash("Enter min days of your trip")
            error = True
        if not isinstance(day_margin, int):
            flash("Enter a margin of days for your search")
            error = True
        if self.check_dates(date=depart_date):
            flash("Enter a valid Depart Date with the following format: dd/mm/yy")
            error = True
        if self.check_dates(date=return_date):
            flash("Enter a valid Return Date with the following format: dd/mm/yy")
            error = True
        if error:
            return False
        else:
            return True

    def check_dates(self, date):
        days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        months =["01","02","03","04","05","06","07","08","09","10","11","12"]
        years=["21","22","23","24","25","26","27","28","29","30"]
        if date[2] != "/" or date[5] != "/":
            return True
        if date[:2] not in days:
            return True
        if date[3:5] not in months:
            return True
        if date[-2:] not in years:
            return True
        return False

