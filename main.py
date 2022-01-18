from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from models import db,InventoryModel
import csv
from io import StringIO
from flask import make_response
from forms import InventoryForm
from validate import Validate


 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'opentheapp'

db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def home():
   return render_template('main.html')

 
@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        form = InventoryForm()
        return render_template('createwtf.html', form=form)
 
    if request.method == 'POST':
        product_id = request.form['product_id']
        product = InventoryModel.query.filter_by(product_id=product_id).first()
        if product:
            return render_template("error_create.html",id = product)
        name = request.form['name']
        price = request.form['price']
        available_count = request.form['available_count']
        product = InventoryModel(product_id=product_id, name=name, price=price, available_count = available_count)
        valid = Validate().validate_product(product_id,name,price,available_count)
        if not valid:
            print(valid)
            return valid
        db.session.add(product)
        db.session.commit()
        return redirect('/data')
 
 
@app.route('/data')
def retrieve_list():
    products = InventoryModel.query.order_by(InventoryModel.product_id).all()
    return render_template('datalist.html',products = products)
 

 
@app.route('/data/view_id', methods = ['GET','POST'])
def get_product_id():
    if request.method == 'GET':
        form = InventoryForm()
        return render_template('getid.html',form=form)    
    if request.method == 'POST':
        id = request.form['product_id']
        return redirect(f'/data/{id}') 


@app.route('/data/<int:id>')
def retrieve_product(id):
    product = InventoryModel.query.filter_by(product_id=id).first()
    if product:
        return render_template('data.html', product = product)
    return render_template("error_list.html",id = product)


 
@app.route('/data/get_update_id', methods = ['GET','POST'])
def get_update_id():
    if request.method == 'GET':
        form = InventoryForm()
        return render_template('getid.html',form=form)     
    if request.method == 'POST':
        id = request.form['product_id']
        return redirect(f'/data/{id}/update')

@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    product = InventoryModel.query.filter_by(product_id=id).first()
    form = InventoryForm(obj=product)
    if not product:
        return render_template("error_list.html",id = id)

    if request.method == 'POST':
        if product:
            form.populate_obj(product)
            db.session.delete(product)
            db.session.commit()
            name = request.form['name']
            price = request.form['price']
            available_count = request.form['available_count']
            valid = Validate().validate_product(id,name,price,available_count)
            if not valid:
                print(valid)
                return valid
            product = InventoryModel(product_id=id, name=name, price=price, available_count = available_count)
            db.session.add(product)
            db.session.commit()
            return redirect(f'/data/{id}')
        return render_template("error_list.html",id = id)
 
    return render_template('updatewtf.html', form = form)
 
 
 
@app.route('/data/get_delete_id', methods = ['GET','POST'])
def get_delete_id():
    if request.method == 'GET':
        form = InventoryForm()
        return render_template('getid.html',form=form)      
    if request.method == 'POST':
        id = request.form['product_id']
        return redirect(f'/data/{id}/delete') 


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    product = InventoryModel.query.filter_by(product_id=id).first()
    if not product:
        return render_template("error_list.html",id = id)
    if request.method == 'POST':
        if product:
            db.session.delete(product)
            db.session.commit()
            return redirect('/data')
        else:
            return render_template("error_list.html",id = id)

 
    return render_template('delete.html',product = product)

@app.route('/data/getcsv/<int:id>', methods=['GET'])
def getcsv_id(id):
    product = InventoryModel.query.filter_by(product_id=id).first()
    si = StringIO()
    cw = csv.writer(si)
    header = InventoryModel.schema()
    cw.writerow(header)
    cw.writerow([product.product_id, product.name, product.price,product.available_count])
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=product-report-'+ str(product.product_id) +'.csv'
    response.headers["Content-type"] = "text/csv"
    return response    



@app.route('/data/getcsv', methods=['GET'])
def getcsv():
    si = StringIO()
    cw = csv.writer(si)
    header = InventoryModel.schema()
    cw.writerow(header)
    records = InventoryModel.query.order_by(InventoryModel.product_id).all()  
    cw.writerows([(r.product_id, r.name, r.price,r.available_count) for r in records])
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=all-products-report.csv'
    response.headers["Content-type"] = "text/csv"
    return response

@app.route('/data/export')
def export():
    return render_template('exportcsv.html')


app.run(host='localhost', port=5000)
