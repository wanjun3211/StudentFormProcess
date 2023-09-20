# This is the admin's server file which contains the following user stories:
# - Confirm students' registration
# - Manage supervisors and students in the faculty
# - Notify user who has not completed the form
# - Confirm that the report is completed and notify student and their supervisors
# - Check overdue reports
# - Identify students that have issues

# Database and flask add ins set up
from flask import Blueprint, render_template, request, url_for, redirect
import re
from datetime import datetime, date
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import jsonify

# for pagination
from flask_paginate import Pagination, get_page_args

# For blueprint
app_admin = Blueprint('app_admin', __name__)

# Set up database connection
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


# List of Registrations (Sabrina)
userlist = []
selected_ids_numbers = []


@app_admin.route('/admin/registrations', methods=['get', 'post'])
def registrations():
    global userlist
    global selected_ids_numbers
    connection = getCursor()

    # Unconfirmed list for both supervisors and students
    connection.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
    inner join student on user.user_id = student.user_id
    where admin_reviewed = 0 and admin_reject is null;""")
    userlist = connection.fetchall()
    active = 'regis'  # For the left nav bar become active

    if request.method == "POST":
        if 'reset' in request.form:
            redirect('/admin/registrations')

        elif 'search-registrations' in request.form:
            # Search results for names only
            name = request.form.get("searchEntry-registrations")

            if name == '':
                message = " Please enter your search!"
                alertStyling = "Red"
                connection.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
                inner join student on user.user_id = student.user_id
                where admin_reviewed = 0 and admin_reject is null
                """)
                userlist = connection.fetchall()
                return render_template("/admin/registrations.html", unconfirmedList=userlist, message=message,
                                       alertStyling=alertStyling)

            connection.execute(f"""select first_name,last_name,email_address,password,user_role,admin_reviewed,  user.user_id from user
            inner join student on user.user_id = student.user_id
            where admin_reviewed = 0 and (first_name LIKE '%{name}%' OR last_name LIKE '%{name}%') and admin_reject is null
            ;""")
            userlist = connection.fetchall()

            if len(userlist) == 0:
                message = "User is not found. Please try again!"
                alertStyling = "Red"
            else:
                message = "User is found!"
                alertStyling = "Green"
            return render_template("/admin/registrations.html", unconfirmedList=userlist, message=message,
                                   alertStyling=alertStyling, active=active)

        elif 'submit-checkbox' in request.form:
            selected_ids = request.form.getlist("ids")
            selected_ids_numbers = [int(x) for x in selected_ids]

            if not selected_ids_numbers:
                print("PLACEHOLDER")
            else:
                for id in selected_ids_numbers:
                    connection.execute(
                        """update user set admin_reviewed = 1 where user_id = %s;""", (id,))

                cur = getCursor()
                cur.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
                inner join student on user.user_id = student.user_id
                where admin_reviewed = 0 and admin_reject is null;""")
                userlist = cur.fetchall()

                message = "Registration(s) confirmed!"
                alertStyling = "Green"
                return render_template("/admin/registrations.html", unconfirmedList=userlist, message=message,
                                       alertStyling=alertStyling, active=active)
        elif 'reject-checkbox' in request.form:
            selected_ids = request.form.getlist("ids")
            selected_ids_numbers = [int(x) for x in selected_ids]

            if not selected_ids_numbers:
                print("PLACEHOLDER")
            else:
                for id in selected_ids_numbers:
                    connection.execute(
                        """update user set admin_reject = 1 where user_id = %s;""", (id,))

                cur = getCursor()
                cur.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
                inner join student on user.user_id = student.user_id
                where admin_reviewed = 0 and admin_reject is null;""")
                userlist = cur.fetchall()

                message = "Registration(s) are rejected and message has been sent!"
                alertStyling = "Yellow"
                return render_template("/admin/registrations.html", unconfirmedList=userlist, message=message,
                                       alertStyling=alertStyling, active=active)

    return render_template("/admin/registrations.html", unconfirmedList=userlist, active=active)


# Confirm registrations (Sabrina)

@app_admin.route("/admin/confirmRegistrations")
def confirm_registrations():
    connection = getCursor()
    connection.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
    inner join student on user.user_id = student.user_id
    where admin_reviewed = 0 and admin_reject is null;""")
    userlist = connection.fetchall()
    active = 'regis'  # For the left nav bar become active
    for user in userlist:
        userID = user[6]
        connection.execute(
            """UPDATE user set user.admin_reviewed = 1 where user.user_id = %s;""", (userID,))
        length = len(userlist)

    if length == 0:
        message = "There is no unconfirmed registrations"
        alertStyling = "Red"
        noConfirmation = 1
        return render_template("/admin/registrations.html", message=message, alertStyling=alertStyling,
                               noConfirmation=noConfirmation, active=active)
    else:
        message = f"{length} students are confirmed!"
        alertStyling = "Green"

        cur = getCursor()
        cur.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
        inner join student on user.user_id = student.user_id
        where admin_reviewed = 0 and admin_reject is null;""")
        userlist = cur.fetchall()
        return render_template("/admin/registrations.html", unconfirmedList=userlist, message=message,
                               alertStyling=alertStyling, active=active)


# Reconfirm registrations that are rejected by admin (Sabrina)
@app_admin.route('/admin/reconfirmRejected', methods=['GET', 'POST'])
def reconfirmRegistrations():
    # Rejected list
    cur3 = getCursor()
    cur3.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
    inner join student on user.user_id = student.user_id
    where admin_reviewed = 0 and admin_reject = 1;""")
    rejected_student_list = cur3.fetchall()
    active = 'regis'  # For the left nav bar become active

    if 'submit-checkbox-rejects' in request.form:
        selected_rejectids = request.form.getlist("rejectedids")
        selected_rejectids_numbers = [int(x) for x in selected_rejectids]
        connection = getCursor()

        for id in selected_rejectids_numbers:
            connection.execute(
                """update user set admin_reviewed = 1, admin_reject = null where user_id = %s;""", (id,))

        cur = getCursor()
        cur.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
        inner join student on user.user_id = student.user_id
        where admin_reviewed = 0 and admin_reject = 1;""")
        rejected_student_list = cur.fetchall()

        message = "Rejected student(s)'s registrations were confirmed and they can now logged in."
        alertStyling = "Green"

        return render_template('/admin/reconfirmRegistrations.html', rejectedlist=rejected_student_list,
                               message=message, alertStyling=alertStyling, active=active)

    return render_template('/admin/reconfirmRegistrations.html', rejectedlist=rejected_student_list, active=active)


# for show a list for all students' info (By Beibei)
@app_admin.route('/admin/students', methods=['GET', 'POST'])
def students():
    message = request.args.get('message')
    alertStyling = request.args.get('alertStyling')
    if request.method == 'GET':
        department_name = 'ALL'
        connection = getCursor()
        connection.execute("""select s.student_id,CONCAT(s.first_name,' ', s.last_name), department_name,email_address,s.phone, GROUP_CONCAT(COALESCE(CONCAT( supervisor_type, ': ' ,supervisor.first_name,' ',supervisor.last_name), '') SEPARATOR ' , ') from student s left join user on s.user_id = user.user_id
                 left join student_supervisor on student_supervisor.student_id = s.student_id
                left join supervisor on supervisor.supervisor_id = student_supervisor.supervisor_id
                left join department on department.department_id = user.department_id group by s.student_id;""")
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
        active = 'student'  # For the left nav bar become active
        return render_template("/admin/students.html", sort_depart=department_name, student_items=student_items, pagination=pagination, pagination_exist=pagination_exist, active=active, message=message, alertStyling=alertStyling)

    elif request.method == 'POST':
        search = request.form.get('search')
        if search is None:
            search_name = '%%'
        else:
            search_name = "%" + search + "%"

        department_name = request.form.get('inputGroupSelect')
        if department_name is None:
            department_name = 'ALL'

        connection = getCursor()
        if department_name == 'ALL':
            connection.execute("""select s.student_id,CONCAT(s.first_name,' ', s.last_name), department_name,email_address,s.phone, GROUP_CONCAT(COALESCE(CONCAT( supervisor_type, ': ' ,supervisor.first_name,' ',supervisor.last_name), '') SEPARATOR ' , ') from student s left join user on s.user_id = user.user_id
         left join student_supervisor on student_supervisor.student_id = s.student_id
        left join supervisor on supervisor.supervisor_id = student_supervisor.supervisor_id
        left join department on department.department_id = user.department_id where CONCAT( s.first_name,' ',s.last_name) like %s group by s.student_id;""",
                               (search_name,))
        else:
            connection.execute("""select s.student_id,CONCAT(s.first_name,' ', s.last_name), department_name, email_address, s.phone, GROUP_CONCAT(COALESCE(CONCAT( supervisor_type, ': ' ,supervisor.first_name,' ',supervisor.last_name), '') SEPARATOR ' , ') from student s left join user on s.user_id = user.user_id
                    left join department on department.department_id = user.department_id
                    left join student_supervisor on student_supervisor.student_id = s.student_id
                    left join supervisor on supervisor.supervisor_id = student_supervisor.supervisor_id where department.department_name = %s and CONCAT( s.first_name,' ',s.last_name) like %s group by s.student_id;""",
                               (department_name, search_name,))

        select_result = connection.fetchall()
        if select_result == []:
            message = "Student is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "Students are found."
            alertStyling = "Green"

        pagination_exist = 'No'
        active = 'student'  # For the left nav bar become active
        return render_template("/admin/students.html", student_items=select_result, sort_depart=department_name,
                               message=message, alertStyling=alertStyling, pagination_exist=pagination_exist, active=active)


# for show all students' info (By Beibei)
studentid = ''


@app_admin.route('/admin/student_detail', methods=['GET', 'POST'])
def student_detail():
    global studentid
    student_id = request.form.get("ID")
    studentid = student_id
    if student_id is None:
        student_id = request.args.get("ID")
        studentid = student_id
    connection1 = getCursor()
    connection1.execute("""select s.first_name, s.last_name, email_address, password, department_name,enrolment_date, address, s.phone,part_full_time, thesis_title,s.student_id from student s left join user on s.user_id = user.user_id
     left join department on department.department_id = user.department_id where s.student_id = %s;""",
                        (student_id,))
    students_list = connection1.fetchall()
    current_date = date.today()
    cur = getCursor()
    cur.execute("""select report_id from 6_month_report where due_date < current_date and student_id = %s;""",
                (student_id,))
    report_list = cur.fetchall()

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
    active = 'student'  # For the left nav bar become active
    return render_template('/admin/student_detail.html', students_list=students_list, supervisor_list=supervisor_list, active=active, report_list=report_list)


@app_admin.route('/admin/fetch_scholarships', methods=['POST'])
def fetch_scholarships():
    cur = getCursor()

    cur.execute("""SELECT scholar_name, scholar_value,scholar_tenure,scholar_end_date FROM 6_month_report
                inner join sectiona_scholar on 6_month_report.report_id = sectiona_scholar.report_id
                where student_id = %s;""", (studentid,))
    scholarship_list = cur.fetchall()

    return jsonify(scholarship_list)


@app_admin.route('/admin/fetch_employments', methods=['POST'])
def fetch_employments():
    cur = getCursor()

    cur.execute("""SELECT teaching,research,other FROM 6_month_report
                inner join sectiona_employment on 6_month_report.report_id = sectiona_employment.report_id
                where student_id = %s;""", (studentid,))
    employment_list = cur.fetchall()

    return jsonify(employment_list)

# add a new student (By Beibei)


@app_admin.route('/admin/add_student', methods=['GET', 'POST'])
def addStudent():
    if request.method == "POST":
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        department = request.form.get('department')
        enrolment_date = request.form.get('enrolment_date')
        address = request.form.get('address')
        phone = request.form.get('phone')
        part_full_time = request.form.get('status')
        thesis_title = request.form.get('thesis_title')
        connection = getCursor()
        connection.execute("""INSERT INTO user (email_address, password, department_id, user_role, admin_reviewed)
        VALUES(%s,%s,%s,'student',true);""", (email, password, department,))

        connection.execute("""INSERT INTO student (first_name, last_name, phone, enrolment_date, address, part_full_time, thesis_title, user_id)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, LAST_INSERT_ID());""", (
            first_name, last_name, phone, enrolment_date, address, part_full_time, thesis_title,))

        message = "New student added successfully!"
        alertStyling = "Green"

        for supervisor_type in ['main', 'associate', 'other']:
            supervisor_name = request.form.get(supervisor_type)
            if supervisor_name:
                supervisor_name = '%' + supervisor_name + '%'
                connection1 = getCursor()
                connection1.execute("""SELECT supervisor_id FROM supervisor
                    WHERE CONCAT(supervisor.first_name,' ', supervisor.last_name) LIKE %s;""", (supervisor_name,))
                supervisor = connection1.fetchall()
                if supervisor != [] and len(supervisor) == 1:
                    supervisor_id = supervisor[0][0]
                    connection2 = getCursor()
                    connection2.execute("""INSERT INTO student_supervisor (student_id,supervisor_id,supervisor_type)
                    VALUES(LAST_INSERT_ID(),%s,%s);""",
                                        (supervisor_id, supervisor_type,))
                else:
                    message = "Other information has been added successfully, except for the supervisor section, please review the entered supervisor name."
                    alertStyling = "Yellow"

        return redirect(url_for('app_admin.students', message=message, alertStyling=alertStyling))

    elif request.method == 'GET':
        active = 'student'  # For the left nav bar become active
        return render_template('/admin/add_student.html', active=active)


# Show the student's infomation of the update page. (By Beibei)
@app_admin.route('/admin/update_student', methods=['GET', 'POST'])
def updateStudent():
    if request.method == 'POST':
        student_id = request.form.get("ID")
        connection1 = getCursor()
        connection1.execute("""select s.first_name, s.last_name, email_address, password, department_id,enrolment_date, address, s.phone,part_full_time, thesis_title,GROUP_CONCAT(COALESCE(CONCAT( supervisor_type, ': ' ,supervisor.first_name,' ',supervisor.last_name), ' ') SEPARATOR ' , '),s.student_id from student s left join user on s.user_id = user.user_id
        left join student_supervisor on student_supervisor.student_id = s.student_id
        left join supervisor on supervisor.supervisor_id = student_supervisor.supervisor_id where s.student_id = %s group by s.student_id ;""",
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
    active = 'student'  # For the left nav bar become active
    return render_template('/admin/update_student.html', students_list=students_list, supervisor_list=supervisor_list, active=active)


# Update the student's infomation after enter the student's information. (By Beibei)
@app_admin.route('/admin/update_student/submit', methods=['GET', 'POST'])
def update_student_submit():
    if request.method == "POST":
        stu_id = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        department = request.form.get('department')
        enrolment_date = request.form.get('enrolment_date')
        address = request.form.get('address')
        phone = request.form.get('phone')
        part_full_time = request.form.get('status')
        thesis_title = request.form.get('thesis_title')

        try:
            connection = getCursor()
            connection.execute("""UPDATE user u JOIN student s ON u.user_id = s.user_id
                SET u.email_address = %s,
                u.password = %s,
                u.department_id = %s,
                s.first_name = %s,
                s.last_name = %s,
                s.enrolment_date = %s,
                s.address = %s,
                s.phone = %s,
                s.part_full_time = %s,
                s.thesis_title = %s
                WHERE s.student_id = %s;""", (
                email, password, department, firstname, lastname, enrolment_date, address, phone, part_full_time,
                thesis_title,
                stu_id))
            message = "The student's personal information has been updated successfully!"
            alertStyling = "Green"

        except Exception:
            message = "The update was unsuccessful, please re-enter!"
            alertStyling = "Red"

        for supervisor_type in ['main', 'associate', 'other']:
            connection3 = getCursor()
            connection3.execute(
                """SELECT * FROM student_supervisor WHERE student_id = %s AND supervisor_type = %s;""",
                (stu_id, supervisor_type,))
            og_super = connection3.fetchall()
            now_super = request.form.get(supervisor_type)
            if now_super:
                supervisor_name = '%' + now_super + '%'
                connection1 = getCursor()
                connection1.execute("""SELECT supervisor_id FROM supervisor
                                WHERE CONCAT(supervisor.first_name,' ', supervisor.last_name) LIKE %s;""",
                                    (supervisor_name,))
                supervisor = connection1.fetchall()
                if supervisor:
                    if supervisor != [] and len(supervisor) == 1:
                        supervisor_id = supervisor[0][0]
                        if og_super and now_super:
                            # There can only be one id to the name entered. Other cases cannot be updated successfully.

                            # If the supervisor type already exists, the function will be update, otherwise it will be insert function.
                            connection4 = getCursor()
                            connection4.execute("""UPDATE student_supervisor SET supervisor_id = %s
                                    WHERE student_id = %s AND supervisor_type = %s;""",
                                                (supervisor_id, stu_id, supervisor_type,))
                        elif og_super and now_super == '':
                            connection4 = getCursor()
                            connection4.execute(
                                """DELETE FROM student_supervisor WHERE student_id = %s AND supervisor_type = %s;""",
                                (stu_id, supervisor_type,))
                        elif og_super == [] and now_super:
                            connection4 = getCursor()
                            connection4.execute("""INSERT INTO student_supervisor (student_id, supervisor_id,
                            supervisor_type) VALUES (%s, %s, %s);""", (stu_id, supervisor_id, supervisor_type,))
                    else:
                        message = "The supervisor you entered was wrong. Please re-enter the name of the supervisor. "
                        alertStyling = "Red"
                        break

                else:
                    message = "The supervisor you entered was wrong. Please re-enter the name of the supervisor. "
                    alertStyling = "Red"
                    break

        c1 = getCursor()
        c1.execute(
            """select s.first_name, s.last_name, email_address, password, department_id,enrolment_date, address, s.phone,part_full_time, thesis_title,s.student_id from student s left join user on s.user_id = user.user_id where s.student_id = %s;""",
            (stu_id,))
        students_list = c1.fetchall()

        supervisor_list = []
        for supervisor_type in ['main', 'associate', 'other']:
            c2 = getCursor()
            c2.execute("""select CONCAT(supervisor.first_name,' ',supervisor.last_name) from student_supervisor
                       join supervisor on student_supervisor.supervisor_id = supervisor.supervisor_id
                       where student_id = %s and supervisor_type = %s ;""", (stu_id, supervisor_type,))
            supervisor = c2.fetchall()
            if not supervisor:
                supervisor_list.append('')
            else:
                supervisor_list.append(supervisor[0][0])
        active = 'student'  # For the left nav bar become active
        return render_template("/admin/student_detail.html", students_list=students_list,
                               supervisor_list=supervisor_list, alertStyling=alertStyling,
                               message=message, active=active)


# Delete a student from user table,student table and student_supervisor table. (By Beibei)
@app_admin.route('/admin/delete_student', methods=['GET', 'POST'])
def delete_student():
    student_id = request.args.get('student_id')
    db = getCursor()
    db.execute("""DELETE student, user, student_supervisor FROM student
    LEFT JOIN user ON user.user_id = student.user_id
    LEFT JOIN student_supervisor ON student_supervisor.student_id = student.student_id
    WHERE student.student_id = %s;""", (student_id,))

    message = "This student has been delete successfully."
    alertStyling = "Green"

    return redirect(url_for('app_admin.students', message=message, alertStyling=alertStyling))


# Get information about all supervisors.(BY Beibei)
@app_admin.route('/admin/supervisors', methods=['GET', 'POST'])
def supervisors():
    message = request.args.get('message')
    alertStyling = request.args.get('alertStyling')
    if request.method == 'GET':
        department_name = 'ALL'
        connection = getCursor()
        connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
            left join department on department.department_id = user.department_id
            left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
            left join student on student.student_id = student_supervisor.student_id group by s.supervisor_id;""", )
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

        active = 'supervisor'  # For the left nav bar become active
        return render_template("/admin/supervisors.html", select_result=student_items, sort_depart=department_name, message=message, alertStyling=alertStyling, active=active, pagination=pagination, pagination_exist=pagination_exist)

    elif request.method == 'POST':
        search = request.form.get('search')
        if search is None:
            search_name = '%%'
        else:
            search_name = "%" + search + "%"

        department_name = request.form.get('inputGroupSelect')
        if department_name is None:
            department_name = 'ALL'

        connection = getCursor()
        if department_name == 'ALL':
            connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type,':',student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
        left join department on department.department_id = user.department_id
        left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
        left join student on student.student_id = student_supervisor.student_id where CONCAT(s.first_name,' ',s.last_name) like %s group by s.supervisor_id;""",
                               (search_name,))
        else:
            connection.execute("""select s.supervisor_id,CONCAT(s.first_name,' ', s.last_name), email_address, department_name, s.phone ,GROUP_CONCAT(COALESCE(CONCAT(student.first_name,' ',student.last_name), '') SEPARATOR ' , ') from supervisor s left join user on s.user_id = user.user_id
        left join department on department.department_id = user.department_id
        left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
        left join student on student.student_id = student_supervisor.student_id where department.department_name = %s AND CONCAT(s.first_name,' ',s.last_name) like %s group by s.supervisor_id;""",
                               (department_name, search_name,))

        select_result = connection.fetchall()
        if select_result == []:
            message = "Supervisor is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "Supervisors are found."
            alertStyling = "Green"

        active = 'supervisor'  # For the left nav bar become active
        return render_template("/admin/supervisors.html", select_result=select_result, sort_depart=department_name,
                               message=message, alertStyling=alertStyling, active=active)


# Show the Update information pages.(BY Beibei)
@app_admin.route('/admin/update_supervisor', methods=['GET', 'POST'])
def updateSupervisor():
    if request.method == 'POST':
        supervisor_id = request.form.get("ID")
        connection1 = getCursor()
        connection1.execute("""select s.first_name, s.last_name, email_address, password, department_id,s.phone, s.supervisor_id from supervisor s left join user on s.user_id = user.user_id
            left join student_supervisor on student_supervisor.supervisor_id = s.supervisor_id
            where s.supervisor_id = %s;""", (supervisor_id,))
        supervisors_list = connection1.fetchall()

    active = 'supervisor'  # For the left nav bar become active
    return render_template("/admin/update_supervisor.html", supervisors_list=supervisors_list, active=active)


# Update the information of supervisors.(BY Beibei)
@app_admin.route('/admin/update_supervisor/submit', methods=['GET', 'POST'])
def update_supervisor_submit():
    if request.method == "POST":
        sup_id = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        department = request.form.get('department')
        phone = request.form.get('phone')

        try:
            connection = getCursor()
            connection.execute("""UPDATE user u JOIN supervisor s ON u.user_id = s.user_id
                        SET u.email_address = %s,
                        u.password = %s,
                        u.department_id = %s,
                        s.first_name = %s,
                        s.last_name = %s,
                        s.phone = %s
                         WHERE s.supervisor_id = %s;""",
                               (email, password, department, firstname, lastname, phone, sup_id,))
            message = "The supervisor's personal information has been updated successfully!"
            alertStyling = "Green"

        except Exception as e:
            message = "The update was unsuccessful, please re-enter!"
            alertStyling = "Red"
            # print(e)

    return redirect(url_for("app_admin.supervisors", alertStyling=alertStyling, message=message))


# Delete a supervisor in user table and supervisor table.(BY Beibei)


@app_admin.route('/admin/delete_supervisor', methods=['GET', 'POST'])
def delete_supervisor():
    super_id = request.args.get('supervisor_id')
    db = getCursor()
    db.execute(
        """SELECT * FROM student_supervisor WHERE supervisor_id = %s;""", (super_id,))
    super_info = db.fetchall()
    if super_info:  # Determine if this supervisor currently has students assigned.
        message = "There are assigned students under this supervisor's name and this time cannot be deleted."
        alertStyling = "Red"
    else:
        connection = getCursor()
        # Delete data associated with supervisor from all tables
        connection.execute(
            """SELECT user_id FROM supervisor WHERE supervisor_id = %s;""", (super_id,))
        user_info = connection.fetchall()
        db.execute(
            """DELETE FROM supervisor WHERE supervisor_id = %s;""", (super_id,))
        user_id = user_info[0][0]
        db.execute("""DELETE FROM user WHERE user_id = %s;""", (user_id,))
        message = "This supervisor has been delete successfully."
        alertStyling = "Green"

    return redirect(url_for('app_admin.supervisors', message=message, alertStyling=alertStyling))


# add a new supervisor in user table and supervisor table.(BY Beibei)
@app_admin.route('/admin/add_supervisor', methods=['GET', 'POST'])
def addSupervisor():
    if request.method == "POST":
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        department = request.form.get('department')
        phone = request.form.get('phone')
        connection = getCursor()
        connection.execute("""INSERT INTO user (email_address, password, department_id, user_role, admin_reviewed)
        VALUES(%s,%s,%s,'supervisor',true);""", (email, password, department,))

        connection.execute("""INSERT INTO supervisor (first_name, last_name, phone, is_convenor,user_id)
        VALUES ( %s, %s, %s, 0, LAST_INSERT_ID());""", (first_name, last_name, phone,))

        message = "New supervisor added successfully!"
        alertStyling = "Green"

        for supervisor_type in ['main', 'associate', 'other']:
            student_name = request.form.get(supervisor_type)
            if student_name:
                student_name = '%' + student_name + '%'
                connection1 = getCursor()
                connection1.execute("""SELECT student_id FROM student
                    WHERE CONCAT(student.first_name,' ', student.last_name) LIKE %s;""", (student_name,))
                students = connection1.fetchall()
                if students != [] and len(students[0]) == 1:
                    student_id = students[0][0]
                    connection2 = getCursor()
                    connection2.execute("""INSERT INTO student_supervisor (supervisor_id,student_id,supervisor_type)
                    VALUES(LAST_INSERT_ID(),%s,%s);""", (student_id, supervisor_type,))
                    message = "New supervisor added successfully!"
                    alertStyling = "Green"
                else:
                    message = "All information has been added successfully, except for the failure to add supervisee."
                    alertStyling = "Yellow"
                    break

        return redirect(url_for('app_admin.supervisors', message=message, alertStyling=alertStyling))

    elif request.method == 'GET':
        active = 'supervisor'  # For the left nav bar become active
        return render_template('/admin/add_supervisor.html', active=active)


# send the reminder to students and supervisors who didn't finished the 6MR.(BY Beibei)
@app_admin.route('/admin/send_reminder', methods=['GET', 'POST'])
def send_reminder():
    active = 'reminder'  # For the left nav bar become active
    if request.method == 'GET':
        message = request.args.get('message')
        alertStyling = request.args.get('alertStyling')

        department_name = 'ALL'
        report_status = request.args.get('report')
        if report_status is None:
            report_status = 'undone'
        connection1 = getCursor()
        if report_status == "undone":
            connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , '),
              MAX(r.term),MAX(r.due_date),MAX(r.report_progress_id) , MAX(r.report_id) FROM student s LEFT JOIN user ON s.user_id = user.user_id
              LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
              LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
              LEFT JOIN department ON department.department_id = user.department_id
              LEFT JOIN 6_month_report r ON r.student_id = s.student_id
              WHERE r.report_progress_id != 6 AND r.report_progress_id != 5 OR r.report_progress_id is NULL GROUP BY s.student_id,r.report_id;""")
        elif report_status == 'done':
            connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , '),
                          MAX(r.term),MAX(r.due_date),MAX(r.report_progress_id) , MAX(r.report_id) FROM student s LEFT JOIN user ON s.user_id = user.user_id
                          LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
                          LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
                          LEFT JOIN department ON department.department_id = user.department_id
                          LEFT JOIN 6_month_report r ON r.student_id = s.student_id
                          WHERE r.report_progress_id = 5 GROUP BY s.student_id;""")
        elif report_status == 'completed':
            connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,
                    GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , ') as a,
                    r.term,r.due_date,r.report_progress_id,r.report_id
                FROM student s LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
                LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
                LEFT JOIN user ON s.user_id = user.user_id
                LEFT JOIN department ON department.department_id = user.department_id
                LEFT JOIN 6_month_report r ON r.student_id = s.student_id
                WHERE r.report_progress_id = 6 AND r.due_date = (select MAX(due_date) from 6_month_report) GROUP BY s.student_id, r.term, r.due_date, r.report_id;
                """)
        select_result = connection1.fetchall()

        current_date = datetime.now().date()
        connection1.execute("""SELECT r.report_id, GROUP_CONCAT(CONCAT(sup.first_name, ' ', sup.last_name)) AS supervisor_names
                                FROM 6_month_report r
                                JOIN student_supervisor ss ON r.student_id = ss.student_id
                                JOIN supervisor sup ON ss.supervisor_id = sup.supervisor_id
                                LEFT JOIN sectionE e ON e.supervisor_id = sup.supervisor_id AND e.report_id = r.report_id
                                WHERE e.report_id IS NULL AND r.report_progress_id =2
                                GROUP BY r.report_id;""")
        supervisor_list = connection1.fetchall()

        for i in range(len(select_result)):
            supervisor_found = False
            for supervisor in supervisor_list:
                if select_result[i][-1] == supervisor[0]:
                    select_result[i] = select_result[i] + (supervisor[1],)
                    supervisor_found = True
                    break
            if not supervisor_found:
                select_result[i] = select_result[i] + (None,)

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

        return render_template('/admin/send_reminder.html', select_result=student_items,
                               department_name=department_name, message=message, alertStyling=alertStyling, report=report_status, current_date=current_date, active=active, pagination=pagination, pagination_exist=pagination_exist)

    elif request.method == 'POST':
        current_date = datetime.now().date()
        report_status = request.form.get('report')
        search = request.form.get('search')
        if search is None:
            search_name = '%%'
        else:
            search_name = "%" + search + "%"

        department_name = request.form.get('inputGroupSelect')
        if department_name is None:
            department_name = 'ALL'

        connection1 = getCursor()
        if department_name == 'ALL':
            if report_status == "undone":
                connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , '),
              MAX(r.term),MAX(r.due_date),MAX(r.report_progress_id),MAX(r.report_id) FROM student s LEFT JOIN user ON s.user_id = user.user_id
              LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
              LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
              LEFT JOIN department ON department.department_id = user.department_id
              LEFT JOIN 6_month_report r ON r.student_id = s.student_id
              WHERE ((r.report_progress_id != 6 AND r.report_progress_id != 5) OR r.report_progress_id is NULL) AND CONCAT( s.first_name,' ',s.last_name) like %s GROUP BY s.student_id;""", (search_name,))

            elif report_status == "done":
                connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , '),
                              MAX(r.term),MAX(r.due_date),MAX(r.report_progress_id),MAX(r.report_id) FROM student s LEFT JOIN user ON s.user_id = user.user_id
                              LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
                              LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
                              LEFT JOIN department ON department.department_id = user.department_id
                              LEFT JOIN 6_month_report r ON r.student_id = s.student_id
                              WHERE r.report_progress_id = 5 AND CONCAT( s.first_name,' ',s.last_name) like %s GROUP BY s.student_id;""",
                                    (search_name,))
            elif report_status == "completed":
                connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,
                    GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , ') as a,
                    r.term,r.due_date,r.report_progress_id,r.report_id
                    FROM student s LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
                    LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
                    LEFT JOIN user ON s.user_id = user.user_id
                    LEFT JOIN department ON department.department_id = user.department_id
                    LEFT JOIN 6_month_report r ON r.student_id = s.student_id
                    WHERE r.report_progress_id = 6 AND r.due_date = (select MAX(due_date) from 6_month_report) AND CONCAT( s.first_name,' ',s.last_name) like %s GROUP BY s.student_id, r.term, r.due_date, r.report_id;""",
                                    (search_name,))
        else:
            if report_status == "undone":
                connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , '),
              MAX(r.term),MAX(r.due_date),MAX(r.report_progress_id) ,MAX(r.report_id) FROM student s LEFT JOIN user ON s.user_id = user.user_id
              LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
              LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
              LEFT JOIN department ON department.department_id = user.department_id
              LEFT JOIN 6_month_report r ON r.student_id = s.student_id
              WHERE ((r.report_progress_id != 6 AND r.report_progress_id != 5) OR r.report_progress_id is NULL )AND department.department_name = %s and CONCAT( s.first_name,' ',s.last_name) like %s group by s.student_id;""",
                                    (department_name, search_name,))
            elif report_status == "done":
                connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,GROUP_CONCAT(COALESCE(CONCAT(supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , '),
                              MAX(r.term),MAX(r.due_date),MAX(r.report_progress_id) ,MAX(r.report_id) FROM student s LEFT JOIN user ON s.user_id = user.user_id
                              LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
                              LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
                              LEFT JOIN department ON department.department_id = user.department_id
                              LEFT JOIN 6_month_report r ON r.student_id = s.student_id
                              WHERE r.report_progress_id = 5 AND department.department_name = %s and CONCAT( s.first_name,' ',s.last_name) like %s group by s.student_id;""",
                                    (department_name, search_name,))
            elif report_status == "completed":
                connection1.execute("""SELECT s.student_id,CONCAT(s.first_name, ' ', s.last_name),department_name,
                    GROUP_CONCAT(COALESCE(CONCAT(student_supervisor.supervisor_type, ': ', supervisor.first_name, ' ', supervisor.last_name), '') SEPARATOR ' , ') as a,
                    r.term,r.due_date,r.report_progress_id,r.report_id
                    FROM student s LEFT JOIN student_supervisor ON student_supervisor.student_id = s.student_id
                    LEFT JOIN supervisor ON supervisor.supervisor_id = student_supervisor.supervisor_id
                    LEFT JOIN user ON s.user_id = user.user_id
                    LEFT JOIN department ON department.department_id = user.department_id
                    LEFT JOIN 6_month_report r ON r.student_id = s.student_id
                    WHERE r.report_progress_id = 6 AND r.due_date = (select MAX(due_date) from 6_month_report) AND department.department_name = %s and CONCAT( s.first_name,' ',s.last_name) like %s GROUP BY s.student_id, r.term, r.due_date, r.report_id;""",
                                    (department_name, search_name,))

        select_result = connection1.fetchall()

        connection1.execute("""SELECT r.report_id, GROUP_CONCAT(CONCAT(sup.first_name, ' ', sup.last_name)) AS supervisor_names
                                        FROM 6_month_report r
                                        JOIN student_supervisor ss ON r.student_id = ss.student_id
                                        JOIN supervisor sup ON ss.supervisor_id = sup.supervisor_id
                                        LEFT JOIN sectionE e ON e.supervisor_id = sup.supervisor_id AND e.report_id = r.report_id
                                        WHERE e.report_id IS NULL AND r.report_progress_id =2
                                        GROUP BY r.report_id;""")
        supervisor_list = connection1.fetchall()

        for i in range(len(select_result)):
            supervisor_found = False
            for supervisor in supervisor_list:
                if select_result[i][-1] == supervisor[0]:
                    select_result[i] = select_result[i] + (supervisor[1],)
                    supervisor_found = True
                    break
            if not supervisor_found:
                select_result[i] = select_result[i] + (None,)

        if select_result == []:
            message = "Student is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "Students is found."
            alertStyling = "Green"

        return render_template("/admin/send_reminder.html", select_result=select_result, sort_depart=department_name,
                               message=message, alertStyling=alertStyling, report=report_status, current_date=current_date, active=active)

# Send reminders for all reports including overdue (Beibei and Sabrina)


@app_admin.route('/admin/send_reminder/submit', methods=['GET', 'POST'])
def send_reminder_submit():
    if request.method == 'POST':
        select_student = request.form.getlist('select_student')
        overdue_date = date.today()

        for student in select_student:
            # For date Only
            pattern = r"\((.*?), (.*?), (.*?), datetime\.date\((.*?)\)\)"
            matches = re.findall(pattern, student)

            if matches:
                match = matches[0]
                date_str = match[3]
                year, month, day = map(int, date_str.split(", "))
                overdue_date = datetime(year, month, day).date()

            # Remove parentheses and split strings with commas
            student = student.strip("()'")
            split_data = student.split(", ")

            # Extraction of segmented data
            student_id = int(split_data[0])
            charge_role = split_data[1].replace("'", "")
            student_name = split_data[2].replace("'", "")

            current_date = date.today()

            report_id = split_data[3].replace("'", "").replace(")", "")
            connection1 = getCursor()
            connection2 = getCursor()
            if charge_role == '1' or charge_role == 'None':
                con = getCursor()
                con.execute("""SELECT reminder_id FROM reminder JOIN student s ON reminder.user_id = s.user_id WHERE s.student_id = %s AND type='message';""",
                            (student_id,))
                reminder_exist = con.fetchall()
                if reminder_exist:
                    connection1.execute("""DELETE FROM reminder WHERE student_id = %s AND type='message';""",
                                        (student_id,))

                if overdue_date < current_date:
                    connection1.execute("""INSERT INTO reminder (user_id, student_id, reminder_info)
                        VALUES ((SELECT user_id FROM student WHERE student_id = %s), %s ,'Your report is now overdued! Please complete it as soon as possible');""",
                                        (student_id, student_id,))
                    for supervisor_type in ['main', 'associate', 'other']:
                        connection2.execute("""INSERT INTO reminder (user_id, student_id, reminder_info) 
                                            VALUES ((SELECT sup.user_id FROM supervisor sup join student_supervisor ss on ss.supervisor_id = sup.supervisor_id 
                                            where ss.student_id = %s and ss.supervisor_type = %s ),%s,"The report of student (%s) is now overdue and not completed, 
                                            please contact him/her to complete it as soon as possible.");""",
                                            (student_id,  supervisor_type, student_id, student_name,))

                elif charge_role == 'None':
                    connection1.execute("""INSERT INTO reminder (user_id, student_id, reminder_info)
                                            VALUES ((SELECT user_id FROM student WHERE student_id = %s), %s ,"You haven't started your report yet, please start it as soon as possible.");""",
                                        (student_id, student_id,))
                else:
                    connection1.execute("""INSERT INTO reminder (user_id,student_id,reminder_info)
                    VALUES ((SELECT user_id FROM student WHERE student_id = %s), %s,'Please complete your report as soon as possible.');""",
                                        (student_id, student_id,))

            elif charge_role == '2':
                # print("Student ID sup:", student_id)
                con = getCursor()
                con.execute("""SELECT reminder_id FROM reminder r JOIN supervisor sup ON sup.user_id = r.user_id
                            WHERE r.student_id = %s AND type='message';""",
                            (student_id,))
                reminder_exist = con.fetchall()
                if reminder_exist:
                    connection1.execute("""DELETE FROM reminder
                    WHERE user_id IN (SELECT user_id FROM supervisor WHERE user_id = reminder.user_id)
                    AND student_id = %s AND type = 'message';""",
                                        (student_id,))

                if overdue_date < current_date:
                    for supervisor_type in ['main', 'associate', 'other']:
                        connection1.execute("""INSERT INTO reminder (user_id, reminder_info,student_id) 
                                        VALUES ((SELECT sup.user_id FROM supervisor sup join student_supervisor ss on ss.supervisor_id = sup.supervisor_id 
                                        where ss.student_id = %s and ss.supervisor_type = %s ),"The report of student (%s) currently awaiting your attention, 
                                        so please deal with them promptly. This report is also overdued so please check it asap.",%s);""",
                                            (student_id, supervisor_type,  student_name, student_id,))
                else:
                    connection1.execute("""
                    INSERT INTO reminder (user_id,student_id, reminder_info)
                    SELECT sup.user_id, s.student_id, CONCAT('The report of student (', s.first_name, ' ', s.last_name, ') currently awaiting your attention, so please deal with them promptly.')
                    FROM supervisor sup
                    JOIN student_supervisor ss ON ss.supervisor_id = sup.supervisor_id
                    JOIN student s ON s.student_id = ss.student_id
                    WHERE ss.student_id = %s
                    AND sup.supervisor_id NOT IN (SELECT supervisor_id FROM sectionE WHERE report_id = %s);
                    """, (student_id, report_id, ))

            elif charge_role == '3':

                con = getCursor()
                con.execute("""SELECT reminder_id FROM reminder r JOIN user u ON u.user_id = r.user_id
                            WHERE u.user_role = 'convenor' AND r.student_id = %s AND r.type='message';""", (student_id,))
                reminder_exist = con.fetchall()
                if reminder_exist:
                    connection1.execute("""DELETE FROM reminder WHERE user_id IN (SELECT u.user_id
                    FROM user u WHERE u.user_role = 'convenor')AND student_id = %s
                    AND type = 'message';""", (student_id,))

                if overdue_date < current_date:
                    connection1.execute("""INSERT INTO reminder (user_id,student_id, reminder_info)
                 SELECT user_id,%s, "The report of student (%s) currently awaiting your attention and is now overdue, so please deal with them promptly." FROM user
                 WHERE department_id IN (SELECT department_id
                                        FROM (SELECT user.department_id
                                              FROM user JOIN student ON user.user_id = student.user_id
                                              WHERE student.student_id = %s) AS temp)
                 AND user_role = 'convenor';""", (student_id, student_name, student_id,))
                else:
                    connection1.execute("""INSERT INTO reminder (user_id,student_id, reminder_info)
                 SELECT user_id,%s, "The report of student (%s) currently awaiting your attention, so please deal with them promptly." FROM user
                 WHERE department_id IN (SELECT department_id
                                        FROM (SELECT user.department_id
                                              FROM user JOIN student ON user.user_id = student.user_id
                                              WHERE student.student_id = %s) AS temp)
                 AND user_role = 'convenor';""", (student_id, student_name, student_id,))

        message = 'Reminder has been sent successfully.'
        alertStyling = 'Green'

        return redirect(url_for('app_admin.send_reminder', message=message, alertStyling=alertStyling))

# Mark report as completed (Beibei)


@app_admin.route('/admin/mark_completed', methods=['GET', 'POST'])
def mark_completed():
    report_id = request.args.get('report_id')
    student_id = request.args.get('student_id')
    student_name = request.args.get('student_name')

    # Change the progress id of the report to 6
    connection = getCursor()
    connection.execute(
        """update 6_month_report set report_progress_id = 6 where report_id = %s;""", (report_id,))
    # Notify the student and his supervisor
    connection1 = getCursor()
    connection1.execute("""INSERT INTO reminder (user_id,student_id, reminder_info)
                        VALUES ((SELECT user_id FROM student WHERE student_id = %s),%s, 'Your report has been marked as completed by admin.');""",
                        (student_id, student_id,))
    current_time = datetime.now()
    # update database table `updated_time`
    connection1.execute(
        """UPDATE updated_time SET completed_date=%s WHERE report_id= %s;""", (current_time, report_id,))

    # Notify the chair if the student did section F
    connection2 = getCursor()
    connection2.execute("""SELECT id FROM sectionF f JOIN 6_month_report r ON f.report_id = r.report_id WHERE 
    r.report_progress_id = 6 AND f.report_id=%s;""", (report_id,))
    sectionF_exist = connection2.fetchall()
    if sectionF_exist:
        connection3 = getCursor()
        connection3.execute("""INSERT INTO reminder (user_id,student_id,reminder_info) VALUES ((SELECT user_id FROM 
        user WHERE user_role = 'chair'),%s, "Student (%s) has submitted section F of report, please deal with 
        it.");""", (student_id, student_name,))

    for supervisor_type in ['main', 'associate', 'other']:
        cur = getCursor()
        cur.execute("""SELECT supervisor_id FROM student_supervisor WHERE student_id = %s AND 
                        supervisor_type = %s;""", (student_id, supervisor_type,))
        supervisor_exist = cur.fetchall()
        if supervisor_exist:
            connection2 = getCursor()
            connection2.execute("""INSERT INTO reminder (user_id,student_id, reminder_info) 
                            VALUES ((SELECT sup.user_id FROM supervisor sup join student_supervisor ss on ss.supervisor_id = sup.supervisor_id 
                            where ss.student_id = %s and ss.supervisor_type = %s ),%s,"Your student, %s, has completed his/her report.");""",
                                (student_id, supervisor_type, student_id, student_name,))

    message = 'You have marked this report as completed and have notified the student and his supervisor.'
    alertStyling = "Green"

    return redirect(url_for('app_admin.send_reminder', message=message, alertStyling=alertStyling))

# Identify students with issues (Beibei)


@app_admin.route('/admin/issue_students', methods=['GET', 'POST'])
def issue_students():
    active = 'issue'  # For the left nav bar become active
    if request.method == 'GET':
        connection = getCursor()
        connection.execute("""SELECT s.student_id,CONCAT(s.first_name,' ', s.last_name), d.department_name, MAX(c.convenor_name), 
            GROUP_CONCAT(COALESCE(CONCAT(ss.supervisor_type, ': ', sup.first_name, ' ', sup.last_name), '') SEPARATOR ', '),
            CASE WHEN EXISTS(SELECT 1 FROM reminder JOIN staff ON reminder.user_id = staff.user_id  WHERE reminder.student_id = s.student_id and reminder.type='action') THEN 'Y' ELSE 'N' END AS has_reminder
        FROM student s LEFT JOIN user u ON s.user_id = u.user_id
        LEFT JOIN student_supervisor ss ON ss.student_id = s.student_id
        LEFT JOIN supervisor sup ON sup.supervisor_id = ss.supervisor_id
        LEFT JOIN department d ON d.department_id = u.department_id
        LEFT JOIN ( SELECT u.department_id, CONCAT(st.first_name, ' ', st.last_name) AS convenor_name
            FROM user u INNER JOIN staff st ON u.user_id = st.user_id WHERE u.user_role = 'convenor'
        ) AS c ON c.department_id = u.department_id
        GROUP BY s.student_id, d.department_name, c.department_id
        ORDER BY s.student_id;""")
        select_result = connection.fetchall()
        connection1 = getCursor()
        connection1.execute("""SELECT cr.student_id, pr.Convenors_to_complete,cr.term,cr.Convenors_to_complete
                FROM ( SELECT r.student_id, r.term, c.Convenors_to_complete FROM 6_month_report r LEFT JOIN sectionE_Convenor c ON c.report_id = r.report_id
                        WHERE r.term = (SELECT MAX(term) FROM 6_month_report WHERE student_id = r.student_id)) AS cr
                LEFT JOIN ( SELECT r.student_id, c.Convenors_to_complete FROM 6_month_report r
                            LEFT JOIN sectionE_Convenor c ON c.report_id = r.report_id
                            WHERE r.term = (SELECT MAX(term) - 1 FROM 6_month_report WHERE student_id = r.student_id)
                ) AS pr ON pr.student_id = cr.student_id WHERE cr.Convenors_to_complete != 'G';""")
        report_list = connection1.fetchall()

        message = request.args.get('message')
        alertStyling = "Green"

        return render_template('/admin/issue_students.html', select_result=select_result, report_list=report_list, message=message, alertStyling=alertStyling, active=active)

    elif request.method == 'POST':
        search = request.form.get('search')
        if search is None:
            search_name = '%%'
        else:
            search_name = "%" + search + "%"

        department_name = request.form.get('inputGroupSelect')
        if department_name is None:
            department_name = 'ALL'

        connection = getCursor()
        if department_name == 'ALL':
            connection.execute("""SELECT cr.student_id, pr.Convenors_to_complete,cr.term,cr.Convenors_to_complete,
            CONCAT(s.first_name, ' ', s.last_name) FROM ( SELECT r.student_id, r.term, c.Convenors_to_complete FROM 
            6_month_report r LEFT JOIN sectionE_Convenor c ON c.report_id = r.report_id WHERE r.term = (SELECT MAX(
            term) FROM 6_month_report WHERE student_id = r.student_id)) AS cr LEFT JOIN ( SELECT r.student_id, 
            c.Convenors_to_complete FROM 6_month_report r LEFT JOIN sectionE_Convenor c ON c.report_id = r.report_id 
            WHERE r.term = (SELECT MAX(term) - 1 FROM 6_month_report WHERE student_id = r.student_id) ) AS pr ON 
            pr.student_id = cr.student_id JOIN student s ON s.student_id = cr.student_id WHERE 
            cr.Convenors_to_complete != 'G' AND CONCAT(s.first_name, ' ', s.last_name) LIKE %s;""",
                               (search_name,))
        else:
            connection.execute("""SELECT cr.student_id, pr.Convenors_to_complete,cr.term,cr.Convenors_to_complete,CONCAT(s.first_name, ' ', s.last_name)
                        FROM ( SELECT r.student_id, r.term, c.Convenors_to_complete FROM 6_month_report r LEFT JOIN sectionE_Convenor c ON c.report_id = r.report_id
                                WHERE r.term = (SELECT MAX(term) FROM 6_month_report WHERE student_id = r.student_id)) AS cr
                        LEFT JOIN ( SELECT r.student_id, c.Convenors_to_complete FROM 6_month_report r
                                    LEFT JOIN sectionE_Convenor c ON c.report_id = r.report_id
                                    WHERE r.term = (SELECT MAX(term) - 1 FROM 6_month_report WHERE student_id = r.student_id)
                        ) AS pr ON pr.student_id = cr.student_id JOIN student s ON s.student_id = cr.student_id 
                        JOIN user ON s.user_id = user.user_id JOIN department d ON d.department_id = user.department_id
                        WHERE cr.Convenors_to_complete != 'G' AND d.department_name = %s AND CONCAT(s.first_name, ' ', s.last_name) LIKE %s;""",
                               (department_name, search_name,))

        report_list = connection.fetchall()
        connection1 = getCursor()
        connection1.execute("""SELECT s.student_id,CONCAT(s.first_name,' ', s.last_name), d.department_name, MAX(c.convenor_name), 
            GROUP_CONCAT(COALESCE(CONCAT(ss.supervisor_type, ': ', sup.first_name, ' ', sup.last_name), '') SEPARATOR ', '),
            CASE WHEN EXISTS(SELECT 1 FROM reminder JOIN staff ON reminder.user_id = staff.user_id WHERE reminder.student_id = s.student_id) THEN 'Y' ELSE 'N' END AS has_reminder
            FROM student s LEFT JOIN user u ON s.user_id = u.user_id
            LEFT JOIN student_supervisor ss ON ss.student_id = s.student_id
            LEFT JOIN supervisor sup ON sup.supervisor_id = ss.supervisor_id
            LEFT JOIN department d ON d.department_id = u.department_id
            LEFT JOIN ( SELECT u.department_id, CONCAT(st.first_name, ' ', st.last_name) AS convenor_name
                FROM user u INNER JOIN staff st ON u.user_id = st.user_id WHERE u.user_role = 'convenor'
            ) AS c ON c.department_id = u.department_id
            GROUP BY s.student_id, d.department_name, c.department_id
            ORDER BY s.student_id;""")
        select_result = connection1.fetchall()
        if report_list == []:
            message = "Student is not found. Please try again!"
            alertStyling = "Red"
        else:
            message = "Students are found."
            alertStyling = "Green"

        return render_template("/admin/issue_students.html", select_result=select_result, report_list=report_list, sort_depart=department_name,
                               message=message, alertStyling=alertStyling, active=active)

# Action page for students with issues (Beibei)


@app_admin.route('/admin/action', methods=['GET', 'POST'])
def action_for_issues():
    student_id = request.args.get("student_id")
    active = 'issue'  # For the left nav bar become active
    if request.method == 'GET':
        last_report = request.args.get("last_report")
        cur_report = request.args.get("cur_report")
        student_name = request.args.get("student_name")
        report_type = request.args.get("report_type")
        action_type = ''
        reminder_content = 'Some text...'
        if cur_report == 'O':
            action_type = 1
            reminder_content = "The Student " + student_name + \
                "'s status for this report (" + report_type + \
                ") is yellow, please follow up with the student's supervisors as soon as possible."
            if last_report == 'O':
                action_type = 3
                reminder_content = "The Student (" + student_name + ") have a yellow status of current report (" + report_type + \
                    ") and last report, the student is slow and should meet with the PG convenor as soon as possible."
        elif cur_report == 'R':
            action_type = 2
            reminder_content = "Student (" + student_name + ")'s status for this report (" + report_type + \
                ") is red and the student and PG convenor should arrange a meeting as soon as possible."
        return render_template('/admin/take_actions.html', action_type=action_type, reminder_content=reminder_content, student_name=student_name, active=active)

    elif request.method == 'POST':
        action_type = request.form.get("action_type")
        content = request.form.get("content")
        connection1 = getCursor()
        connection1.execute("""INSERT INTO reminder (user_id, student_id,type,reminder_info) 
                            SELECT user_id, %s,'action', %s FROM user 
                            WHERE department_id IN (SELECT department_id 
                                                   FROM (SELECT user.department_id 
                                                         FROM user JOIN student ON user.user_id = student.user_id 
                                                         WHERE student.student_id = %s) AS temp) 
                            AND user_role = 'convenor';""", (student_id, content, student_id,))
        if action_type == '3':
            connection2 = getCursor()
            connection2.execute("""INSERT INTO reminder (user_id,student_id, type,reminder_info)
                                   VALUES ((SELECT user_id FROM student WHERE student_id = %s),%s,'action', %s);""",
                                (student_id, student_id, content,))

        message = 'The content of the action has been successfully sent.'
        return redirect(url_for('app_admin.issue_students', message=message))
