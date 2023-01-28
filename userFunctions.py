import app	
from app import mysql
import MySQLdb.cursors


class db:
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




