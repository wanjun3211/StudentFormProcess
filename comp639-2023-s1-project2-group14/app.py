# This is the main python file for the system which consists of the login system, reminder system and view reports sections

# Import separated views
from student import app_student
from supervisor import app_supervisor
from convenor import app_convenor
from admin import app_admin
from chair import app_chair

# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from forms import SignUpForm

# From previous Project 1
from flask.helpers import make_response
from datetime import datetime, date
from decimal import Decimal
import re
import mysql.connector
from mysql.connector import FieldType
import connect

# create the application object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'


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


# Route for handling the login page logic
user_role = None
user_email = None
user_password = None
user_name = None
user_id = None
double_role = None

# create app and separated views
app.register_blueprint(app_student)
app.register_blueprint(app_supervisor)
app.register_blueprint(app_convenor)
app.register_blueprint(app_admin)
app.register_blueprint(app_chair)


@app.context_processor
def inject_user():
    global user_role
    global user_email
    global user_password
    global user_name
    global user_id
    global double_role
    return dict(user_role=user_role, user_email=user_email, user_password=user_password, user_name=user_name, user_id=user_id, double_role=double_role)


# For Registrations - Sign up to the system (Sabrina)
temp_mainsupervisor = []


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    global temp_mainsupervisor
    if request.method == "POST":
        if form.validate_on_submit():

            # # Get the form data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            # get existing email addresses from database to check whether the email has been registered
            connection = getCursor()
            connection.execute("""SELECT email_address from user;""")
            all_emails = connection.fetchall()

            # check if user input is in the list of emails above
            for database_email in all_emails:
                if database_email[0] == email:

                    message = "This email has been registered. Please try again with another email, thank you!"
                    alertStyling = "Red"
                    return render_template('signup.html', form=form, message=message, alertStyling=alertStyling)

            # if email input does not match all_emails, then we continue to insert the user
            cur = getCursor()
            cur.execute(
                f"""INSERT INTO user (email_address, password,user_role,admin_reviewed) VALUES ('{email}','{password}','student',0);""")

            cur2 = getCursor()
            cur2.execute(
                f"""select user_id from user where email_address = '{email}';""")
            currentUserid = cur2.fetchall()

            cur3 = getCursor()

            cur3.execute(
                f"""INSERT INTO student (first_name,last_name,user_id) VALUES ('{first_name}','{last_name}','{currentUserid[0][0]}');""")

            # Supervisor details to check for later and only if currentuserid is not empty
            if currentUserid != '':
                temp_mainsupervisor.append(
                    (currentUserid[0][0], form.main_supervisor.data))

            alertStyling = "Green"
            message = "Sign up for successfully. Please wait for a confirmation email before logging into the system. Thank you!"
            return render_template('signup.html', form=form, message=message, alertStyling=alertStyling)

    return render_template('signup.html', form=form)

# Login System (Sabrina)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email_input = request.form.get('user_email')
        user_password_input = request.form.get('user_password')

        # Established database connection
        cur = getCursor()
        cur.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user 
        inner join student on user.user_id = student.user_id
        UNION
        select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
        inner join supervisor on user.user_id = supervisor.user_id
        UNION
        select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
        inner join staff on user.user_id = staff.user_id;""")
        users = cur.fetchall()

        # For unconfirmed queries, not allowed to log in
        cur2 = getCursor()
        cur2.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user 
        inner join student on user.user_id = student.user_id
        where admin_reviewed = 0
        UNION
        select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
        inner join supervisor on user.user_id = supervisor.user_id
        where admin_reviewed = 0
        UNION
        select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user
        inner join staff on user.user_id = staff.user_id
        where admin_reviewed = 0;""")
        unconfirmedlist = cur2.fetchall()

        # For rejected users, not allowed to log in and different message needed
        cur3 = getCursor()
        cur3.execute("""select first_name,last_name,email_address,password,user_role,admin_reviewed,user.user_id from user 
        inner join student on user.user_id = student.user_id
        where admin_reviewed = 0 and admin_reject = 1;""")
        rejected_student_list = cur3.fetchall()

        # Check whether email and password is in the database
        for user in users:

            if user_email_input == user[2] and user_password_input == user[3]:
                user_name = str(user[0] + " " + user[1])
                user_role = str(user[4])
                user_email = str(user[2])
                user_password = str(user[3])
                user_id = str(user[6])
                double_role = 'No'
                if user_role == 'convenor':
                    connection1 = getCursor()
                    connection1.execute(
                        """select supervisor_id from supervisor where user_id=%s;""", (user_id,))
                    supervisor_check = connection1.fetchall()
                    if supervisor_check:
                        double_role = 'Yes'

            # If the user is a student and in the rejected list, they are prevented to log in
                for student in rejected_student_list:
                    if student[2] == user_email_input:
                        return render_template('login.html', error_msg="Your account has been rejected. Please contact an admin to resolve the issue(s). Thank you!")

            # If the user is in the unconfirmed list, they are prevented from logging in
                for user in unconfirmedlist:
                    if user[2] == user_email_input:
                        return render_template('login.html', error_msg="Sorry, your account has not been confirmed, please wait till you have a confirmation email.")

            # If they are not in the unconfirmed list, data will be stored so they are logged in
                resp = make_response(redirect('/'))
                resp.set_cookie('user_name', user_name)
                resp.set_cookie('user_email', user_email)
                resp.set_cookie('user_password', user_password)
                resp.set_cookie('user_role', user_role)
                resp.set_cookie('user_id', user_id)
                resp.set_cookie('double_role', double_role)
                return resp
            elif user_email_input == '' or user_password_input == '':
                return render_template('login.html', error_msg="Please enter both email and password to log in.")

        return render_template('login.html', error_msg="You have entered the incorrect email or password. Please try again.")

    return render_template('login.html')

# Log out (Sabrina)


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('user_role')
    resp.delete_cookie('user_email')
    resp.delete_cookie('user_pasword')
    resp.delete_cookie('user_name')
    resp.delete_cookie('user_id')
    resp.delete_cookie('double_role')
    global user_role
    global user_email
    global user_password
    global user_name
    global user_id
    global double_role
    user_role = None
    user_email = None
    user_password = None
    user_name = None
    user_id = None
    double_role = None
    return resp

# Index Page (Sabrina)


@app.route("/")
def index():
    global user_role
    global user_email
    global user_password
    global user_name
    global user_id
    global double_role
    user_role = request.cookies.get('user_role')
    user_email = request.cookies.get('user_email')
    user_password = request.cookies.get('user_password')
    user_name = request.cookies.get('user_name')
    user_id = request.cookies.get('user_id')
    double_role = request.cookies.get('double_role')
    reminder_result = ''
    report_check = ''
    reject_message = ''
    confirm_message = ''
    active = 'home'  # For the left nav bar become active
    if request.method == 'GET':
        if user_id:
            connection1 = getCursor()
            connection1.execute(
                """SELECT reminder_id,type,reminder_info FROM reminder WHERE user_id = %s;""", (user_id,))
            reminder_result = connection1.fetchall()

            connection2 = getCursor()
            connection2.execute("""select report_id, main_check,main_message, term from 6_month_report r 
            inner join student s on r.student_id = s.student_id 
            inner join user u on s.user_id = u.user_id
            where u.user_id = %s;""", (user_id,))
            report_check = connection2.fetchall()
            active = 'home'  # For the left nav bar become active

            for item in report_check:
                if item[1] == 'reject':
                    reject_message = 1
                elif item[1] == 'confirm':
                    confirm_message = 1

    return render_template('index.html', reminder_result=reminder_result, report_check=report_check, active=active, reject_message=reject_message, confirm_message=confirm_message)

# Reminder banner (Beibei)


@app.route("/reminder", methods=['GET', 'POST'])
def reminder():
    reminder_id = request.args.get('reminder_id')
    connection = getCursor()
    connection.execute("""DELETE FROM reminder
                       WHERE reminder_id = %s;""", (reminder_id,))
    return redirect(url_for('index'))


@app.route("/acknowledge", methods=['GET', 'POST'])
def acknowledge():
    report_id = request.args.get('report_id')
    action = request.args.get('action')
    term = request.args.get('term')
    connection = getCursor()

    if action == 1:
        connection.execute("""update 6_month_report set main_check = 'in progress'
        where report_id = %s;""", (report_id,))

    else:
        connection.execute("""update 6_month_report set main_check = 'checked', main_message = null where 
        report_id = %s;""", (report_id,))

    return redirect(url_for('index'))

# Below are all sections of the report for viewing function. This is added in the app.py file
# multiple users in the system has this functionality. Therefore, we chose to put this in the shared
# main file so there is no duplicate code.

# Done by Beibei


@app.route("/view_report/sectionA", methods=['GET', 'POST'])
def report_sectionA():
    section = 'sectionA'
    report_id = request.args.get('report_id')
    term = request.args.get('term')
    routing = request.args.get('routing')
    # Get to users' personal information
    connection1 = getCursor()
    connection1.execute("""select CONCAT(s.first_name,' ', s.last_name), s.student_id,enrolment_date, address, s.phone,email_address,part_full_time,thesis_title 
    from student s left join 6_month_report r on s.student_id = r.student_id
    left join user on user.user_id = s.user_id
                    where r.report_id = %s;""",
                        (report_id,))
    students_list = connection1.fetchall()
    # Get to users' supervisor information
    supervisor_list = []
    for supervisor_type in ['main', 'associate', 'other']:
        connection2 = getCursor()
        connection2.execute("""select CONCAT(supervisor.first_name,' ',supervisor.last_name) from student_supervisor 
                            join supervisor on student_supervisor.supervisor_id = supervisor.supervisor_id
                            join student on student_supervisor.student_id = student.student_id
                            join 6_month_report r on student.student_id = r.student_id
                            where r.report_id = %s and supervisor_type = %s ;""", (report_id, supervisor_type,))
        supervisor = connection2.fetchall()
        if not supervisor:
            supervisor_list.append('')
        else:
            supervisor_list.append(supervisor[0][0])
    # Get to users' scholarship information
    connection3 = getCursor()
    connection3.execute("""select scholar_name,scholar_value,scholar_tenure,scholar_end_date,content_status,scholar_id from sectionA_scholar join 6_month_report on sectionA_scholar.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id 
                    where 6_month_report.report_id = %s;""",
                        (report_id,))
    scholar_list = connection3.fetchall()
    # Get to users' employment information
    connection4 = getCursor()
    connection4.execute("""select sectionA_employment.report_id,teaching,research,other,content_status,id from sectionA_employment join 6_month_report on sectionA_employment.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id 
                    where 6_month_report.report_id = %s;""",
                        (report_id,))
    employment_list = connection4.fetchall()
    return render_template("report/sectionA.html", students_list=students_list, supervisor_list=supervisor_list, scholar_list=scholar_list, employment_list=employment_list, report_id=report_id, term=term, section=section, routing=routing)


@app.route("/view_report/sectionB", methods=['GET', 'POST'])
def report_sectionB():
    section = 'sectionB'
    report_id = request.args.get('report_id')
    term = request.args.get('term')
    routing = request.args.get('routing')
    # Get the report's sectionB information
    connection1 = getCursor()
    connection1.execute("""select sectionB_1.report_id, induction_program, Mutual_expectation, MEA, Intellectual_Property, Thesis_proposal_seminar, Research_proposal_approved, 
               PG_conference_presentation, Thesis_Results_Seminar,content_status from sectionB_1 join 6_month_report on sectionB_1.report_id = 6_month_report.report_id
                       join student on student.student_id = 6_month_report.student_id 
                       where 6_month_report.report_id = %s;""",
                        (report_id,))
    sectionB_1_list = connection1.fetchall()
    if sectionB_1_list:
        sectionB_1 = sectionB_1_list[0]
    else:
        sectionB_1 = []

    connection2 = getCursor()
    connection2.execute("""select sectionB_2_committee.report_id,Human_Ethics, Health_and_Safety, Animal_Ethics, Institutional_Biological_Safety, Radiation_Protection_Officer,content_status from sectionB_2_committee 
               join 6_month_report on sectionB_2_committee.report_id = 6_month_report.report_id
                       join student on student.student_id = 6_month_report.student_id 
                       where 6_month_report.report_id = %s;""",
                        (report_id,))
    sectionB_2_list = connection2.fetchall()
    if sectionB_2_list:
        sectionB_2 = sectionB_2_list[0]
    else:
        sectionB_2 = []

    return render_template("report/sectionB.html", sectionB_1=sectionB_1, sectionB_2=sectionB_2, report_id=report_id, term=term, section=section, routing=routing)


@app.route("/view_report/sectionC", methods=['GET', 'POST'])
def report_sectionC():
    section = 'sectionC'
    report_id = request.args.get('report_id')
    term = request.args.get('term')
    routing = request.args.get('routing')
    # Grab existing values from section C part 1
    cur = getCursor()
    cur.execute("""select Access_Psuper, Access_Asuper, Psuper_expertise, Asuper_expertise,
        Qua_Psuper, Qua_Asuper, TL_Psuper, TL_Asuper, Courses_avail, Workspace, Com_facility,
        ITS_support, Res_software, Lib_facility, T_L_cen_support, Stat_support,Res_equipment,Tech_support,Finan_resources
        from sectionc_1 where report_id = %s;""", (report_id,))
    sectionc_part1 = cur.fetchall()

    cur.execute(
        """select other_title, other, comment from sectionC_1_other where report_id = %s;""", (report_id,))
    sectionc_part1_other = cur.fetchall()

    # Grab existing comments from section C part 1 comments
    cur.execute("""select comment_1, comment_2,comment_3,comment_4,comment_5, comment_6,comment_7, comment_8, comment_9,comment_10,
        comment_11, comment_12, comment_13, comment_14, comment_15, comment_16, comment_17, comment_18, comment_19 from sectionc_1
        where report_id = %s;""", (report_id,))
    sectionc_part1_comments = cur.fetchall()
    if sectionc_part1_comments:
        part1_comments = sectionc_part1_comments[0]
    else:
        part1_comments = ''
    # Grab any existing values available for the currently form for section C part 2
    cur.execute(
        """select meeting_frequ, period_feedback from sectionc_2 where report_id = %s; """, (report_id,))
    sectionc_part2 = cur.fetchall()
    # grab only receive_feedback
    cur.execute(
        """select receive_feedback from sectionc_2_receive_feedback where report_id = %s; """, (report_id,))
    sectionc_part2_feedback = cur.fetchall()

    return render_template("report/sectionC.html", report_id=report_id, sectionc_part1=sectionc_part1,  part1_comments=part1_comments, sectionc_part2=sectionc_part2, sectionc_part2_feedback=sectionc_part2_feedback, term=term, section=section, sectionc_part1_other=sectionc_part1_other, routing=routing)


@app.route("/view_report/sectionD", methods=['GET', 'POST'])
def report_sectionD():
    section = 'sectionD'
    report_id = request.args.get('report_id')
    term = request.args.get('term')
    routing = request.args.get('routing')
    connection1 = getCursor()
    connection1.execute(
        """select obj_content, status, comment, obj_change_reason from sectiond_1_objective where report_id = %s;""",
        (report_id,))
    objectives = connection1.fetchall()

    connection1.execute(
        """select comment from sectiond_2_covid where report_id = %s;""", (report_id,))
    covids = connection1.fetchall()

    connection1.execute(
        """select achievement from sectiond_3_achievements where report_id = %s;""", (report_id,))
    achievements = connection1.fetchall()

    connection1.execute(
        """select * from sectiond_4_objective where report_id = %s;""", (report_id,))
    sec4_obejcitves = connection1.fetchall()

    connection1.execute(
        """select * from sectiond_4_objective where report_id = %s;""", (report_id,))
    sec4_obejcitves = connection1.fetchall()

    connection1.execute(
        """select * from sectiond_5_objective where report_id = %s;""", (report_id,))
    sec5_obejcitves = connection1.fetchall()
    return render_template("report/sectionD.html", section=section, Objectives=objectives, report_id=report_id, Covids=covids, Achievements=achievements,
                           Sec4_obejcitves=sec4_obejcitves, Sec5_obejcitves=sec5_obejcitves, term=term, routing=routing)


@app.route("/view_report/sectionE", methods=['GET', 'POST'])
def report_sectionE():
    section = 'sectionE'
    report_id = request.args.get('report_id')
    term = request.args.get('term')
    routing = request.args.get('routing')
    connection1 = getCursor()

    connection1.execute(
        """SELECT CONCAT(s.first_name,' ',s.last_name),s.student_id from 6_month_report r
        JOIN student s ON s.student_id=r.student_id where r.report_id = %s;""",
        (report_id,))
    student_info = connection1.fetchall()

    connection1.execute(
        """SELECT CONCAT(supervisor.first_name,' ',supervisor.last_name), supervisor_answer1, supervisor_answer2, supervisor_answer3, supervisor_answer4, supervisor_answer5, supervisor_response, supervisor_comments 
        from sectionE JOIN supervisor ON sectionE.supervisor_id=supervisor.supervisor_id where report_id = %s;""",
        (report_id,))
    sectionE_list = connection1.fetchall()

    connection1.execute(
        """SELECT CONCAT(staff.first_name,' ',staff.last_name), Convenor_highlight, Convenors_to_complete
        FROM sectionE_Convenor c JOIN staff ON c.user_id = staff.user_id 
        where c.report_id = %s;""", (report_id,))

    sectionE_convenor = connection1.fetchall()

    return render_template("report/sectionE.html", section=section, sectionE_list=sectionE_list, report_id=report_id, term=term, student_info=student_info, sectionE_convenor=sectionE_convenor, routing=routing)


@app.route("/view_report/sectionF", methods=['GET', 'POST'])
def report_sectionF():
    user_role = request.cookies.get('user_role')
    section = 'sectionF'
    report_id = request.args.get('report_id')
    term = request.args.get('term')
    routing = request.args.get('routing')

    c1 = getCursor()
    c1.execute("""SELECT s.supervisor_id,CONCAT(s.first_name, ' ', s.last_name,' - ',ss.supervisor_type),CONCAT(st.first_name, ' ', st.last_name)
                FROM student AS st JOIN student_supervisor AS ss ON st.student_id = ss.student_id
                JOIN supervisor AS s ON ss.supervisor_id = s.supervisor_id
                JOIN 6_month_report r ON st.student_id = r.student_id 
                WHERE r.report_id = %s;""", (report_id,))
    supervisor_list = c1.fetchall()
    c2 = getCursor()
    c2.execute("""select report_id, supervisor_id, comment, talk_option,content_status from sectionF 
                                 WHERE report_id = %s;""", (report_id,))

    sectionF_list = c2.fetchall()
    if sectionF_list:
        sectionF = sectionF_list[0]
    else:
        sectionF = []
    return render_template("report/sectionF.html", report_id=report_id, sectionF=sectionF, supervisor_list=supervisor_list, term=term, section=section, routing=routing, user_role=user_role)


if __name__ == '__main__':
    app.run(debug=True)
