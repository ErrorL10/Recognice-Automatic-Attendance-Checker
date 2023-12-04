import csv
from datetime import date
import mysql.connector

class data_controller:
    def __init__(self):
        self.database_name = "recognice_db"
        self.today = date.today()
        
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
            section_id INT,
            birthday DATE,
            age INT,
            gender VARCHAR(255),
            contact_no VARCHAR(255),
            student_email VARCHAR(255)
        );
        """
        cursor.execute(sql)
        
        sql ="""
        CREATE TABLE IF NOT EXISTS sections (
        section_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        section_name VARCHAR(20) NOT NULL
        );"""
        
        cursor.execute(sql)
        
        sql = """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            student_number INT,
            section_id INT,
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

    def get_sections(self):
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="recognice_db"
        )
        cursor = conn.cursor()
        
        sql = "SELECT * FROM sections"
        cursor.execute(sql)
        sections = cursor.fetchall()
        
         # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        return sections
     
    def get_students(self, section):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )

        cursor = conn.cursor()

        sql = "SELECT student_number, CONCAT(first_name, ' ', middle_initial, ' ', last_name) as Name, section_id FROM students WHERE section_id = %s"
        cursor.execute(sql, (self.get_section_id(section),))
        students = cursor.fetchall()
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        return students  
    
    def get_section_table_info(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )

        cursor = conn.cursor()
        
        sections = self.get_sections()

        sections_info = []
        for section in sections:
            sql = "SELECT COUNT(*) from students WHERE section_id = %s"
            cursor.execute(sql, (section[0],))
            count = cursor.fetchone()
            
            date_today = self.today.strftime("%Y/%m/%d")
            
            sql = "SELECT count(attendance_status) from attendance WHERE section_id = %s AND attendance_date = %s AND attendance_status = %s"
            cursor.execute(sql, (section[0], date_today, "Present"))
            present = cursor.fetchone()
            
            sql = "SELECT count(attendance_status) from attendance WHERE section_id = %s AND attendance_date = %s AND attendance_status = %s"
            cursor.execute(sql, (section[0], date_today, "Absent"))
            absent = cursor.fetchone()
            
            sections_info.append((section[1], count[0], present[0] if present[0] > 0 else "Not Checked", absent[0] if absent[0] > 0 else "Not Checked"))
            
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        return sections_info
    
    def get_section_id(self, section):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )

        cursor = conn.cursor()
        
        sql = "SELECT section_id from sections WHERE section_name = %s"
        cursor.execute(sql, [section])
        section_id = cursor.fetchone()
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        try:
            return section_id[0]
        except TypeError:
            return 0
    
    def get_dates(self, section):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )

        cursor = conn.cursor()
        
        sql = "SELECT DISTINCT attendance_date from attendance WHERE section_id = %s"
        cursor.execute(sql, [self.get_section_id(section)])
        dates = cursor.fetchall()
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        new_dates = [date.strftime(i[0], '%Y/%m/%d') for i in dates]
        
        return new_dates
        
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
            
            new_student = (student[0], student[1], present, absent)
            students_list.append(new_student)
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
            
        return students_list
    
    def get_report_table_info(self, students, date):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )

        cursor = conn.cursor(buffered=True)
        
        students_list = []
        for student in students:
            sql = "SELECT attendance_status FROM attendance WHERE student_number = %s AND section_id = %s AND attendance_date = %s"
            cursor.execute(sql, (student[0], 1, date))
            
            present = cursor.fetchone()
            
            new_student = (student[0], student[1], present[0])
            students_list.append(new_student)
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
            
        return students_list
     
    def get_student_info(self, student_number):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )
        
        cursor = conn.cursor()
        
        sql = "SELECT * FROM students WHERE student_number = %s"
        cursor.execute(sql, (student_number, ))
        student_info = cursor.fetchone()
        
        return student_info
    
    def insert_attendance(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )
        
        cursor = conn.cursor()
        
        with open('attendance.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            
            for row in reader:
                sql = "INSERT INTO attendance (student_number, section_id, attendance_date, face_attendance, face_attendance_time, barcode_attendance, barcode_attendance_time, attendance_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
                print("row inserted")

            # Commit the changes and close the connection
            conn.commit()
            cursor.close()
            conn.close()
    
    def find_section(self, value):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )
        cursor = conn.cursor(buffered=True)
        
        sql = "SELECT section_name FROM sections WHERE section_name = %s"
        cursor.execute(sql, (value,))
        
        data = cursor.fetchone()
        
         # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        if not data:
            return False
        else:
            return True
        
    def add_section(self, value):
        print("Value:", value)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )
        cursor = conn.cursor()
        
        sql = "INSERT INTO sections (section_name) VALUES (%s)"
        cursor.execute(sql, (value,))
        print("section added")
        
         # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()    
         
    def add_student(self, values):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )
        cursor = conn.cursor()
        
        sql = "INSERT INTO students (student_number, first_name, last_name, middle_initial, section_id, birthday, age, gender, contact_no, student_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9]))
        print("student added")
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()    
         
    def update_student(self, values):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database_name
        )
        cursor = conn.cursor()
        
        sql = "UPDATE students SET first_name = %s, last_name = %s, middle_initial = %s, section_id = %s, birthday = %s, age = %s, gender = %s, contact_no = %s, student_email = %s WHERE student_number = %s"
        cursor.execute(sql, (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9]))
        print("student updated")
        
        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()    
        
    
    
    def fill_attendance(self, section):
        students_list = self.get_students(section)
        
        today = date.today()
        date_today = date.strftime(today, "%Y/%m/%d")
        
        data = []
        for row in students_list:
            data_row = [row[0], row[1], row[2], date_today, 0, "N/A", 0, "N/A", "Absent"]
            data.append(data_row)
            
        if self.attendance_is_empty():

            with open('attendance.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        else:
            print("no")
    
    def attendance_is_empty(self):
        with open('attendance.csv', "r") as file:
            reader = csv.reader(file)
            old_data = list(reader)
        
        return len(old_data) == 0
            
            
    def reset_attendance(self):
        with open('attendance.csv', 'w') as file:
            file.write('')
            
    def write_face_attendance(self, value):
        with open('attendance.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(value)
    
    def write_barcode_attendance(self, value):
        # Write the updated data back to the CSV file
        with open('attendance.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(value)
    
    
    
