from flask import Flask, render_template, request, redirect, url_for
from models import FoodItems, db
from datetime import datetime, timedelta
app = Flask(__name__)
db.create_all()
@app.route("/")
def index():
    ListOfFoodItems = db.query(FoodItems).filter_by(IsExpired=0, IsRemoved=0).filter(FoodItems.Kolicina > 0).order_by(FoodItems.DatumPoteka.asc()).all()
    i, l = 0, len(ListOfFoodItems)
    while i < l:
        if ListOfFoodItems[i].DatumPoteka and ListOfFoodItems[i].DatumPoteka < datetime.now() - timedelta(days = 1):
            el = ListOfFoodItems.pop(i)
            el.IsExpired = 1
            db.commit()
            l -= 1
            i -= 1
        i += 1
    return render_template("index.html", ListOfFoodItems = ListOfFoodItems,
                           CurrentDate0 = datetime.now() + timedelta(days=2),
                           CurrentDate1 = datetime.now() + timedelta(days = 5),
                           CurrentDate2 = datetime.now() + timedelta(days = 10))

@app.route("/DodajZivila")
def AddFood():
    return render_template("AddFood.html")

@app.route("/AddedFoodItem", methods = ["GET", "POST"])
def AddedFoodItem():
    DatumPoteka = request.form.get("ExpirationDate")
    if not DatumPoteka:
        DatumPoteka = None
    else:
        DatumPoteka = datetime.strptime(DatumPoteka, '%Y-%m-%d')
    FoodItem = FoodItems(ImeZivila = request.form.get("FoodName"),
                         DatumVpisa = datetime.now(),
                         DatumPoteka = DatumPoteka,
                         Kolicina = request.form.get("Quantity"),
                         IsExpired = 0,
                         IsRemoved = 0)
    db.add(FoodItem)
    db.commit()
    return redirect(url_for("AddFood"))

@app.route("/AddDeleteFoodItem", methods = ["GET","POST"])
def AddDeleteFoodItem():
    FoodItem = db.query(FoodItems).get(request.form.get("FoodItemID"))
    if request.form["SubmitButton"] == "+":
        FoodItem.Kolicina += 1
    else:
        FoodItem.Kolicina -= 1
    db.commit()
    return redirect(url_for("index"))

@app.route("/UrejanjePoteklih")
def DeletedFood():
    ListOfDeletedFoodItems = db.query(FoodItems).filter_by(IsExpired = 0, IsRemoved = 0, Kolicina = 0).order_by(FoodItems.DatumPoteka.asc()).all()
    i, l = 0, len(ListOfDeletedFoodItems)
    while i < l:
        if ListOfDeletedFoodItems[i].DatumPoteka and ListOfDeletedFoodItems[i].DatumPoteka < datetime.now() - timedelta(days = 1):
            el = ListOfDeletedFoodItems.pop(i)
            el.IsExpired = 1
            db.commit()
            l -= 1
            i -= 1
        i += 1
    return render_template("ExpiredFood.html", ListOfDeletedFoodItems = ListOfDeletedFoodItems,
                           CurrentDate0 = datetime.now() + timedelta(days = 2),
                           CurrentDate1 = datetime.now() + timedelta(days = 5),
                           CurrentDate2 = datetime.now() + timedelta(days = 10))

@app.route("/DeleteOrRestoreFoodItem", methods = ["GET","POST"])
def DeleteOrRestoreFoodItem():
    FoodItem = db.query(FoodItems).get(request.form.get("FoodItemID"))
    if request.form["SubmitButton"] == "X":
        FoodItem.IsRemoved = 1
    else:
        FoodItem.Kolicina += 1
    db.commit()
    return redirect(url_for("DeletedFood"))

if __name__ == '__main__':
    app.run()