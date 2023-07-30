#Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from PIL import Image

#Initialize the Flask Application
app = Flask(__name__)

#Configure Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='heartattack2023',
        database='School'
    )
    return conn

#Define routes
#Route to handle the form submission for adding a new student
@app.route('/add_student', methods = ['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']
        enrollment_date = request.form['enrollment_date']
        profile_picture = request.files['profile_picture']


        #save the image
        profile_picture_path = 'static/images/' + profile_picture.filename
        profile_picture.save(profile_picture_path)

        #Get profile picture filename to be stored in the database
        profile_picture_filename = profile_picture.filename


        #Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        #Insert the new student into the database
        insert_query = "INSERT INTO Students (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, EnrollmentDate, ProfilePicture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (first_name, last_name, date_of_birth, gender,email, phone_number, address, enrollment_date, profile_picture_filename ))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('add_student.html')


#Add route to serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)


#Route to displaya list of Students
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    conn.close()

    return render_template('index.html', students=students)

#Route to display students profiles
@app.route('/student/<int:student_id>')
def student_profile(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the student information from the database
    query = "SELECT * FROM Students WHERE StudentID = %s"
    cursor.execute(query, (student_id,))
    student = cursor.fetchone()
    conn.close()

    if student:
        return render_template('student_profile.html', student=student)
    else:
        return "Student not found."
    
#Route to delete a student profile
@app.route('/student/delete/<int:student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    #Send delete request to the database
    query = "DELETE FROM Students WHERE StudentID = %s"
    cursor.execute(query, (student_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))
    

#Route to serve a json file- This end point can be integrated by any front-end application - React.js of Vue.js or a mobile app
@app.route('/students', methods = ['GET', 'POST'])
def students():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Retrieve the student information from the database
    query = "SELECT * FROM Students"
    cursor.execute(query)
    student = cursor.fetchall()
    conn.close()

    return jsonify(student)




#Run the Flask App
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5002)