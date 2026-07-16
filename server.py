import json
from flask import Flask, render_template
from forms import ExpenseForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'eZbOFITfJVsEj?#9'

@app.route("/")
@app.route("/home")
def home():
    with open("data.json", "r") as file:
        expenses = json.load(file)

    total_spent = sum(expense["price"] for expense in expenses)

    return render_template('Home.html', expenses=expenses, total_spent=total_spent)

@app.route("/addexpense")
def addexpense():
    form = ExpenseForm()
    return render_template('AddExpense.html')

if __name__ == "__main__":
    app.run(debug=True)
