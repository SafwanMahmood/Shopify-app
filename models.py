from cgitb import text
from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class InventoryModel(db.Model):
    __tablename__ = "inventory_table"
 
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    available_count = db.Column(db.Integer())
    
    def validate_product(self,product_id,name,price,available_count):
        if not isinstance(product_id,(int)):
            return ValueError("Product Id: Int expected")
        if not isinstance(name,(str)):
            return ValueError("Name: Str/text expected")    
        if not isinstance(price,(int,float)):
            return ValueError("Price: Int/float expected")
        if not isinstance(available_count,(int)):
            return ValueError("Availablity Count: Int expected")
        return True
    def schema():
        return ['product_id','name','price','available_count']
 
    def __init__(self, product_id,name,price,available_count):
        valid = self.validate_product(product_id,name,price,available_count)
        if not valid:
            print(valid)
            return valid
        self.product_id = product_id
        self.name = name
        self.price = price
        self.available_count = available_count
 
    def __repr__(self):
        return f"{self.name}:{self.product_id}"

    