from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
import os
import json

class AddExpenseForm(FlaskForm):
    name = StringField('Expense Name', validators=[DataRequired(), Length(max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = SelectField('Category', choices=[('food', 'Food'), ('transportation', 'Transportation'), ('entertainment', 'Entertainment')], validators=[DataRequired()])
    expense_type = SelectField('Expense Type', choices=[('one-time', 'One-Time'), ('recurring', 'Recurring')], validators=[DataRequired()])
    bill_type = SelectField('Bill Type', choices=[('none', 'None'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class DeleteExpenseForm(FlaskForm):
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            expense_list = json.load(f)
    else:
        expense_list = []

    name = SelectField('Expense Name', choices=[(expense["name"], expense["name"]) for expense in expense_list], validators=[DataRequired()])
    submit = SubmitField('Delete Expense')