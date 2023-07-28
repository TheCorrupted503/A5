from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_renfroc"
app.config["MYSQL_PASSWORD"] = "DHSwrestler11294!!"
app.config["MYSQL_DB"] = "cs340_renfroc"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/employee', methods=['GET','POST'])
def employee_page():
    if request.method == 'GET':
        employee_query = "SELECT employee_id AS 'Employee ID',first_name AS 'First Name', last_name AS 'Last Name', email_address AS 'Email', Job_Title.job_title AS 'Job Title', Shift_Name.shift_type AS 'Shift Type', Shift_Days.shift_days_names AS 'Shift Days' \
FROM Employee \
INNER JOIN Job_Title ON Employee.job_title_id = Job_Title.job_title_id \
INNER JOIN Shift ON Employee.shift_id = Shift.shift_id \
INNER JOIN Shift_Name ON Shift.shift_name_id = Shift_Name.shift_name_id \
INNER JOIN Shift_Days ON Shift.shift_days_id = Shift_Days.shift_days_id \
ORDER BY last_name,first_name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(employee_query)
        employee_table = cur.fetchall()

        job_title_query = "SELECT job_title AS Job_Title, job_title_id \
FROM Job_Title \
ORDER BY job_title;"
        cur = mysql.connection.cursor()
        cur.execute(job_title_query)
        job_title_table = cur.fetchall()
        
        
        shift_query = "SELECT shift_id, CONCAT(shift_type,': ',shift_days_names) AS Shift \
FROM Shift \
INNER JOIN Shift_Name ON Shift.shift_name_id = Shift_Name.shift_name_id \
INNER JOIN Shift_Days ON Shift.shift_days_id = Shift_Days.shift_days_id \
ORDER BY shift_type ASC;"

        cur = mysql.connection.cursor()
        cur.execute(shift_query)
        shift_table = cur.fetchall()

        return render_template('employee.html', employee_table=employee_table, job_title_table=job_title_table, shift_table=shift_table)
    
    if request.method == 'POST':
        if request.form.get("Create"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email_address = request.form["email_address"]
            job_title_id = request.form["job_title_id"]
            shift_id = request.form["shift_id"]

            cur = mysql.connection.cursor()

            employee_add_query = "INSERT INTO Employee (first_name, last_name, email_address, job_title_id, shift_id) VALUES (%s, %s, %s, %s, %s);"
            employee_add_query2 = "DELETE FROM Employee \
WHERE employee_id NOT IN( \
SELECT MIN(employee_id) \
FROM Employee \
GROUP BY first_name, last_name, email_address);"
            cur.execute(employee_add_query, (first_name, last_name, email_address, job_title_id, shift_id))
            cur.execute(employee_add_query2)
            mysql.connection.commit()

            return redirect('/employee')


@app.route('/job_title', methods=['GET','POST'])
def job_title_page():
    if request.method == 'GET':
        job_title_query = "SELECT job_title_id AS 'Job Title ID',job_title AS 'Job Title', job_description AS 'Job Description' \
FROM Job_Title \
ORDER BY job_title ASC;"
        cur = mysql.connection.cursor()
        cur.execute(job_title_query)
        job_title_table = cur.fetchall()
        
        return render_template('job_title.html', job_title_table=job_title_table)

    if request.method == 'POST':
        if request.form.get("Create"):
            job_title = request.form["job_title"]
            job_description = request.form["job_description"]

            cur = mysql.connection.cursor()

            job_title_add_query = "INSERT INTO Job_Title (job_title, job_description) VALUES (%s, %s);"
            job_title_add_query2 = "DELETE FROM Job_Title \
WHERE job_title_id NOT IN( \
SELECT MIN(job_title_id) \
FROM Job_Title \
GROUP BY job_title, job_description);"
            cur.execute(job_title_add_query, (job_title, job_description))
            cur.execute(job_title_add_query2)
            mysql.connection.commit()

            return redirect('/job_title')

@app.route('/certification',  methods=['GET','POST'])
def certification_page():
    if request.method == 'GET':
        certification_query = "SELECT cert_id AS 'Certification ID',cert_name AS 'Certification', cert_description AS 'Certification Description' \
FROM Certification \
ORDER BY cert_name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(certification_query)
        certification_table = cur.fetchall()
        
        return render_template('certification.html', certification_table=certification_table)

    if request.method == 'POST':
        if request.form.get("Create"):
            cert_name = request.form["cert_name"]
            cert_description = request.form["cert_description"]

            cur = mysql.connection.cursor()

            certification_add_query = "INSERT INTO Certification (cert_name, cert_description) VALUES (%s, %s);"
            certification_add_query2 = "DELETE FROM Certification \
WHERE cert_id NOT IN( \
SELECT MIN(cert_id) \
FROM Certification \
GROUP BY cert_name, cert_description);"
            cur.execute(certification_add_query, (cert_name, cert_description))
            cur.execute(certification_add_query2)
            mysql.connection.commit()

            return redirect('/certification')

@app.route('/employee_certification', methods=['POST', 'GET'])
def employee_certification_page():
    if request.method == 'GET':
        query = "SELECT CONCAT(first_name,' ',last_name) AS Employee, cert_name AS Certification \
FROM Employee_has_Certification \
INNER JOIN Employee ON Employee_has_Certification.employee_id = Employee.employee_id \
INNER JOIN Certification ON Employee_has_Certification.cert_id = Certification.cert_id \
ORDER BY last_name, first_name ASC;"
        
        cur = mysql.connection.cursor()
        cur.execute(query)
        read = cur.fetchall()

        
        
        query2 = "SELECT CONCAT(first_name,' ',last_name) AS Employee_Name, Employee.employee_id \
FROM Employee \
WHERE Employee.employee_id NOT IN (\
    SELECT employee_id FROM Employee_has_Certification) \
ORDER BY last_name, first_name ASC;"
   

        cur = mysql.connection.cursor()
        cur.execute(query2)
        employee_name = cur.fetchall()

        query3 = "SELECT cert_name AS Certification_Name, cert_id \
FROM Certification \
ORDER BY cert_name;"

        cur = mysql.connection.cursor()
        cur.execute(query3)
        cert_name = cur.fetchall()

        return render_template('employee_certification.html', read=read, employee_name=employee_name, cert_name=cert_name)

    if request.method == "POST":

        if request.form.get("Create"):
            employee = request.form["employee"]
            cert = request.form["cert"]
            
            query = "INSERT INTO Employee_has_Certification (employee_id, cert_id) VALUES (%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (employee, cert))
            mysql.connection.commit()

        if request.form.get("Update"):
            employee = request.form["employee"]
            cert = request.form["cert"]
            
            
            query = "UPDATE Employee_has_Certification \
SET cert_id = %s \
WHERE employee_id = (\
    SELECT employee_id \
    FROM Employee \
    WHERE CONCAT(first_name,' ',last_name) = %s);"
          
            
            cur = mysql.connection.cursor()
            cur.execute(query, (cert, employee))
            mysql.connection.commit()

        if request.form.get("Delete"):
            employee = request.form["employee"]
            query = "DELETE FROM Employee_has_Certification \
WHERE employee_id IN (\
SELECT Employee.employee_id \
FROM Employee_has_Certification \
INNER JOIN Employee ON Employee_has_Certification.employee_id = Employee.employee_id \
WHERE (CONCAT(first_name,' ',last_name) = %s));"
            cur = mysql.connection.cursor()
            cur.execute(query, (employee,))
            mysql.connection.commit()

        return redirect('/employee_certification')


@app.route('/shift', methods=['GET', 'POST'])
def shift_page():
    if request.method == 'GET':

        query2 = "SELECT shift_id, shift_type AS 'Shift Type', shift_days_names AS 'Shift Days' \
FROM Shift \
INNER JOIN Shift_Name ON Shift.shift_name_id = Shift_Name.shift_name_id \
INNER JOIN Shift_Days ON Shift.shift_days_id = Shift_Days.shift_days_id \
ORDER BY shift_id ASC;"

        cur = mysql.connection.cursor()
        cur.execute(query2)
        shift_table = cur.fetchall()


        
        
        query2 = "SELECT shift_type AS 'Shift Type', shift_name_id \
FROM Shift_Name \
ORDER BY shift_type ASC;"
   

        cur = mysql.connection.cursor()
        cur.execute(query2)
        shift_name_table = cur.fetchall()

        query3 = "SELECT shift_days_names AS 'Shift Days', shift_days_id \
FROM Shift_Days \
ORDER BY shift_days_names ASC;"

        cur = mysql.connection.cursor()
        cur.execute(query3)
        shift_days_table = cur.fetchall()

        return render_template('shift.html', shift_table=shift_table, shift_name_table=shift_name_table, shift_days_table=shift_days_table)

    if request.method == "POST":

        if request.form.get("Create"):
            shift_name_id = request.form["shift_name_id"]
            shift_days_id = request.form["shift_days_id"]

            cur = mysql.connection.cursor()
            
            query = "INSERT INTO Shift (shift_name_id, shift_days_id) VALUES (%s, %s);"
            query2 = "DELETE FROM Shift \
WHERE shift_id NOT IN( \
SELECT MIN(shift_id) \
FROM Shift \
INNER JOIN Shift_Name ON Shift.shift_name_id = Shift_Name.shift_name_id \
INNER JOIN Shift_Days ON Shift.shift_days_id = Shift_Days.shift_days_id \
GROUP BY shift_type, shift_days_names);"
            cur.execute(query,(shift_name_id, shift_days_id))
            cur.execute(query2)
            mysql.connection.commit()

            return redirect('/shift')

@app.route('/shift_days', methods=['GET', 'POST'])
def shift_days_page():
    if request.method == 'GET':
        shift_days_names_query = "SELECT shift_days_id AS 'Shift Days ID',shift_days_names AS 'Shift Days Names' \
FROM Shift_Days \
ORDER BY shift_days_names ASC;"
        cur = mysql.connection.cursor()
        cur.execute(shift_days_names_query)
        shift_days_names_table = cur.fetchall()
        
        return render_template('shift_days.html', shift_days_names_table=shift_days_names_table)

    if request.method == 'POST':
        if request.form.get("Create"):
            shift_days_names = request.form["shift_days_names"]

            cur = mysql.connection.cursor()

            shift_days_names_add_query = "INSERT INTO Shift_Days (shift_days_names) VALUE (%s);"
            shift_days_names_add_query2 = "DELETE FROM Shift_Days \
WHERE shift_days_id NOT IN( \
SELECT MIN(shift_days_id) \
FROM Shift_Days \
GROUP BY shift_days_names);"
            cur.execute(shift_days_names_add_query, (shift_days_names,))
            cur.execute(shift_days_names_add_query2)
            mysql.connection.commit()

            return redirect('/shift_days')

@app.route('/shift_names', methods=['POST', 'GET'])
def shift_name_page():
    if request.method == 'GET':
        shift_type_query = "SELECT shift_name_id AS 'Shift Name ID',shift_type AS 'Shift Type' \
FROM Shift_Name \
ORDER BY shift_type ASC;"
        cur = mysql.connection.cursor()
        cur.execute(shift_type_query)
        shift_type_table = cur.fetchall()
        
        return render_template('shift_names.html', shift_type_table=shift_type_table)

    if request.method == 'POST':
        if request.form.get("Create"):
            shift_type = request.form["shift_type"]

            cur = mysql.connection.cursor()

            shift_type_add_query = "INSERT INTO Shift_Name (shift_type) VALUE (%s);"
            shift_type_add_query2 = "DELETE FROM Shift_Name \
WHERE shift_name_id NOT IN( \
SELECT MIN(shift_name_id) \
FROM Shift_Name \
GROUP BY shift_type);"
            cur.execute(shift_type_add_query, (shift_type,))
            cur.execute(shift_type_add_query2)
            mysql.connection.commit()

            return redirect('/shift_names')

if __name__ == "__main__":
    app.run(port=46780, debug=True)