import app	
from app import mysql
import MySQLdb.cursors


class db:
	def __init__(self):
		self.cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

	def findUserClasses(self, student_id):
		self.cursor.execute(r"SELECT classes.class_name, teachers.first_name, teachers.last_name, student_classes.grade FROM classes JOIN teachers ON classes.teacher_id = teachers.teacher_id JOIN student_classes ON classes.class_id = student_classes.class_id WHERE student_classes.student_id = '{}';".format(student_id))
		return self.cursor.fetchall()

	def findUserAssignments(self, student_id):
		self.cursor.execute(r"SELECT assignments.assignment_name, assignments.due_date, student_assignments.grade FROM assignments JOIN student_assignments ON assignments.assignment_id = student_assignments.assignment_id JOIN classes ON assignments.class_id = classes.class_id WHERE classes.class_name = '{}' AND student_assignments.student_id = '{}';".format(class_name, student_id))
		return self.cursor.fetchall()

	def countUserClasses(self, student_id):
		self.cursor.execute(r"SELECT COUNT(*) FROM student_classes WHERE student_id ={}".format(student_id))
		account1 = self.cursor.fetchone()
		return int(account1['COUNT(*)'])

	def calculateUserGrade(self, hw, test):
		return None