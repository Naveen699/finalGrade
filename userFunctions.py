import app	
from app import mysql
import MySQLdb.cursors


class studentFunctions:
	def __init__(self):
		self.cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		self.updateConnection = MySQLdb.connect("us-cdbr-east-06.cleardb.net", "b3b957a90e179c", "695f9180", "heroku_3d330f55efec1ed")

	def findUserClasses(self, student_id):
		self.cursor.execute(r"SELECT classes.class_name, teachers.first_name, teachers.last_name, student_classes.grade FROM classes JOIN teachers ON classes.teacher_id = teachers.teacher_id JOIN student_classes ON classes.class_id = student_classes.class_id WHERE student_classes.student_id = '{}';".format(student_id))
		return self.cursor.fetchall()

	def findUserAssignments(self, student_id, class_name):
		self.cursor.execute(r"SELECT assignments.assignment_name, assignments.due_date, student_assignments.grade FROM assignments JOIN student_assignments ON assignments.assignment_id = student_assignments.assignment_id JOIN classes ON assignments.class_id = classes.class_id WHERE classes.class_name = '{}' AND student_assignments.student_id = '{}';".format(class_name, student_id))
		return self.cursor.fetchall()

	def returnClassId(self, class_name):
		self.cursor.execute(r"SELECT class_id FROM classes WHERE class_name='{}'".format(class_name))
		account = self.cursor.fetchone()
		return account['class_id']

	def countUserClasses(self, student_id):
		self.cursor.execute(r"SELECT COUNT(*) FROM student_classes WHERE student_id ={}".format(student_id))
		account1 = self.cursor.fetchone()
		return int(account1['COUNT(*)'])
	

	def testUpdate(self, student_id, class_id, updateValue):
		confirmExecute = self.updateConnection.cursor()
		confirmExecute.execute(r"UPDATE student_classes SET grade = '{}' WHERE student_id = '{}' AND class_id = '{}'".format(updateValue, student_id, class_id))
		self.updateConnection.commit()
		return "Update successful"

	def updateUserGrades(self, student_id):
		avg = 0
		for k in self.findUserClasses(student_id):
			for i in range(0, len(self.findUserAssignments(student_id, str(k['class_name'])))):
				account = self.findUserAssignments(student_id, str(k['class_name']))
				avg += account[i]['grade']
			if (avg>0):
				avg = avg / len(self.findUserAssignments(student_id, str(k['class_name'])))
				#Average found
				#Commit average to sql database 
				#UPDATE student_classes VALUUES (grade = avg) WHERE student_id = student_id, class_id = str(k['class_name'])
				self.testUpdate(student_id, str(self.returnClassId(str(k['class_name']))), avg)
			else:
				#Finds Average if 0 assignments
				avg = 0
				self.testUpdate(student_id, str(self.returnClassId(str(k['class_name']))), avg)

			#Resets Average
			avg = 0

class teacherFunctions:
	def __init__(self):
		self.cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		self.updateConnection = MySQLdb.connect("us-cdbr-east-06.cleardb.net", "b3b957a90e179c", "695f9180", "heroku_3d330f55efec1ed")


	def returnAllClasses(self, teacher_id):
		self.cursor.execute("SELECT * FROM classes WHERE teacher_id = '{}'".format(teacher_id))
		return self.cursor.fetchall()

	def returnIdFromName(self, class_name):
		self.cursor.execute(r"SELECT class_id FROM classes WHERE class_name='{}'".format(class_name))
		return self.cursor.fetchone()

	def returnNameFromId(self, class_id):
		self.cursor.execute(r"SELECT class_name FROM classes WHERE class_id='{}'".format(class_id))
		return self.cursor.fetchone()

	
	def returnStudentsInClass(self, class_id):
		# return all students in specific class
		self.cursor.execute(r"SELECT students.* FROM students JOIN student_classes ON students.student_id = student_classes.student_id WHERE student_classes.class_id = '{}';".format(class_id))
		return self.cursor.fetchall()
		
	
	def returnStudentsFromTeacher(self, teacher_id):
		# return all students in specific class
		self.cursor.execute(r"SELECT students.student_id, students.first_name, students.last_name, student_classes.class_id FROM students JOIN student_classes ON students.student_id = student_classes.student_id JOIN classes ON student_classes.class_id = classes.class_id WHERE classes.teacher_id = '{}';".format(teacher_id))
		return self.cursor.fetchall()

	def addAssignment(self, class_name,  assignment_name, due_date, class_id):
		# Add assignment logic, apply to all students in class
		class_id = self.returnIdFromName(class_name)
		confirmExecute = self.updateConnection.cursor()
		confirmExecute.execute(r"INSERT INTO assignments (assignment_id, class_id, assignment_name, due_date) SELECT MAX(assignment_id) + 1, '{}', '{}', '{}' FROM assignments;".format(class_id['class_id'], assignment_name, due_date))
		self.updateConnection.commit()

	
		return None



















