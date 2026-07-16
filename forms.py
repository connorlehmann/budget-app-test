from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ExpenseForm(FlaskForm):
    name = StringField('Expense Name', validators=[DataRequired(), Length(max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = StringField('Category', validators=[DataRequired(), Length(max=50)])
    expense_type = StringField('Expense Type', validators=[DataRequired(), Length(max=50)])
    bill_type = StringField('Bill Type', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Expense')