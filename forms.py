from itertools import product
from tokenize import Double
from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField,FloatField, DecimalField)

from wtforms.validators import InputRequired, Length,ValidationError


class InventoryForm(FlaskForm):
    product_id = IntegerField('Product_Id', validators=[InputRequired("Int type required"),Length(min=1, max=100)])
    name = StringField('Name', validators=[InputRequired("Text type required"), Length(min=1,max=200)])
    price =  DecimalField('Price', validators=[InputRequired("Float type required")])
    available_count = IntegerField('Available Count', validators=[InputRequired("Int type required")])