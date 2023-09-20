# This is the convenor's python file which consists of the following user stories:
# - Update report status
# - Complete report as a convenor
# - Complete report as a supervisor
# - Manage supervisors and students in the department

# Initial setup
from flask import Blueprint, render_template, request, url_for, redirect
import re
from datetime import datetime, date
import mysql.connector
from mysql.connector import FieldType
import connect

app_convenor = Blueprint('app_convenor', __name__)

# DB connection
dbconn = None
connection = None


def getCursor():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect.dbuser,
                                             password=connect.dbpass, host=connect.dbhost,
                                             database=connect.dbname, autocommit=True)
        dbconn = connection.cursor()
        return dbconn
    else:
        if connection.is_connected():
            return dbconn
        else:
            connection = None
            dbconn = None
            return getCursor()


# for show a list for all students' info for a convenor's  department (Wanjun wang/Vic)
@app_convenor.route('/convenor/students', methods=['GET', 'POST'])
def students():
    active = 'con_student'  # For the left nav bar become active
    if request.method == 'GET':
        # to get department name to identify students under the department of a respecive convener
        connection = getCursor()
        user_email = request.cookies.get('user_email')
        connection.execute(
            "SELECT department_id FROM user where email_address =%s;", (user_email,))
        result = connection.fetchall()
        department_id = result[0][0]
        connection.execute(
            "SELECT department_name FROM department where department_id=%s;", (department_id,))
        result = connection.fetchall()
        department_name = result[0][0]
        connection.execute(
            "SELECT user_id FROM user where email_address =%s;", (user_email,))
        result = connection.fetchall()
        user_id = result[0][0]

# figure out whether convener is supervisor as this column attribute is in the supervisor table. if it is there is no row in supervisor table by user ID of convener, it means convener is not supervisor
        connection.execute(
            "SELECT is_convenor FROM supervisor where user_id =%s;", (user_id,))
        result = connection.fetchall()

        if result == []:
            connection.reset()
            connection = getCursor()
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                          FROM student AS s
                          LEFT JOIN 
                          ( SELECT
                           student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                          LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                          LEFT JOIN user AS u ON u.user_id = s.user_id where u.department_id=%s;""", (department_id,))
            select_result = connection.fetchall()

            return render_template("/convenor/student_list_departm.html", select_result=select_result, active=active)

        else:
            is_convenor = result[0][0]
            connection.execute(
                "SELECT supervisor_id FROM supervisor where user_id =%s;", (user_id,))
            result = connection.fetchall()
            supervisor_id = result[0][0]

            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                          FROM student AS s
                          LEFT JOIN 
                          ( SELECT
                           student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                          LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                          LEFT JOIN user AS u ON u.user_id = s.user_id where (u.department_id=%s and s.student_id not in (SELECT student_id FROM student_supervisor where supervisor_id=%s) or
                           (u.department_id=%s and r.report_progress_id<>%s));""", (department_id, supervisor_id, department_id, 3))
            select_result = connection.fetchall()
            return render_template("/convenor/student_list_departm.html", select_result=select_result, active=active)

    else:
        message = 'begin'
        alertStyling = 'begin'
        search = request.form.get('search')
        if search == '':
            search = '%%'
        else:
            search = "%" + search + "%"

        connection = getCursor()
        user_email = request.cookies.get('user_email')
        connection.execute(
            "SELECT department_id FROM user where email_address =%s;", (user_email,))
        result = connection.fetchall()
        department_id = result[0][0]

        connection.execute(
            "SELECT department_name FROM department where department_id=%s;", (department_id,))
        result = connection.fetchall()
        department_name = result[0][0]

        connection.execute(
            "SELECT user_id FROM user where email_address =%s;", (user_email,))
        result = connection.fetchall()
        user_id = result[0][0]

# figure out whether convener is supervisor as this column attribute is in the supervisor table. if it is there is no row in supervisor table by user ID of convener, it means convener is not supervisor
        connection.execute(
            "SELECT is_convenor FROM supervisor where user_id =%s;", (user_id,))
        result = connection.fetchall()
        if result == []:
            connection.reset()
            connection = getCursor()
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                          FROM student AS s
                          LEFT JOIN 
                          ( SELECT
                           student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                          LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                          LEFT JOIN user AS u ON u.user_id = s.user_id where u.department_id=%s and CONCAT(s.first_name, ' ', s.last_name) like %s;'""", (department_id, search))
            select_result = connection.fetchall()
            if select_result == []:
                message = "Student is not found. Please try again!"
                alertStyling = "Red"
            else:
                message = "Students are found."
                alertStyling = "Green"

            return render_template("/convenor/student_list_departm.html", select_result=select_result, message=message, alertStyling=alertStyling, active=active)

        else:
            is_convenor = result[0][0]
            connection.execute(
                "SELECT supervisor_id FROM supervisor where user_id =%s;", (user_id,))
            result = connection.fetchall()
            supervisor_id = result[0][0]
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                          FROM student AS s
                          LEFT JOIN 
                          ( SELECT
                           student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                          LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                          LEFT JOIN user AS u ON u.user_id = s.user_id where (u.department_id=%s and s.student_id not in (SELECT student_id FROM student_supervisor where supervisor_id=%s) 
                          and CONCAT(s.first_name, ' ', s.last_name) like %s) or
                           (u.department_id=%s and r.report_progress_id<>%s and CONCAT(s.first_name, ' ', s.last_name) like %s );""", (department_id, supervisor_id, search, department_id, 3, search))

            select_result = connection.fetchall()
            if select_result == []:
                message = "Student is not found. Please try again!"
                alertStyling = "Red"
            else:
                message = "Students are found."
                alertStyling = "Green"
            return render_template("/convenor/student_list_departm.html", select_result=select_result, message=message, alertStyling=alertStyling, active=active)

# Filter report progress in students' list


@app_convenor.route('/convenor/filter_report_progress', methods=['POST'])
def student_detail_filter1():
    active = 'con_student'  # For the left nav bar become active
    message = 'begin'
    alertStyling = 'begin'
    report_progress = request.form.get("report_progress")

    connection = getCursor()
    user_email = request.cookies.get('user_email')
    connection.execute(
        "SELECT department_id FROM user where email_address =%s;", (user_email,))
    result = connection.fetchall()
    department_id = result[0][0]

    connection.execute(
        "SELECT department_name FROM department where department_id=%s;", (department_id,))
    result = connection.fetchall()
    department_name = result[0][0]

    connection.execute(
        "SELECT user_id FROM user where email_address =%s;", (user_email,))
    result = connection.fetchall()
    user_id = result[0][0]

    connection.execute(
        "SELECT is_convenor FROM supervisor where user_id =%s;", (user_id,))
    result = connection.fetchall()

    connection.reset()

    if result == []:

        # if report_progress equal to "None", it means the report has not been started by students and report_progress attribute in
        # database sql queyies should be assigned the value 'null' to select those reports as part of filer function
        if report_progress == 'None':
            connection.reset()
            connection = getCursor()
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                          FROM student AS s
                          LEFT JOIN 
                          ( SELECT
                           student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                          LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                          LEFT JOIN user AS u ON u.user_id = s.user_id where u.department_id=%s and r.report_progress_id is null;""", (department_id,))
            select_result = connection.fetchall()
            if select_result == []:
                message = "reprot is not found. Please try again!"
                alertStyling = "Red"
            else:
                message = "reports are found."
                alertStyling = "Green"

            return render_template("/convenor/student_list_departm.html", select_result=select_result, message=message, alertStyling=alertStyling, sort_re_progress=report_progress, active=active)

        else:
            connection.reset()
            connection = getCursor()
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                                FROM student AS s
                                LEFT JOIN 
                                ( SELECT
                                student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                                LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                                LEFT JOIN user AS u ON u.user_id = s.user_id where u.department_id=%s and r.report_progress_id=%s;""", (department_id, report_progress))
            select_result = connection.fetchall()
            if select_result == []:
                message = "report is not found. Please try again!"
                alertStyling = "Red"
            else:
                message = "reports are found."
                alertStyling = "Green"

            return render_template("/convenor/student_list_departm.html", select_result=select_result, message=message, alertStyling=alertStyling, sort_re_progress=report_progress, active=active)

    else:
        is_convenor = result[0][0]

        # if report_progress equal to "None", it means the report has not been started by students and report_progress attribute in
        # database sql queyies should be assigned the value 'null' to select those reports as part of filer function
        if report_progress == 'None':
            connection.execute(
                "SELECT supervisor_id FROM supervisor where user_id =%s;", (user_id,))
            result = connection.fetchall()
            supervisor_id = result[0][0]

            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                                FROM student AS s
                                LEFT JOIN 
                                ( SELECT
                                student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                                LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                                LEFT JOIN user AS u ON u.user_id = s.user_id where (u.department_id=%s and s.student_id not in (SELECT student_id FROM student_supervisor where supervisor_id=%s) 
                                and r.report_progress_id is null) or
                                (u.department_id=%s and r.report_progress_id<>%s and r.report_progress_id is null );""", (department_id, supervisor_id, department_id, 3))
            select_result = connection.fetchall()

            if select_result == []:
                message = "report is not found. Please try again!"
                alertStyling = "Red"
            else:
                message = "reports are found."
                alertStyling = "Green"

            return render_template("/convenor/student_list_departm.html", select_result=select_result, message=message, alertStyling=alertStyling, sort_re_progress=report_progress, active=active)

        else:
            connection.execute(
                "SELECT supervisor_id FROM supervisor where user_id =%s;", (user_id,))
            result = connection.fetchall()
            supervisor_id = result[0][0]

            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, u.email_address, s.phone, r.report_id, r.report_progress_id, r.term, r.due_date
                                FROM student AS s
                                LEFT JOIN 
                                ( SELECT
                                student_id, MAX(term) AS max_term FROM 6_month_report GROUP BY student_id) AS m ON s.student_id = m.student_id
                                LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                                LEFT JOIN user AS u ON u.user_id = s.user_id where (u.department_id=%s and s.student_id not in (SELECT student_id FROM student_supervisor where supervisor_id=%s) 
                                and r.report_progress_id= %s) or
                                (u.department_id=%s and r.report_progress_id<>%s and r.report_progress_id = %s );""", (department_id, supervisor_id, report_progress, department_id, 3, report_progress))
            select_result = connection.fetchall()
            if select_result == []:
                message = "report is not found. Please try again!"
                alertStyling = "Red"
            else:
                message = "reports are found."
                alertStyling = "Green"

            return render_template("/convenor/student_list_departm.html", select_result=select_result, message=message, alertStyling=alertStyling, sort_re_progress=report_progress, active=active)

# Individual student details


@app_convenor.route('/convenor/student_detail', methods=['GET', 'POST'])
def student_detail():
    active = 'con_student'  # For the left nav bar become active
    student_id = request.form.get("ID")
    if student_id is None:
        student_id = request.args.get("ID")
    connection1 = getCursor()
    connection1.execute("""select s.first_name, s.last_name, email_address, password, department_name,enrolment_date, address, s.phone,part_full_time, thesis_title,s.student_id from student s left join user on s.user_id = user.user_id
         left join department on department.department_id = user.department_id where s.student_id = %s;""",
                        (student_id,))
    students_list = connection1.fetchall()
    supervisor_list = []
    for supervisor_type in ['main', 'associate', 'other']:
        connection2 = getCursor()
        connection2.execute("""select CONCAT(supervisor.first_name,' ',supervisor.last_name) from student_supervisor 
                join supervisor on student_supervisor.supervisor_id = supervisor.supervisor_id
                where student_id = %s and supervisor_type = %s ;""", (student_id, supervisor_type,))
        supervisor = connection2.fetchall()
        if not supervisor:
            supervisor_list.append('')
        else:
            supervisor_list.append(supervisor[0][0])

    return render_template('/convenor/student_detail.html', students_list=students_list, supervisor_list=supervisor_list, active=active)

# For convenor to edit his/her grade for a student


@app_convenor.route('/convenor/grade_edited', methods=['POST'])
def grade_edited():
    grade_status = request.form.get("grade")
    convenor_highlight = request.form.get("comment")
    con_subtime = datetime.now()
    reprot_id = request.form.get("reprot_ID")
    user_id = request.cookies.get('user_id')
    connection = getCursor()

    #  update database table sectione as it stores grade and hightlights by convener
    connection.execute("INSERT INTO sectionE_Convenor (report_id, user_id, Convenor_highlight, Convenors_to_complete) values(%s,%s,%s,%s);",
                       (reprot_id, user_id, convenor_highlight, grade_status))

    # update database table `updated_time` as it stores the submit time by different role
    connection.execute(
        "UPDATE updated_time SET convenor=%s WHERE report_id= %s;", (con_subtime, reprot_id))

    #  update database table 6_month_report as it records the reviewing process of report, '5 ' means this report is at admin after being reviewed by convener
    connection.execute(
        "UPDATE 6_month_report SET report_progress_id=%s WHERE report_id= %s;", (5, reprot_id))
    return redirect('/convenor/students')


# show all supervisor information, copied from administer part
@app_convenor.route('/convenor/supervisors', methods=['GET', 'POST'])
def supervisor():
    active = 'con_supervisor'  # For the left nav bar become active
    if request.method == 'GET':
        user_id = request.cookies.get('user_id')
        connection = getCursor()
        connection.execute(
            "SELECT department_id FROM user where user_id =%s;", (user_id,))
        result = connection.fetchall()
        department_id = result[0][0]
        connection.execute(
            "SELECT department_name  FROM 639_lu.department where department_id =%s;", (department_id,))
        result = connection.fetchall()
        Department_name = result[0][0]
        connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
            left join department on department.department_id = user.department_id
            left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
            left join student on student.student_id = student_supervisor.student_id group by s.supervisor_id having department_name = %s ;""", (Department_name,))
        select_result = connection.fetchall()
        return render_template("/convenor/supervisor.html", select_result=select_result, active=active)

    elif request.method == 'POST':
        search = request.form.get('search')
        if search == '':
            search_name = '%%'
        else:
            search_name = "%" + search + "%"

        user_id = request.cookies.get('user_id')
        connection = getCursor()
        connection.execute(
            "SELECT department_id FROM user where user_id =%s;", (user_id,))
        result = connection.fetchall()
        department_id = result[0][0]
        connection.execute(
            "SELECT department_name  FROM 639_lu.department where department_id =%s;", (department_id,))
        result = connection.fetchall()
        Department_name = result[0][0]
        connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
        left join department on department.department_id = user.department_id
        left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
        left join student on student.student_id = student_supervisor.student_id where department_name = %s AND CONCAT(s.first_name,' ',s.last_name) like %s group by s.supervisor_id;""", (Department_name, search_name))

        select_result = connection.fetchall()
        if select_result == []:
            message = "Supervisor is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "Supervisors are found."
            alertStyling = "Green"

        return render_template("/convenor/supervisor.html", select_result=select_result, message=message, alertStyling=alertStyling, active=active)

# Show history report


@app_convenor.route('/convenor/history_report', methods=['GET', 'POST'])
def view_histroyReport():
    active = 'con_student'  # For the left nav bar become active
    student_id = request.form.get('studentID')

    connection = getCursor()
    connection.execute(
        "SELECT * FROM 6_month_report where report_progress_id=6 and student_id=%s;", (student_id,))
    select_result = connection.fetchall()

    if select_result == []:
        message = "You have no history report availabe"
        alertStyling = "Red"

    return render_template('/convenor/view_old _report.html', select_result=select_result, student_id=student_id, active=active)
