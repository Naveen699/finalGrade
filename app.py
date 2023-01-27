from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'b3b957a90e179c'
app.config['MYSQL_PASSWORD'] = '695f9180'
app.config['MYSQL_DB'] = 'heroku_3d330f55efec1ed'

mysql = MySQL(app)


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = ("SELECT * FROM students WHERE first_name = %s AND studentPassword = %s")
        values = (name, password)
        cursor.execute(sql, values)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['current_id'] = account['student_id']
            session['name'] = name
            session['password'] = password
            return redirect(url_for('student_home'))

    return render_template('login.html')

@app.route('/student_home')
def student_home():
	if 'loggedin' in session:
		name = session.get('name', None)
		student_id = session.get('current_id', None)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(r"SELECT classes.class_name, teachers.first_name, teachers.last_name, student_classes.grade FROM classes JOIN teachers ON classes.teacher_id = teachers.teacher_id JOIN student_classes ON classes.class_id = student_classes.class_id WHERE student_classes.student_id = '{}';".format(student_id))
		account = cursor.fetchall()
		cursor.execute(r"SELECT COUNT(*) FROM student_classes WHERE student_id ={}".format(student_id))
		account1 = cursor.fetchone()
		account1 = int(account1['COUNT(*)'])
		return render_template('student_home.html', name = name, account = account, account1 = account1)
	else:
		return redirect(url_for('login'))


@app.route("/teacher_login", methods=['GET', 'POST'])
def teacher_login():
	if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
		name = request.form['name']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		sql = ("SELECT * FROM teachers WHERE first_name = %s AND password = %s")
		values = (name, password)
		cursor.execute(sql, values)
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			return redirect(url_for('teacher_home'))


	return render_template('teacher_login.html')

@app.route('/view_student_assignments')
def view_student_assignments():
	class_name = request.args.get('class_name', None)
	student_id = session.get('current_id', None)
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(r"SELECT assignments.assignment_name, assignments.due_date, student_assignments.grade FROM assignments JOIN student_assignments ON assignments.assignment_id = student_assignments.assignment_id JOIN classes ON assignments.class_id = classes.class_id WHERE classes.class_name = '{}' AND student_assignments.student_id = '{}';".format(class_name, student_id))
	account = cursor.fetchall()
	amount = len(account)

	return render_template('view_student_assignments.html', account=account, amount=amount)

@app.route("/teacher_home")
def teacher_home():
	if 'loggedin' in session:
		return render_template('teacher_home.html')
	#return render_template("teacher_home.html")
	else:
		return redirect(url_for('teacher_login'))

@app.route('/teacher')


@app.route('/profile')
def profile():
	name = session.get('name', None)
	password = session.get('password', None)
	return render_template("profile.html", name = name, password = password)
	


@app.route('/logout')
def logout():
	session.pop('name', None)
	session.pop('loggedin', None)
	return redirect(url_for('login'))

# @app.route('/home')
# def home():
# 	if 'loogedin' in session:
# 		return 'home'
# 	else:
# 		return redirect(url_for('login'))




