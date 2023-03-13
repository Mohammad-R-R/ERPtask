from flask import Flask, render_template, request, url_for
from models import db, Product, Location, ProductMovement
from flask import redirect
import datetime
import secrets
from flask import flash




app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Products
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    
    if request.method == 'POST':
        product_id = request.form['product_id']
        Check_id = Product.query.filter_by(product_id=product_id).first()
        if Check_id :
            flash("this Id is already exist","error")
            return redirect(url_for('add_product'))
        product = Product(product_id=product_id)
        if not product_id:
            flash("fill the input","error")
            return redirect(url_for('add_product'))
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('add_product.html')



@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if request.method == 'POST':
        new_product_id = request.form['product_id']
        if new_product_id == '':
            flash('Please fill in the product ID.')
            return redirect(url_for('edit_product', product_id=product_id))
        if new_product_id != product_id:
            if Product.query.filter_by(product_id=new_product_id).first():
                flash('The product ID '+new_product_id+' already exists.')
                return redirect(url_for('edit_product', product_id=product_id))
            product.product_id = new_product_id
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('edit_product.html', product=product)


@app.route('/view_product/<product_id>')
def view_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    return render_template('view_product.html', product=product)

# Locations
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        check_location = Location.query.filter_by(location_id= location_id).first()
        if check_location:
            flash("This location is already exist")
            return redirect(url_for('add_location'))
        location = Location(location_id=location_id)
        if not location_id:
            flash("Location feild is empty fill it ")
            return redirect(url_for('add_location'))
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('locations'))
    return render_template('add_location.html')

@app.route('/edit_location/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    locations = Location.query.filter_by(location_id=location_id).first()
    if request.method == 'POST':
        new_location_id = request.form['location_id']
        if new_location_id == '':
            flash('Please fill in the Location ID.')
            return redirect(url_for('edit_location',location_id=location_id))

        if  new_location_id != location_id:
            flash('The Location ID '+new_location_id+' already exists.')
            return redirect(url_for('edit_location', location_id=location_id))
        db.session.commit()
        return redirect(url_for('locations'))
    return render_template('edit_location.html', location=locations)


@app.route('/view_location/<location_id>')
def view_location(location_id):
    location = Location.query.filter_by(location_id= location_id).first()
    return render_template('view_location.html',l= location)



@app.route('/add_product_movement', methods=['GET', 'POST'])
def add_product_movement():
    if request.method == 'POST':
        movement_id = request.form.get('movement_id')
        check_movment = ProductMovement.query.filter_by(movement_id=movement_id).first()
        if check_movment:
            flash("this movemnt already done")
            return redirect(url_for('add_product_movement'))
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        if from_location == to_location:
            flash("can't move from "+from_location+" to "+to_location)
            return redirect(url_for('add_product_movement'))
        product_id = request.form.get('product_id')
        qty = request.form.get('qty')

        # Validate input
        if not movement_id or not from_location or not to_location or not product_id or not qty:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('add_product_movement'))

        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except ValueError:
            flash('Invalid quantity', 'error')
            return redirect(url_for('add_product_movement'))

        # Add product movement to database
        product_movement = ProductMovement(movement_id=movement_id, from_location=from_location,
                                           to_location=to_location, product_id=product_id, qty=qty)
        db.session.add(product_movement)
        db.session.commit()

        flash('Product movement added successfully', 'success')
        return redirect(url_for('product_movements'))

    products = Product.query.all()
    locations = Location.query.all()
    return render_template('add_product_movement.html', products=products, locations=locations)

@app.route('/product_movements')
def product_movements():
    product_movements = ProductMovement.query.all()
    return render_template('product_movements.html', product_movements=product_movements)



@app.route('/edit_product_movement/<movement_id>', methods=['GET', 'POST'])
def edit_product_movement(movement_id):
    product_movement = ProductMovement.query.filter_by(movement_id=movement_id).first()
    if request.method == 'POST':
        pre= product_movement.movement_id
        product_movement.movement_id= request.form['movement_id']
        product_movement.from_location = request.form['from_location']
        product_movement.to_location = request.form['to_location']
        product_movement.product_id = request.form['product_id']
        product_movement.qty = request.form['qty']

        if not product_movement.movement_id or not product_movement.from_location or not product_movement.to_location or not product_movement.product_id or not product_movement.qty:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('edit_product_movement',movment_id=pre))

        try:
            # qty = int(qty)
            if int(product_movement.qty) <= 0:
                raise ValueError
        except ValueError:
            flash('Invalid quantity', 'error')
            return redirect(url_for('add_product_movement'))
        db.session.commit()
        return redirect(url_for('product_movements'))
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('edit_product_movement.html', product_movement=product_movement, product=products, products=products, locations=locations)


@app.route('/view_product_movement/<movement_id>')
def view_product_movement(movement_id):
    product_movement = ProductMovement.query.filter_by(movement_id=movement_id).first()
    return render_template('view_product_movement.html', product_movement=product_movement)




@app.route('/report', methods=['GET'])
def view_report():
    locations = Location.query.all()
    products = Product.query.all()

    data = []
    for product in products:
        for location in locations:
            movements = ProductMovement.query.filter_by(product_id=product.product_id, to_location=location.location_id).all()
            total_in = sum(m.qty for m in movements)
            movements = ProductMovement.query.filter_by(product_id=product.product_id, from_location=location.location_id).all()
            total_out = sum(m.qty for m in movements)
            balance = total_in - total_out
            data.append((product.product_id, location.location_id, balance))

    return render_template('report.html', data=data)


@app.route('/delete_product/<product_id>')
def delete(product_id):
    product= Product.query.filter_by(product_id=product_id).first()
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('products')) 
if __name__ == '__main__':
    app.run(debug=True)



    