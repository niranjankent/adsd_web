#loading required libraries
from bottle import Bottle, request, template, redirect, static_file, response
import sqlite3

#creating web application 
app = Bottle()

#connecting to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#creating users and orders tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
               user_id TEXT PRIMARY KEY, 
               first_name TEXT, 
               last_name TEXT,
               email TEXT, 
               mobile_number INTEGER
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    product TEXT,
                    quantity INTEGER,
                    price_per_qty REAL,
                    total_price REAL
                )''')
conn.commit()



#creating API'S for CRUD operations and Search Engine

#creating homepage
@app.route('/')
def index():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    orders = {}
    for user in users:
        cursor.execute('SELECT * FROM orders WHERE user_id=?', (user[0],))
        user_orders = cursor.fetchall()
        orders[user[0]] = user_orders
    return template('views/index', users=users, orders=orders)

#retrieving user table
@app.route('/get_users')
def get_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return template('views/view_users', users=users)

#adding a new user
@app.route('/add_user')
def add_user():
    return template('views/add_user')

#saving a new user
@app.route('/save_user', method='POST')
def save_user():
    user_id = request.forms.get('user_id')
    first_name = request.forms.get('first_name')
    last_name = request.forms.get('last_name')
    email = request.forms.get('email')
    mobile_number = request.forms.get('mobile_number')
    cursor.execute('INSERT INTO users (user_id, first_name, last_name, email, mobile_number) VALUES (?, ?, ?, ?, ?)', 
                   (user_id, first_name, last_name, email, mobile_number))
    conn.commit()
    redirect('/')

#editing a existing user
@app.route('/edit_user/<user_id>')
def edit_user(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    user = cursor.fetchone()
    return template('views/edit_user', user=user)

#updating a existing user
@app.route('/update_user/<user_id>', method='POST')
def update_user(user_id):
    first_name = request.forms.get('first_name')
    last_name = request.forms.get('last_name')
    email = request.forms.get('email')
    mobile_number = request.forms.get('mobile_number')
    cursor.execute('UPDATE users SET first_name=?, last_name=?, email=?, mobile_number=? WHERE user_id=?', 
                   (first_name, last_name, email, mobile_number, user_id))
    conn.commit()
    redirect('/')
    
#deleting a existing user
@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    cursor.execute('DELETE FROM orders WHERE user_id=?', (user_id,))
    cursor.execute('DELETE FROM users WHERE user_id=?', (user_id,))
    conn.commit()
    redirect('/')




#getting orders table
@app.route('/get_orders')
def get_orders():
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    return template('views/view_orders', orders=orders)

#adding new order
@app.route('/add_order/<user_id>')
def add_order(user_id):
    return template('views/add_order', user_id=user_id)

#saving new order
@app.route('/save_order/<user_id>', method='POST')
def save_order(user_id):
    order_id = request.forms.get('order_id')
    user_id = request.forms.get('user_id')
    product = request.forms.get('product')
    quantity = int(request.forms.get('quantity'))
    price_per_qty = int(request.forms.get('price_per_qty'))
    total_price = int(request.forms.get('total_price'))
    cursor.execute('INSERT INTO orders (order_id, user_id, product, quantity, price_per_qty, total_price) VALUES (?, ?, ?, ?, ?, ?)',
                   (order_id, user_id, product, quantity, price_per_qty, total_price))
    conn.commit()
    redirect('/')

#editing existing order
@app.route('/edit_order/<order_id>')
def edit_order(order_id):
    cursor.execute('SELECT * FROM orders WHERE order_id=?', (order_id,))
    order = cursor.fetchone()
    return template('views/edit_order', order=order)

#updating existing order
@app.route('/update_order/<order_id>', method='POST')
def update_order(order_id):
    product = request.forms.get('product')
    quantity = int(request.forms.get('quantity'))
    price_per_qty = int(request.forms.get('price_per_qty'))
    total_price = int(request.forms.get('total_price'))
    cursor.execute('UPDATE orders SET product=?, quantity=?, price_per_qty=?, total_price=? WHERE order_id=?',
                    (product, quantity, price_per_qty, total_price, order_id))
    conn.commit()
    redirect('/')

#deleting existing order
@app.route('/delete_order/<order_id>')
def delete_order(order_id):
    cursor.execute('DELETE FROM orders WHERE order_id=?', (order_id,))
    conn.commit()
    redirect('/')

#searching users and their orders by using first name
@app.route('/search')
def search():
    search_term = request.query.get('search_term')
    cursor.execute('SELECT * FROM users WHERE first_name LIKE ?', ('%' + search_term + '%',))
    users = cursor.fetchall()
    orders = {}
    for user in users:
        cursor.execute('SELECT * FROM orders WHERE user_id=?', (user[0],))
        user_orders = cursor.fetchall()
        orders[user[0]] = user_orders
    return template('views/index', users=users, orders=orders)

@app.route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')

if __name__ == '__main__':
    app.run(debug=True)
