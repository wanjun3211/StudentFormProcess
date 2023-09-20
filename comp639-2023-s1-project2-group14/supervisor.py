# This is the supervisor's python file which consists of the following user stories:
# - View supervisees
# - Manage supervisees (where main supervisor needs to check the student's submission before other supervisors can fill in section E)
# - Fill in Section E
# - View personal info and edit

# Initial Setup
from flask import Blueprint, render_template, request, url_for, redirect
import re
from datetime import datetime, date
import mysql.connector
from mysql.connector import FieldType
import connect


import re
from datetime import datetime, date
import mysql.connector
from mysql.connector import FieldType
import connect

app_supervisor = Blueprint('app_supervisor', __name__)

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


# for show a list for all supervisees' info (By Beibei)
@app_supervisor.route('/supervisor/supervisee', methods=['GET', 'POST'])
def supervisee():
    user_id = request.cookies.get('user_id')
    active = 'supervisee'
    if request.method == 'GET':
        search_name = "%%"
        message = ""
        alertStyling = ""

    elif request.method == 'POST':
        search = request.form.get('search')
        if search != None:
            search_name = "%" + search + "%"
        else:
            search_name = "%%"

    connection = getCursor()
    connection.execute("""select s.student_id,CONCAT(s.first_name,' ', s.last_name), u.email_address,d.department_name,s.phone, UCASE(supervisor_type)
            FROM student AS s
            INNER JOIN student_supervisor AS ss ON s.student_id = ss.student_id
            INNER JOIN supervisor AS sp ON ss.supervisor_id = sp.supervisor_id
            INNER JOIN user AS u ON s.user_id = u.user_id
            INNER JOIN department AS d ON u.department_id = d.department_id
            where sp.user_id = %s and CONCAT( s.first_name,' ',s.last_name) like %s;""",
                       (user_id, search_name,))

    select_result = connection.fetchall()
    if select_result == [] and request.method == 'POST':
        message = "Student is not found. Please try again!"
        alertStyling = "Red"
    elif select_result and request.method == 'POST':
        message = "Student is found."
        alertStyling = "Green"

    return render_template("/supervisor/supervisee.html", select_result=select_result, message=message, alertStyling=alertStyling, active=active)

# View supervisee's details


@app_supervisor.route('/supervisor/supervisee_detail', methods=['GET', 'POST'])
def supervisee_detail():
    active = 'supervisee'
    if request.method == 'POST':
        student_id = request.form.get("student_id")

        connection = getCursor()
        connection.execute("""select s.first_name, s.last_name, user.email_address, department_name,enrolment_date, address, s.phone,part_full_time, thesis_title from student s
            left join user on user.user_id = s.user_id
            left join department on department.department_id = user.department_id
            where s.student_id = %s group by s.student_id;""",
                           (student_id,))

    select_result = connection.fetchall()

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
    return render_template("/supervisor/supervisee_detail.html", students_list=select_result, supervisor_list=supervisor_list, active=active)

# View supervisees' list of reports (Sabrina)


@app_supervisor.route('/supervisor/view_reports', methods=['GET', 'POST'])
def view_reports():
    user_id = request.cookies.get('user_id')
    supervisor_role = ''
    message = request.args.get('message')
    alertStyling = request.args.get('alertStyling')
    cur = getCursor()
    active = 'supervisee'

    if request.method == 'POST':
        student_id = request.form.get("ID")
        if 'confirm-reject' in request.form:
            report_id = request.args.get('report_id')
            cur.execute(
                """select student_id from 6_month_report where report_id = %s;""", (report_id,))
            student_id = cur.fetchall()
            student_id = student_id[0][0]

            result = request.form.get("confirmation")

            reject_message = request.form.get("reject_message")

            if result == 'confirm':
                cur.execute(
                    """update 6_month_report set main_check = 'confirm' where report_id = %s;""", (report_id,))
                message = 'Student report has been checked'
                alertStyling = 'Green'

                # Send a reminder to all supervisors of the student to remind them that can start to fill in the report.
                cur.execute("""INSERT INTO reminder (user_id,student_id, reminder_info)
                                    SELECT sup.user_id,%s, CONCAT('The student (', s.first_name, ' ', s.last_name, ') has submitted his/her report, so please fill in the sectionE of the report.')
                                    FROM supervisor sup
                                    JOIN student_supervisor ss ON ss.supervisor_id = sup.supervisor_id
                                    JOIN student s ON s.student_id = ss.student_id
                                    WHERE ss.student_id = %s;
                                    """, (student_id, student_id,))

            elif result == 'reject':
                # Back to student + message
                cur.execute(
                    """update 6_month_report set main_check = 'reject',main_message = %s, report_progress_id= 1 where report_id = %s;""",
                    (reject_message, report_id,))

                # Update the sectionF submit button.
                cur.execute(
                    """update sectionF set content_status = 'draft' where report_id = %s;""",
                    (report_id,))

                message = 'Student report has been rejected and the student has been notified'
                alertStyling = 'Red'

    elif request.method == 'GET':
        report_id = request.args.get('report_id')

        cur.execute(
            """select student_id from 6_month_report where report_id = %s;""", (report_id,))
        student_id = cur.fetchall()
        student_id = student_id[0][0]

    # Determine if sectionE has been completed by this supervisor.(BY beibei)
    cur.execute(
        """SELECT r.report_id, r.report_progress_id, r.due_date, r.term, r.main_check,
       CASE WHEN e.report_id IS NOT NULL THEN 'Yes' ELSE 'No' END AS supervisor_present
        FROM 6_month_report r LEFT JOIN sectionE e ON e.report_id = r.report_id AND e.supervisor_id = (
    SELECT supervisor_id FROM supervisor WHERE user_id = %s) WHERE r.student_id = %s;;""", (user_id, student_id,))
    report_list = cur.fetchall()

    cur.execute(
        """SELECT concat(first_name,' ',last_name) FROM student where student_id = %s;""", (student_id,))
    current_supervisee = cur.fetchall()

    # Get students' supervisor list and check if the current supervisor's user id is in the list and what type
    cur.execute("""
    select concat(sp.first_name,' ',sp.last_name), supervisor_type, u.user_id from student s
    inner join student_supervisor ss on s.student_id = ss.student_id
    inner join supervisor sp on ss.supervisor_id = sp.supervisor_id
    inner join user u on u.user_id = sp.user_id
    where s.student_id = %s;""", (student_id,))
    student_supervisors = cur.fetchall()

    # filter through to find current supervisor's type
    for supervisor in student_supervisors:

        if supervisor[2] == int(user_id):
            if supervisor[1] == 'main':
                supervisor_role = 'main'
            elif supervisor[1] == 'associate':
                supervisor_role = 'associate'
            elif supervisor[1] == 'other':
                supervisor_role = 'other'

    return render_template("/supervisor/view_reports.html", report_list=report_list,
                           current_supervisee=current_supervisee, supervisor_role=supervisor_role,
                           message=message, alertStyling=alertStyling, active=active)

# View personal info for the supervisor


@app_supervisor.route('/supervisor/profile')
def supervisor_profile():
    user_email = request.cookies.get('user_email')
    connection = getCursor()
    connection.execute("select s.first_name, s.last_name, d.department_name, u.email_address, s.phone from supervisor as s inner join user as u on s.user_id = u.user_id \
                        inner join department as d on u.department_id=d.department_id where u.email_address =%s;", (user_email,))
    profile_data = connection.fetchall()
    active = 'sup_profile'
    return render_template("/supervisor/personalinfo.html", profile_Data=profile_data, user_Email=user_email, active=active)

# Be able to edit personal info


@app_supervisor.route('/supervisor/profile/edit', methods=['POST'])
def supervisor_profile_edit():
    active = 'sup_profile'
    user_email = request.cookies.get('user_email')
    connection = getCursor()
    connection.execute("select s.first_name, s.last_name, d.department_name, u.email_address, s.phone from supervisor as s inner join user as u on s.user_id = u.user_id \
                        inner join department as d on u.department_id=d.department_id where u.email_address =%s;", (user_email,))
    profile_data = connection.fetchall()

    connection.execute("SELECT * FROM 639_lu.department;")
    departm_infor = connection.fetchall()

    return render_template("/supervisor/personalinfo_edit.html", profile_Data=profile_data, user_Email=user_email, departm_Infor=departm_infor, active=active)

# Submitting updated info


@app_supervisor.route('/supervisor/profile_editted', methods=['POST'])
def update_member_profile_edit():
    user_email = request.cookies.get('user_email')
    new_depm = request.form.get('Departm')
    new_phone = request.form.get('Phone')
    connection = getCursor()
    connection.execute(
        "SELECT user_id FROM user where email_address =%s;", (user_email,))

    # get the user ID for update corresponding row
    result = connection.fetchall()
    user_id = result[0][0]

    # udpate phone and department, and department is updated by the newest department ID number
    connection.execute(
        "UPDATE supervisor SET phone=%s WHERE user_id= %s;", (new_phone, user_id))
    connection.execute(
        "UPDATE user SET department_id=%s WHERE user_id= %s;", (new_depm, user_id))

    connection = getCursor()
    connection.execute("select s.first_name, s.last_name, d.department_name, u.email_address, s.phone from supervisor as s inner join user as u on s.user_id = u.user_id \
                        inner join department as d on u.department_id=d.department_id where u.email_address =%s;", (user_email,))
    profile_data = connection.fetchall()
    active = 'sup_profile'
    return render_template("/supervisor/personalinfo.html", profile_Data=profile_data, user_Email=user_email, active=active)

# Fill in section E as a supervisor (Beibei)


@app_supervisor.route('/supervisor/sectionE', methods=['GET', 'POST'])
def fill_sectionE():
    user_name = request.cookies.get('user_name')
    user_id = request.cookies.get('user_id')
    section = 'sectionE'
    if request.method == 'GET':
        report_id = request.args.get('report_id')
        role = request.args.get('role')
        connection1 = getCursor()
        connection1.execute(
            """SELECT CONCAT(s.first_name,' ',s.last_name),s.student_id from 6_month_report r
            JOIN student s ON s.student_id=r.student_id where r.report_id = %s;""",
            (report_id,))
        student_info = connection1.fetchall()

        return render_template("/supervisor/sectionE.html", student_info=student_info, user_name=user_name,
                               report_id=report_id, role=role, section=section)
    elif request.method == 'POST':
        report_id = request.form.get('report_id')
        supervisor_answer1 = request.form.get('supervisor_answer1')
        supervisor_answer2 = request.form.get('supervisor_answer2')
        supervisor_answer3 = request.form.get('supervisor_answer3')
        supervisor_answer4 = request.form.get('supervisor_answer4')
        supervisor_answer5 = request.form.get('supervisor_answer5')
        supervisor_response = request.form.get('progress_review')
        supervisor_comments = request.form.get('supervisor_comments')
        connection1 = getCursor()
        connection1.execute("""INSERT INTO sectionE (supervisor_id, report_id, supervisor_answer1, supervisor_answer2, supervisor_answer3, supervisor_answer4, supervisor_answer5, supervisor_response, supervisor_comments)
                VALUES((SELECT supervisor_id FROM supervisor WHERE user_id = %s), %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (user_id, report_id, supervisor_answer1, supervisor_answer2, supervisor_answer3,
                             supervisor_answer4, supervisor_answer5, supervisor_response, supervisor_comments,))

        message = "You have completed sectionE of report."
        alertStyling = "Green"
        current_datetime = datetime.now()
        connection2 = getCursor()
        connection2.execute("""select supervisor_type from supervisor sup 
        join user u on u.user_id = sup.user_id
        join student_supervisor ss on sup.supervisor_id=ss.supervisor_id
        join 6_month_report r on r.student_id = ss.student_id where r.report_id = %s and sup.user_id = %s;""",
                            (report_id, user_id,))
        supervisor_type = connection2.fetchall()
        if supervisor_type:
            supervisor_role = supervisor_type[0][0]

        if supervisor_role == 'main':
            connection2.execute("""UPDATE updated_time SET sec_E_main = %s WHERE report_id = %s; """,
                                (current_datetime, report_id,))
        elif supervisor_role == 'associate':
            connection2.execute("""UPDATE updated_time SET sec_E_associate = %s WHERE report_id = %s; """,
                                (current_datetime, report_id,))
        elif supervisor_role == 'other':
            connection2.execute("""UPDATE updated_time SET sec_E_other = %s WHERE report_id = %s; """,
                                (current_datetime, report_id,))

        # When all supervisors have filled out section E, the report process is passed to the convenor and a reminder is sent to him.
        connection3 = getCursor()
        connection3.execute("""SELECT sup.supervisor_id FROM supervisor sup JOIN student_supervisor ss ON 
        ss.supervisor_id = sup.supervisor_id JOIN student s ON s.student_id = ss.student_id
        JOIN 6_month_report r ON r.student_id = s.student_id WHERE r.report_id = %s 
        AND sup.supervisor_id NOT IN (SELECT supervisor_id FROM sectionE WHERE report_id = %s) """,
                            (report_id, report_id,))
        supervisor_id = connection3.fetchall()
        if not supervisor_id:
            connection3.execute(
                """update 6_month_report set report_progress_id = 3 where report_id = %s;""", (report_id,))
            connection4 = getCursor()
            connection4.execute("""INSERT INTO reminder (user_id, student_id,reminder_info)
            SELECT u.user_id, r.student_id,  CONCAT("You can start to grade the student's (", r.first_name, ' ', r.last_name, ") report.")
            FROM user u JOIN ( SELECT department_id FROM (
            SELECT user.department_id FROM user JOIN student s ON user.user_id = s.user_id JOIN 6_month_report r ON r.student_id = s.student_id
            WHERE r.report_id = %s) AS temp) AS d ON u.department_id = d.department_id
            JOIN (SELECT r.student_id ,s.first_name,s.last_name FROM 6_month_report r JOIN student s ON r.student_id = s.student_id WHERE r.report_id = %s) AS r ON u.user_role = 'convenor'
            WHERE u.user_role = 'convenor';""", (report_id, report_id,))

        return redirect(
            url_for('app_supervisor.view_reports', message=message, alertStyling=alertStyling, report_id=report_id))
