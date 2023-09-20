# This is the chair's python file which consists of the following user stories:
# - Update status as a convenor
# - Complete Section E as a convenor
# - View students and staff in the faculty
# - Act on Section F

# Initial Setup
from flask import Blueprint, render_template, request, url_for, redirect, jsonify
import re
from datetime import datetime, date
import mysql.connector
from mysql.connector import FieldType
import connect

# for pagination
from flask_paginate import Pagination, get_page_args

app_chair = Blueprint('app_chair', __name__)

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

# View list of students (Sabrina)


@app_chair.route('/chair/students', methods=['GET', 'POST'])
def students():
    active = 'chair_student'  # For the left nav bar become active
    if request.method == 'GET':
        department_name = 'ALL'
        connection = getCursor()
        # revise this SQL queries part to add report column information by Wanjun Wang
        connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, department_name, email_address, s.phone, GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ', '), r.report_id, r.report_progress_id, r.term, r.due_date
                            FROM student AS s
                            LEFT JOIN user AS u ON s.user_id = u.user_id
                            LEFT JOIN student_supervisor AS ss ON ss.student_id = s.student_id
                            LEFT JOIN supervisor AS supervisor ON supervisor.supervisor_id = ss.supervisor_id
                            LEFT JOIN department AS d ON d.department_id = u.department_id
                            LEFT JOIN (
                                SELECT student_id, MAX(term) AS max_term
                                FROM 6_month_report
                                GROUP BY student_id
                            ) AS m ON s.student_id = m.student_id
                            LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                            GROUP BY s.student_id;""")
        select_result = connection.fetchall()
        # Get the current page number and the number of items displayed per page
        page, per_page, offset = get_page_args(
            page_parameter='page', per_page_parameter='per_page')
        # Calculate start index and end index
        start = offset
        end = offset + per_page
        # Get the data of the current page
        student_items = select_result[start:end]
        # Create a Pagination object
        pagination = Pagination(page=page, per_page=per_page, total=len(
            select_result), css_framework='bootstrap4')
        pagination_exist = 'Yes'
        return render_template("/chair/students.html", select_result=student_items, sort_depart=department_name, active=active, pagination=pagination, pagination_exist=pagination_exist)

    elif request.method == 'POST':
        search = request.form.get('search')
        if search is None:
            search_name = '%%'
        else:
            search_name = "%" + search + "%"

        department_name = request.form.get('inputGroupSelect')
        if department_name is None:
            department_name = 'ALL'
  # revise this SQL queries part to add report column information by Wanjun Wang
        connection = getCursor()
        if department_name == 'ALL':
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, department_name, email_address, s.phone, GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ', '), r.report_id, r.report_progress_id, r.term, r.due_date
                            FROM student AS s
                            LEFT JOIN user AS u ON s.user_id = u.user_id
                            LEFT JOIN student_supervisor AS ss ON ss.student_id = s.student_id
                            LEFT JOIN supervisor AS supervisor ON supervisor.supervisor_id = ss.supervisor_id
                            LEFT JOIN department AS d ON d.department_id = u.department_id
                            LEFT JOIN (
                                SELECT student_id, MAX(term) AS max_term
                                FROM 6_month_report
                                GROUP BY student_id
                            ) AS m ON s.student_id = m.student_id
                            LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                            where CONCAT( s.first_name,' ',s.last_name) like %s group by s.student_id;""", (search_name,))
        else:
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, department_name, email_address, s.phone, GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ', '), r.report_id, r.report_progress_id, r.term, r.due_date
                            FROM student AS s
                            LEFT JOIN user AS u ON s.user_id = u.user_id
                            LEFT JOIN student_supervisor AS ss ON ss.student_id = s.student_id
                            LEFT JOIN supervisor AS supervisor ON supervisor.supervisor_id = ss.supervisor_id
                            LEFT JOIN department AS d ON d.department_id = u.department_id
                            LEFT JOIN (
                                SELECT student_id, MAX(term) AS max_term
                                FROM 6_month_report
                                GROUP BY student_id
                            ) AS m ON s.student_id = m.student_id
                            LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term
                            where department_name = %s and CONCAT( s.first_name,' ',s.last_name) like %s group by s.student_id;""", (department_name, search_name,))

        select_result = connection.fetchall()
        if select_result == []:
            message = "Student is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "Students is found."
            alertStyling = "Green"

        return render_template("/chair/students.html", select_result=select_result, sort_depart=department_name,
                               message=message, alertStyling=alertStyling, active=active)

# View student's details


@app_chair.route('/chair/student_detail', methods=['GET', 'POST'])
def student_detail():
    global studentid
    if request.method == 'POST':
        student_id = request.form.get("ID")

        # use these varibles to return to grade task page instead of student list page
        return_to_grade = request.form.get("Return_to_grade")
        retrun_back_grade = False
        if return_to_grade == 'return_to_grade':
            retrun_back_grade = True

        connection1 = getCursor()
        connection1.execute("""select s.first_name, s.last_name, email_address, password, department_name,enrolment_date, address, s.phone,part_full_time, thesis_title,s.student_id from student s left join user on s.user_id = user.user_id
         left join department on department.department_id = user.department_id where s.student_id = %s;""",
                            (student_id,))
        students_list = connection1.fetchall()
        studentid = students_list[0][10]

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
    
    else:
         student_id = request.args.get("ID")
        # use these varibles to return to grade task page instead of student list page
         return_to_grade = request.form.get("Return_to_grade")
         retrun_back_grade = False
         if return_to_grade == 'return_to_grade':
            retrun_back_grade = True

         connection1 = getCursor()
         connection1.execute("""select s.first_name, s.last_name, email_address, password, department_name,enrolment_date, address, s.phone,part_full_time, thesis_title,s.student_id from student s left join user on s.user_id = user.user_id
         left join department on department.department_id = user.department_id where s.student_id = %s;""",
                            (student_id,))
         students_list = connection1.fetchall()
         studentid = students_list[0][10]

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
    return render_template('/chair/student_detail.html', students_list=students_list, supervisor_list=supervisor_list, Retrun_back_grade=retrun_back_grade)

# Get  details of a student


@app_chair.route('/chair/fetch_scholarships', methods=['POST'])
def fetch_scholarships():
    cur = getCursor()

    cur.execute("""SELECT scholar_name, scholar_value,scholar_tenure,scholar_end_date FROM 6_month_report
                inner join sectiona_scholar on 6_month_report.report_id = sectiona_scholar.report_id
                where student_id = %s;""", (studentid,))
    scholarship_list = cur.fetchall()

    return jsonify(scholarship_list)

# Get employment details of a student


@app_chair.route('/chair/fetch_employments', methods=['POST'])
def fetch_employments():
    cur = getCursor()

    cur.execute("""SELECT teaching,research,other FROM 6_month_report
                inner join sectiona_employment on 6_month_report.report_id = sectiona_employment.report_id
                where student_id = %s;""", (studentid,))
    employment_list = cur.fetchall()

    return jsonify(employment_list)

# View list of staff


@app_chair.route('/chair/staff', methods=['GET', 'POST'])
def staff():
    active = 'staff'  # For the left nav bar become active
    if request.method == 'GET':
        department_name = 'ALL'
        connection = getCursor()
        connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
            left join department on department.department_id = user.department_id
            left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
            left join student on student.student_id = student_supervisor.student_id group by s.supervisor_id;""",)
        select_result = connection.fetchall()

        connection.execute("""select staff_id,CONCAT(first_name,' ',last_name),email_address,department_name,phone,user_role from staff
        inner join user on staff.user_id = user.user_id
        inner join department on user.department_id = department.department_id;""")
        convenor_list = connection.fetchall()

        return render_template("/chair/supervisors.html", select_result=select_result,
                               sort_depart=department_name, convenor_list=convenor_list, active=active)

    elif request.method == 'POST':
        search = request.form.get('search')
        if search is None:
            search_name = '%%'
        else:
            search_name = "%" + search + "%"

        role = request.form.get("role")
        if role is not None:
            cur = getCursor()

            if role == 'supervisor':

                cur.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
                left join department on department.department_id = user.department_id
                left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
                left join student on student.student_id = student_supervisor.student_id group by s.supervisor_id;""")
                role_list = cur.fetchall()
                message = "Supervisors found"

            elif role == 'convenor':
                cur.execute("""select staff_id,CONCAT(first_name,' ',last_name),email_address,department_name,phone,user_role from staff
                inner join user on staff.user_id = user.user_id
                inner join department on user.department_id = department.department_id;""")
                role_list = cur.fetchall()
                message = "Convenors found"
            else:
                role = 'all'
                message = "All staff is listed below."
                cur.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
                left join department on department.department_id = user.department_id
                left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
                left join student on student.student_id = student_supervisor.student_id group by s.supervisor_id;""")
                supervisors = cur.fetchall()

                cur.execute("""select staff_id,CONCAT(first_name,' ',last_name),email_address,department_name,phone,user_role from staff
                inner join user on staff.user_id = user.user_id
                inner join department on user.department_id = department.department_id;""")
                convenor = cur.fetchall()

                role_list = supervisors + convenor

            alertStyling = 'Green'

            return render_template("/chair/supervisors.html", sort_role=role, role_list=role_list, message=message, alertStyling=alertStyling, active=active)

        department_name = request.form.get('inputGroupSelect')
        if department_name is None:
            department_name = 'ALL'

        # For supervisors only
        connection = getCursor()
        if department_name == 'ALL':
            connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,
            GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') 
            from supervisor s left join user on s.user_id = user.user_id
        left join department on department.department_id = user.department_id
        left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
        left join student on student.student_id = student_supervisor.student_id where CONCAT(s.first_name,' ',s.last_name) like %s group by s.supervisor_id;""", (search_name,))
        else:
            connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
        left join department on department.department_id = user.department_id
        left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
        left join student on student.student_id = student_supervisor.student_id where department.department_name = %s AND CONCAT(s.first_name,' ',s.last_name) like %s group by s.supervisor_id;""",
                               (department_name, search_name,))

        select_result = connection.fetchall()

        # For convenor
        if department_name == 'ALL':
            connection.execute("""select staff_id,CONCAT(first_name,' ',last_name),email_address,department_name,phone,user_role 
            from staff s left join user on s.user_id = user.user_id
            left join department on department.department_id = user.department_id
            where CONCAT(s.first_name,' ',s.last_name) like %s group by s.staff_id;""", (search_name,))
        else:
            connection.execute("""select staff_id,CONCAT(first_name,' ',last_name),email_address,department_name,phone,user_role 
            from staff s left join user on s.user_id = user.user_id
            left join department on department.department_id = user.department_id
            where department.department_name = %s AND CONCAT(s.first_name,' ',s.last_name) like %s group by s.staff_id;""", (department_name, search_name,))

        convenor_result = connection.fetchall()

        # combine both list
        select_result = select_result + convenor_result

        if select_result == []:
            message = "Staff is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "All staff is listed below."
            alertStyling = "Green"

        return render_template("/chair/supervisors.html", select_result=select_result, sort_depart=department_name, message=message, alertStyling=alertStyling, active=active)

# Grade as a convenor  (Wanjun)


@app_chair.route('/chair/grade/task', methods=['GET', 'POST'])
def grade_task():
    active = 'task'  # For the left nav bar become active
    if request.method == 'GET':
        no_task_message = False
        alertStyling_1 = 'color for warning'
        connection = getCursor()
        connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                          FROM student AS s
                          left join 6_month_report as 6r on s.student_id=6r.student_id 
                          left join user as u on u.user_id=s.user_id
                          where 6r.report_progress_id=3 and (s.student_id in (SELECT s_s.student_id FROM supervisor as sp inner join student_supervisor as s_s on sp.supervisor_id=s_s.supervisor_id  where sp.is_convenor=1));""")
        select_result1 = connection.fetchall()

        connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                                FROM sectionF As F inner join 6_month_report AS 6r on F.report_id=6r.report_id
                                left join student AS s on s.student_id=6r.student_id
                                left join user AS u on u.user_id=s.user_id 
                                where 6r.chair_action is null and report_progress_id='6';""")
        select_result2 = connection.fetchall()
        if select_result1 == [] and select_result2 == []:
            no_task_message = 'Currently there is no task to grade'
            alertStyling_1 = "Yellow"
        return render_template("/chair/grade.html", select_result1=select_result1, select_result2=select_result2, no_task_message=no_task_message, alertStyling_1=alertStyling_1, active=active)

    else:
        message = False
        alertStyling = 'color for warning'
        search = request.form.get('search')
        if search == '':
            search_name = '%%'
        else:
            search_name = "%" + search + "%"
            connection = getCursor()
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                          FROM student AS s\
                          left join 6_month_report as 6r on s.student_id=6r.student_id \
                          left join user as u on u.user_id=s.user_id\
                          where 6r.report_progress_id=3 and (s.student_id in (SELECT s_s.student_id FROM supervisor as sp inner join student_supervisor as s_s on sp.supervisor_id=s_s.supervisor_id  where sp.is_convenor=1)) and CONCAT(s.first_name, ' ', s.last_name) like %s;""", (search_name,))
            select_result1 = connection.fetchall()

            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                                FROM sectionF As F inner join 6_month_report AS 6r on F.report_id=6r.report_id
                                left join student AS s on s.student_id=6r.student_id
                                left join user AS u on u.user_id=s.user_id 
                                where (6r.chair_action is null and report_progress_id='6')
                                having student_name like %s;""", (search_name,))
            select_result2 = connection.fetchall()
            if select_result1 == [] and select_result2 == []:
                message = 'No results found '
                alertStyling = "Red"
        return render_template("/chair/grade.html", select_result1=select_result1, select_result2=select_result2, message=message, alertStyling=alertStyling, active=active)

# Grade edited (Wanjun)


@app_chair.route('/chair/grade_edited', methods=['POST'])
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
    return redirect('/chair/grade/task')

# Send section F message


@app_chair.route('/chair/send_reminder_sectionF', methods=['GET', 'POST'])
def SectionF_reminder():
    if request.method == 'POST':
        report_id = request.form.get("Report_ID")
        chair_comment = request.form.get("Chair_Comment")
        reminder_info = 'chair has seen the F part you worte, and the given comment is :'+chair_comment
        connection = getCursor()
        connection.execute(
            "SELECT student_id FROM 6_month_report where report_id =%s;", (report_id,))
        result = connection.fetchall()
        student_id = result[0][0]
        connection.execute(
            "SELECT user_id FROM student where student_id=%s;", (student_id,))
        result = connection.fetchall()
        user_id = result[0][0]
        # insert new row into reminder table
        connection.execute("INSERT INTO reminder (user_id, student_id, type,reminder_info) values(%s,%s,%s,%s);",
                           (user_id, student_id, 'F_section', reminder_info))
        # update 6MR report
        connection.execute(
            "UPDATE 6_month_report SET chair_action=%s WHERE report_id=%s;", (chair_comment, report_id))
        return redirect('/chair/grade/task')

# Filter student's report progress


@app_chair.route('/chair/filter_report_progress', methods=['POST'])
def student_detail_filter1():
    active = 'chair_student'  # For the left nav bar become active
    message = 'begin'
    alertStyling = 'begin'
    report_progress = request.form.get("report_progress")

    # if report_progress equal to "None", it means the report has not been started by students and report_progress ID attribute in
    # database sql queyies should be assigned the value 'null' to select those reports as part of filer function
    if report_progress == 'None':
        connection = getCursor()
        connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, department_name, email_address, s.phone, GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ', '), r.report_id, r.report_progress_id, r.term, r.due_date
                            FROM student AS s
                            LEFT JOIN user AS u ON s.user_id = u.user_id
                            LEFT JOIN student_supervisor AS ss ON ss.student_id = s.student_id
                            LEFT JOIN supervisor AS supervisor ON supervisor.supervisor_id = ss.supervisor_id
                            LEFT JOIN department AS d ON d.department_id = u.department_id
                            LEFT JOIN (
                                SELECT student_id, MAX(term) AS max_term
                                FROM 6_month_report
                                GROUP BY student_id
                            ) AS m ON s.student_id = m.student_id
                            LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term 
                            where r.report_progress_id is null
                            GROUP BY s.student_id;""")
        select_result = connection.fetchall()
        if select_result == []:
            message = "reprot is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "reports are found."
            alertStyling = "Green"

        return render_template("/chair/students.html", select_result=select_result, message=message, alertStyling=alertStyling, sort_re_progress=report_progress, active=active)

    else:
        connection = getCursor()
        connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, department_name, email_address, s.phone, GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ', '), r.report_id, r.report_progress_id, r.term, r.due_date
                            FROM student AS s
                            LEFT JOIN user AS u ON s.user_id = u.user_id
                            LEFT JOIN student_supervisor AS ss ON ss.student_id = s.student_id
                            LEFT JOIN supervisor AS supervisor ON supervisor.supervisor_id = ss.supervisor_id
                            LEFT JOIN department AS d ON d.department_id = u.department_id
                            LEFT JOIN (
                                SELECT student_id, MAX(term) AS max_term
                                FROM 6_month_report
                                GROUP BY student_id
                            ) AS m ON s.student_id = m.student_id
                            LEFT JOIN 6_month_report AS r ON r.student_id = s.student_id AND r.term = m.max_term 
                            where r.report_progress_id =%s
                            GROUP BY s.student_id;""", (report_progress,))
        select_result = connection.fetchall()
        if select_result == []:
            message = "report is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "reports are found."
            alertStyling = "Green"

        return render_template("/chair/students.html", select_result=select_result, message=message, alertStyling=alertStyling, sort_re_progress=report_progress, active=active)

# Chair's tasks filter


@app_chair.route('/chair/filter_task', methods=['POST'])
def task_filter():
    active = 'task'  # For the left nav bar become active
    message = 'begin'
    alertStyling = 'begin'
    task_classfi = request.form.get("task_classfi")
    search = request.form.get('search')

    if task_classfi == '1':
            connection = getCursor()
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                          FROM student AS s
                          left join 6_month_report as 6r on s.student_id=6r.student_id 
                          left join user as u on u.user_id=s.user_id
                          where 6r.report_progress_id=3 and (s.student_id in (SELECT s_s.student_id FROM supervisor as sp inner join student_supervisor as s_s on sp.supervisor_id=s_s.supervisor_id  where sp.is_convenor=1));""")
            select_result1 = connection.fetchall()
            select_result2 = False

            if select_result1 == []:
                message = "no task is not found. Please try again!"
                alertStyling = "Red"
            else:
               message = "task is found."
               alertStyling = "Green"

               return render_template("/chair/grade.html", select_result1=select_result1, select_result2=select_result2, message=message, alertStyling=alertStyling, sort_task=task_classfi, active=active)

    elif  task_classfi == '2':
             connection = getCursor()
             connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                                FROM sectionF As F inner join 6_month_report AS 6r on F.report_id=6r.report_id
                                left join student AS s on s.student_id=6r.student_id
                                left join user AS u on u.user_id=s.user_id 
                                where 6r.chair_action is null and report_progress_id='6';""")
             select_result2 = connection.fetchall()
             select_result1 = False
             if select_result2 == []:
                message = "no task is not found. Please try again!"
                alertStyling = "Red"
             else:
                message = "task is found."
                alertStyling = "Green"

             return render_template("/chair/grade.html", select_result1=select_result1, select_result2 = select_result2, message=message, alertStyling=alertStyling,sort_task=task_classfi)


    else:
        message = False
        alertStyling = 'color for warning'
        search = request.form.get('search')
        if search == '':
            search_name = '%%'
        else:
            search_name = "%" + search + "%"
            connection = getCursor()
            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                          FROM student AS s\
                          left join 6_month_report as 6r on s.student_id=6r.student_id \
                          left join user as u on u.user_id=s.user_id\
                          where 6r.report_progress_id=3 and (s.student_id in (SELECT s_s.student_id FROM supervisor as sp inner join student_supervisor as s_s on sp.supervisor_id=s_s.supervisor_id  where sp.is_convenor=1)) and CONCAT(s.first_name, ' ', s.last_name) like %s;""", (search_name,))
            select_result1 = connection.fetchall()

            connection.execute("""SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, s.phone, u.email_address, 6r.report_id, 6r.report_progress_id, 6r.term, 6r.due_date
                                FROM sectionF As F inner join 6_month_report AS 6r on F.report_id=6r.report_id
                                left join student AS s on s.student_id=6r.student_id
                                left join user AS u on u.user_id=s.user_id 
                                where (6r.chair_action is null and report_progress_id='6')
                                having student_name like %s;""", (search_name,))
            select_result2 = connection.fetchall()
            if select_result1 == [] and select_result2 == []:
                message = 'No results found '
                alertStyling = "Red"
        return render_template("/chair/grade.html", select_result1=select_result1, select_result2=select_result2, message=message, alertStyling=alertStyling, active=active)


@app_chair.route('/chair/history_report', methods=['GET', 'POST'])
def view_histroyReport():
    student_id = request.form.get('studentID')

    connection = getCursor()
    connection.execute(
        "SELECT * FROM 6_month_report where report_progress_id=6 and student_id=%s;", (student_id,))
    select_result = connection.fetchall()

    if select_result == []:
        message = "You have no history report availabe"
        alertStyling = "Red"

    return render_template('/chair/view_old _report.html', select_result=select_result,student_id=student_id)
