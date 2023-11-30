import csv
import mysql.connector

class data_controller:
    def __init__(self):
        self.database_name = "recognice_db"
    
    def create_database(self):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Define the SQL query
        sql = "CREATE DATABASE IF NOT EXISTS {}".format(self.database_name)

        cursor.execute(sql)
        
        print("Database created successfully.")
        
        # Commit the changes and close the connection
        cursor.close()
        conn.close()
        
    def create_tables(self):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="recognice_db"
        )
        
        # Create a cursor object
        cursor = conn.cursor()

        # Execute the SQL code to create the tables
        sql = """
        CREATE TABLE IF NOT EXISTS students (
            student_number INT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            middle_initial VARCHAR(255),
            section VARCHAR(20),
            birthday DATE,
            age INT,
            gender VARCHAR(255),
            contact_no VARCHAR(255),
            student_email VARCHAR(255)
        );
        """
        cursor.execute(sql)
        
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255),
            user_email VARCHAR(255),
            user_password VARCHAR(255)
        );
        """
        cursor.execute(sql)
        
        sql = """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            student_number INT,
            attendance_date DATE,
            face_attendance VARCHAR(255),
            face_attendance_time TIME,
            barcode_attendance VARCHAR(255),
            barcode_attendance_time TIME,
            attendance_status VARCHAR(255),
            FOREIGN KEY (student_number) REFERENCES students(student_number)
        );
        """
        cursor.execute(sql)
         
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        print("tables created")

    def get_student_table_info(self, students):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )

        cursor = conn.cursor()
        
        students_list = []
        for student in students:
            sql = "SELECT count(attendance_status) FROM attendance WHERE student_number = %s AND attendance_status = %s"
            cursor.execute(sql, (student[0], "Present"))
            present = cursor.fetchone()
            
            sql = "SELECT count(attendance_status) FROM attendance WHERE student_number = %s AND attendance_status = %s"
            cursor.execute(sql, (student[0], "Absent"))
            absent = cursor.fetchone()
            
            list = [present[0], absent[0]]
            
            new_student = student + tuple(list)
            students_list.append(new_student)
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
            
        return students_list
    
    def get_students(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )

        cursor = conn.cursor()

        sql = "SELECT student_number, CONCAT(first_name, ' ', middle_initial, '. ', last_name) as Name FROM students WHERE section = 'BSCS-3A'"
        cursor.execute(sql)
        students = cursor.fetchall()
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        return students
   
    
    def write_face_attendance(self, value):
        with open('attendance.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(value)
            
    
    
