from flask import Flask, render_template, request, redirect, url_for
from models import FoodItems, db
from datetime import datetime, timedelta
app = Flask(__name__)
db.create_all()
@app.route("/")
def index():
    ListOfFoodItems = db.query(FoodItems).filter_by(IsExpired=0, IsDeleted=0, IsRemoved=0).order_by(FoodItems.DatumPoteka.asc()).all()
    i, l = 0, len(ListOfFoodItems)
    while i < l:
        if ListOfFoodItems[i].DatumPoteka < datetime.now() - timedelta(days = 1):
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
    FoodItem = FoodItems(ImeZivila = request.form.get("FoodName"),
                         DatumVpisa = datetime.now(),
                         DatumPoteka = datetime.strptime(request.form.get("ExpirationDate"), '%Y-%m-%d'),
                         IsExpired = 0,
                         IsDeleted = 0,
                         IsRemoved = 0)
    db.add(FoodItem)
    db.commit()
    return redirect(url_for("AddFood"))

@app.route("/DeleteFoodItem", methods = ["GET","POST"])
def DeletedFoodItem():
    FoodItemID = request.form.get("FoodItemID")
    FoodItem = db.query(FoodItems).get(FoodItemID)
    FoodItem.IsDeleted = 1
    db.commit()
    return redirect(url_for("index"))

@app.route("/UrejanjePoteklih")
def ExpiredFood():
    ListOfExpiredOrDeletedFoodItems = db.query(FoodItems).filter_by(IsExpired = 0, IsDeleted = 1, IsRemoved = 0).order_by(FoodItems.DatumPoteka.asc()).all()
    i, l = 0, len(ListOfExpiredOrDeletedFoodItems)
    while i < l:
        if ListOfExpiredOrDeletedFoodItems[i].DatumPoteka < datetime.now() - timedelta(days = 1):
            el = ListOfExpiredOrDeletedFoodItems.pop(i)
            el.IsExpired = 1
            db.commit()
            l -= 1
            i -= 1
        i += 1
    return render_template("ExpiredFood.html", ListOfExpiredOrDeletedFoodItems = ListOfExpiredOrDeletedFoodItems,
                           CurrentDate0 = datetime.now() + timedelta(days = 2),
                           CurrentDate1 = datetime.now() + timedelta(days = 5),
                           CurrentDate2 = datetime.now() + timedelta(days = 10))

@app.route("/DeleteOrRestoreFoodItem", methods = ["GET","POST"])
def DeleteOrRestoreFoodItem():
    FoodItem = db.query(FoodItems).get(request.form.get("FoodItemID"))
    if request.form["SubmitButton"] == "X":
        FoodItem.IsRemoved = 1
    else:
        FoodItem.IsDeleted = 0
    db.commit()
    return redirect(url_for("ExpiredFood"))

if __name__ == '__main__':
    app.run()