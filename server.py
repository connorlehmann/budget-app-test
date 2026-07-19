from datetime import datetime, timedelta
import json
from flask import Flask, render_template, redirect, url_for
from forms import AddExpenseForm, DeleteExpenseForm
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'eZbOFITfJVsEj?#9'

@app.route("/")
@app.route("/home")
def home():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            expense_list = json.load(f)
    else:
        expense_list = []

    total_spent = float(sum(expense["price"] for expense in expense_list))

    return render_template('Home.html', expenses=expense_list, total_spent=total_spent)

@app.route("/addexpense", methods=['GET', 'POST'])
def addexpense():
    form = AddExpenseForm()

    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            expense_list = json.load(f)
    else:
        expense_list = []

    if form.validate_on_submit():
        name = form.name.data
        price = float(form.price.data)
        category = form.category.data
        expense_type = form.expense_type.data
        bill_type = form.bill_type.data
        
        date = datetime.now().strftime("%m/%d/%Y")

        item = {"name" : name,
                "price" : price,
                "category" : category,
                "expense_type" : expense_type,
                "bill_type": bill_type,
                "date" : date
        }
        
        expense_list.append(item)

        with open("data.json", "w") as f:
            json.dump(expense_list, f)

        return redirect(url_for('home'))

    return render_template('AddExpense.html', title='Regular', form=form)

@app.route("/deleteexpense", methods=['GET', 'POST'])
def deleteexpense():
    form = DeleteExpenseForm()

    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            expense_list = json.load(f)
    else:
        expense_list = []

    form.name.choices = [(expense["name"], expense["name"]) for expense in expense_list]

    if form.validate_on_submit():
        name = form.name.data
        expense_list = [expense for expense in expense_list if expense["name"] != name]

        with open("data.json", "w") as f:
            json.dump(expense_list, f)

        return redirect(url_for('home'))

    return render_template('DeleteExpense.html', title='Regular', form=form)

@app.route("/nextbill", methods=['GET', 'POST'])
def nextbill():

    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            expense_list = json.load(f)
    else:
        expense_list = []

    billed_expenses = [expense for expense in expense_list if expense["bill_type"] in ["monthly", "yearly"]]

    potential_bills = []

    for item in billed_expenses:
        base_date = datetime.strptime(item["date"], "%m/%d/%Y")
        if item["bill_type"] == "monthly":
            next_date = base_date + timedelta(days=30)
        if item["bill_type"] == "yearly":
            next_date = base_date + timedelta(days=365)
        
        while next_date < datetime.now():
            if item["bill_type"] == "monthly":
                next_date += timedelta(days=30)
            elif item["bill_type"] == "yearly":
                next_date += timedelta(days=365)
        
        potential_bills.append((item["name"], next_date.strftime("%m/%d/%Y")))
            

    return render_template('NextBill.html', title='Regular', potential_bills=potential_bills)


if __name__ == "__main__":
    app.run(debug=True)
