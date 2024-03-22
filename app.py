from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'shogunmode69'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
 msg = ''
 if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
  username = request.form['username']
  password = request.form['password']
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('SELECT * FROM accounts1 WHERE username = % s AND password = % s', (username, password))
  account = cursor.fetchone()
  type=account['type']
 
  if account:
    session['loggedin'] = True
    session['username'] = account['username']
    msg = 'Logged in successfully !'
    if type=='admin':
      cursor=mysql.connection.cursor()
      cursor.execute("SELECT * FROM accounts1")
      account_data=cursor.fetchall()
      cursor.execute("SELECT * FROM store")
      store_data=cursor.fetchall()
      return render_template('admin.html',account_data=account_data,store_data=store_data)
    else:
      return render_template('user.html')
  
 return render_template('login.html', msg = msg)

# @app.route('/logout')
# def logout():
#  session.pop('loggedin', None)
#  session.pop('id', None)
#  session.pop('username', None)
#  return redirect(url_for('login'))

@app.route('/register', methods =['GET','POST'])
def register():
 msg = ''
 if request.method == 'POST' and 'username' in request.form  and 'password' in request.form and 'email' in request.form:
  username = request.form['username']
  password = request.form['password']
  email = request.form['email']
  
  type='user'
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('SELECT * FROM accounts1 WHERE username = % s', (username, ))
  account = cursor.fetchone()
  if account:
   msg = 'Account already exists !'
  elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
   msg='invalid email address'
  elif not re.match(r'[A-Za-z0-9]+', username):
   msg = 'username must contain only characters and numbers !'
  elif not username or not password or not email:
    msg = 'Please fill out the form !'
  else:
   cursor.execute('INSERT INTO accounts1 VALUES ( % s, % s, % s, % s)', (username, password,email,type))
   mysql.connection.commit()
   msg = 'You have successfully registered !'
   return render_template('login.html')
 elif request.method == 'POST':
  msg = 'Please fill out the form !'
 return render_template('register.html', msg = msg)

@app.route('/admin',methods=['GET','POST'])
def admin():
  storename = request.form['storename']
  owner = request.form['owner']
  product = request.form['product']
  place = request.form['place']
  phoneno = request.form['phoneno']
  address = request.form['address']
  productname = request.form['productname']
  cursor=mysql.connection.cursor()
  cursor.execute("INSERT INTO store VALUES ( % s, % s, % s, % s,% s, % s, % s)", (storename,owner,product,place,phoneno,address,productname,))
  mysql.connection.commit()
  cursor=mysql.connection.cursor()
  cursor.execute("SELECT * FROM accounts1")
  account_data=cursor.fetchall()
  cursor.execute("SELECT * FROM store")
  store_data=cursor.fetchall()
  return render_template('admin.html',account_data=account_data,store_data=store_data)
@app.route('/back')
def back():
  return redirect('admin.html')
@app.route('/user')
def user():
  
  return render_template('user.html')
@app.route('/fd')
def fd():
  return render_template('feedback.html')

@app.route('/feedback',methods=['GET','POST'])
def feedback():
  Name = request.form['Name']
  Email = request.form['Email']
  Message = request.form['Message']
  cursor=mysql.connection.cursor()
  cursor.execute('INSERT INTO feedback VALUES ( % s, % s, % s)', (Name,Email,Message,))
  mysql.connection.commit()
  return render_template('user.html')

@app.route('/Feedbackdetails')
def Feedbackdetails():
  cursor=mysql.connection.cursor()
  cursor.execute("SELECT * FROM feedback")
  feed_data=cursor.fetchall()
  return render_template('Feedbackdetails.html',feed_data=feed_data)

@app.route('/AboutUs')
def AboutUs():
  return render_template('AboutUs.html')

@app.route('/FruitsCatgory')
def FruitsCatgory():
  return render_template('FruitsCatgory.html')
@app.route('/BestDeals')
def BestDeals():
  return render_template('BestDeals.html')
@app.route('/MedicineCategory')
def MedicineCategory():
  return render_template('MedicineCategory.html')
@app.route('/BabyCare')
def BabyCare():
  return render_template('BabyCare.html')
@app.route('/OfficeCategory')
def OfficeCategory():
  return render_template('OfficeCategory.html')
@app.route('/BeautyCategory')
def BeautyCategory():
  return render_template('BeautyCategory.html')
@app.route('/Gardening')
def Gardening():
  return render_template('Gardening.html')

#@app.route('/ContactFormCSS')
#def ContactFormCSS():
  #return render_template('ContactFormCSS.html')
@app.route('/detailscheckout')
def detailscheckout():
  return render_template('DetailsCheckout.html')
@app.route('/cart',methods=['POST'])
def cart():
  productname=request.form['name']
  price=request.form['price']
  quantity=request.form['quantity']
  cursor=mysql.connection.cursor()
  cursor.execute('INSERT INTO cart VALUES ( % s, % s, % s)', (productname,price,quantity,))
  mysql.connection.commit()
  return render_template('user.html')
@app.route('/store',methods=['POST'])
def store():
  cursor=mysql.connection.cursor()
  cursor.execute("INSERT INTO store VALUES ( % s, % s, % s, % s,% s, % s)", (storename,owner,product,place,phoneno,address,))
  mysql.connection.commit()
@app.route('/st',methods=['POST'])
def st():
  product=request.form['te1']
  
  place=request.form['s1']


  cursor=mysql.connection.cursor()
  cursor.execute('SELECT * FROM store WHERE product=%s and place=%s',(product,place))
  data=cursor.fetchall()
  return render_template('view.html',data=data)
@app.route('/sear',methods=['POST'])
def sear():
  productname=request.form['search']
  cursor=mysql.connection.cursor()
  cursor.execute('SELECT * FROM category WHERE productname=%s',[productname])
  data=cursor.fetchall()
  
  if data:
    d1=data[0][0]
    cursor.execute('SELECT * FROM store WHERE product=%s',[d1])
    data1=cursor.fetchall()
    return render_template('searchview.html',data1=data1,data=data)
  else:
    
    return render_template('error.html')
@app.route('/pricedetails')
def pricedetails():
  cursor=mysql.connection.cursor()
  cursor.execute("SELECT * FROM category")
  data=cursor.fetchall()
  return render_template('pricedetails.html',data=data)
@app.route('/priceadder')
def priceadder():
  
  return render_template('priceadder.html')
@app.route('/price',methods=['POST'])
def price():
  product = request.form['product']
  productname = request.form['productname']
  price = request.form['price']
  cursor=mysql.connection.cursor()
  cursor.execute('INSERT INTO category VALUES ( % s, % s, % s)', (product,productname,price,))
  mysql.connection.commit()
  return redirect('pricedetails')
@app.route('/priceup')
def priceup():
  cursor=mysql.connection.cursor()
  cursor.execute('SELECT * FROM category')
  data=cursor.fetchall()
  
  
  return render_template('priceupdate.html',data=data)
@app.route('/priceupdater',methods=['POST'])
def priceupdater():
  productname=request.form['s1']
  price=request.form['p1']
  cursor=mysql.connection.cursor()

  cursor.execute('UPDATE  category SET price=(%s) WHERE productname=(%s)',(price,productname,))
  mysql.connection.commit()  

  return redirect('pricedetails')
#@app.route('/admin',methods=['GET','POST'])
#def admin():
  #cursor=mysql.connection.cursor()
  #cursor.execute("SELECT * FROM accounts1")
  #data=cursor.fetchall()
  #print(type(data[0]))
  #return render_template('admin.html',data=data)
  
@app.route('/storeadder')
def storeadder():
  return render_template('storeadder.html')




if __name__=="__main__":
  app.run(debug=True)