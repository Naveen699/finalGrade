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

@app.route("/testRoute")
def testRoute():
	return "yes"


@app.route('/student_home')
def student_home():
	from userFunctions import studentFunctions
	if 'loggedin' in session:
		name = session.get('name', None)
		student_id = session.get('current_id', None)
		re = studentFunctions()
		re.updateUserGrades(student_id)
		account = re.findUserClasses(student_id)
		account1 = re.countUserClasses(student_id)
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
	if 'loggedin' in session:
		from userFunctions import studentFunctions
		class_name = request.args.get('class_name', None)
		student_id = session.get('current_id', None)
		re = studentFunctions()
		account = re.findUserAssignments(student_id, class_name)
		amount = len(account)
		return render_template('view_student_assignments.html', account=account, amount=amount)
	else:
		return url_for('login')

@app.route("/teacher_home")
def teacher_home():
	from userFunctions import teacherFunctions
	if 'loggedin' in session:
		teacher_id = session.get("current_id", None)
		re = teacherFunctions()
		data= re.returnAllClasses(teacher_id)
		return render_template('teacher_home.html', data=data)
	#return render_template("teacher_home.html")
	else:
		return redirect(url_for('teacher_login'))

@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
	from userFunctions import teacherFunctions
	re = teacherFunctions()
	teacher_id = session.get('current_id', None)
	amount = len(re.returnAllClasses(teacher_id))
	return render_template('add_assignment.html', account=re.returnAllClasses(teacher_id), amount = amount)

@app.route('/sumbitAddedAssignment', methods=['GET', 'POST'])
def sumbitAddedAssignment():
	from userFunctions import teacherFunctions
	re = teacherFunctions()
	classChoice = request.form['selected_value']
	assignment_name = request.form['assignmentName']
	due_date = request.form['dueDate']
	class_id = re.returnIdFromName(classChoice)
	re.addAssignment(classChoice, assignment_name, due_date, class_id['class_id'])

	return str(classChoice)

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



