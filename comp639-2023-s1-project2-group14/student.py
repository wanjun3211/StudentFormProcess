# This is the student's python file which consists of the following user stories:
# - View previous reports
# - View personal information and able to edit information
# - Fill in Section A, B, C, D and F

# Initial setup
from flask import Blueprint, render_template, request, url_for, redirect, flash
import mysql.connector
from mysql.connector import FieldType
import connect
from datetime import datetime
from flask import jsonify
from datetime import date

app_student = Blueprint('app_student', __name__)

app_student.secret_key = 'your_secret_key'


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


studentid = ''

# View student's personal info


@app_student.route('/student/personalinfo', methods=['GET', 'POST'])
def about():
    global studentid
    user_id = request.cookies.get('user_id')
    user_email = request.cookies.get('user_email')
    message = request.args.get('message')
    alertStyling = request.args.get('alertStyling')

    cur = getCursor()
    cur.execute("""select first_name,last_name, phone, address, enrolment_date,part_full_time,thesis_title,student_id
    from student
    where student.user_id = %s;""", (user_id,))
    infoDetails = cur.fetchall()
    studentid = infoDetails[0][7]

    cur2 = getCursor()
    cur2.execute(
        """SELECT email_address,department_id from user where user_id = %s;""", (user_id,))
    user = cur2.fetchall()

    cur3 = getCursor()
    cur3.execute("""SELECT user.email_address AS "Student Email", supervisor.first_name AS "Supervisor First Name", supervisor.last_name AS "Supervisor Last Name", supervisor_type
    FROM student_supervisor
    inner join student on student.student_id = student_supervisor.student_id
    inner join supervisor on supervisor.supervisor_id = student_supervisor.supervisor_id
    inner join user on student.user_id = user.user_id
    where user.email_address=%s;""", (user_email,))
    supervisors = cur3.fetchall()
    section = '1'  # To make the nav tabs active
    active = 'profile'  # For the left nav bar become active
    return render_template("/student/personalinfo.html", infoDetails=infoDetails, user=user, supervisors=supervisors, section=section, message=message, alertStyling=alertStyling, active=active)

# Get scholarship details of student


@app_student.route('/student/fetch_scholarships', methods=['POST'])
def fetch_scholarships():
    cur = getCursor()

    cur.execute("""SELECT scholar_name, scholar_value,scholar_tenure,scholar_end_date FROM 6_month_report
                inner join sectiona_scholar on 6_month_report.report_id = sectiona_scholar.report_id
                where student_id = %s;""", (studentid,))
    scholarship_list = cur.fetchall()

    return jsonify(scholarship_list)

# Get employment details of student


@app_student.route('/student/fetch_employments', methods=['POST'])
def fetch_employments():
    cur = getCursor()

    cur.execute("""SELECT teaching,research,other FROM 6_month_report
                inner join sectiona_employment on 6_month_report.report_id = sectiona_employment.report_id
                where student_id = %s;""", (studentid,))
    employment_list = cur.fetchall()

    return jsonify(employment_list)

# Update personal information


@app_student.route('/student/personalinfo/update', methods=['GET', 'POST'])
def updateinfo():
    user_id = request.cookies.get('user_id')
    user_email = request.cookies.get('user_email')

    if request.method == 'GET':
        connection = getCursor()
        connection.execute("""SELECT first_name, last_name, address, enrolment_date, part_full_time, thesis_title,phone
        FROM student WHERE user_id = %s;""", (user_id,))
        student = connection.fetchall()

        cur = getCursor()
        cur.execute(
            """SELECT email_address,department_id from user where user_id = %s;""", (user_id,))
        user = cur.fetchall()

        # Get to users' supervisor information
        supervisor_list = []
        for supervisor_type in ['main', 'associate', 'other']:
            connection2 = getCursor()
            connection2.execute("""select supervisor_type, CONCAT(supervisor.first_name,' ',supervisor.last_name) from student_supervisor
                                join supervisor on student_supervisor.supervisor_id = supervisor.supervisor_id
                                join student on student_supervisor.student_id = student.student_id
                                join user on user.user_id = student.user_id
                                where student.user_id = %s and supervisor_type = %s ;""", (user_id, supervisor_type,))
            supervisor = connection2.fetchall()
            if not supervisor:
                supervisor_list.append((supervisor_type, ''))
            else:
                supervisor_list.append((supervisor[0][0], supervisor[0][1]))

        # scholarship list
        cur.execute("""SELECT scholar_name, scholar_value,scholar_tenure,scholar_end_date  FROM 6_month_report
                inner join sectiona_scholar on 6_month_report.report_id = sectiona_scholar.report_id
                inner join student on 6_month_report.student_id = student.student_id
                where user_id = %s;""", (user_id,))
        scholarship_list = cur.fetchall()

        # employment list
        cur.execute("""SELECT teaching,research,other FROM 6_month_report
                inner join sectiona_employment on 6_month_report.report_id = sectiona_employment.report_id
                inner join student on 6_month_report.student_id = student.student_id
                where user_id = %s;""", (user_id,))
        employment_list = cur.fetchall()
        section = '2'  # To make the nav tabs active
        active = 'profile'  # For the left nav bar become active
        return render_template('/student/update-personalinfo.html', student=student, user=user, supervisor_list=supervisor_list, scholarship_list=scholarship_list, employment_list=employment_list, section=section, active=active)
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        address = request.form.get('address')
        enrolment = request.form.get('enrolment')
        status = request.form.get('status')
        title = request.form.get('title')
        phone = request.form.get('phone')
        department = request.form.get('department')

        if department == 'Environmental Management (DEM)':
            department = 1
        elif department == 'Tourism, Sport and Society (DTSS)':
            department = 2
        elif department == 'Landscape Architecture (SOLA)':
            department = 3

        print("DEPT: ", department)
        cur = getCursor()
        cur.execute("""update user join student on user.user_id = student.user_id
        SET student.first_name = %s, student.last_name = %s, user.email_address = %s,phone=%s,enrolment_date=%s,address=%s, part_full_time=%s,thesis_title=%s
        where user.user_id = %s;""",
                    (firstname, lastname, email, phone, enrolment, address, status, title, user_id))

        cur2 = getCursor()
        cur2.execute(
            """update user set department_id = %s where user_id = %s;""", (department, user_id))

        message = "Information has been updated!"
        alertStyling = "Green"

        return redirect(url_for('app_student.about', message=message, alertStyling=alertStyling))
        # return render_template("/student/personalinfo.html", infoDetails=infoDetails, user=user, message=message, alertStyling=alertStyling, supervisors=supervisors)

# Update student's password


@app_student.route('/student/personalinfo/changepassword', methods=['GET', 'POST'])
def changepassword():
    user_id = request.cookies.get('user_id')

    if request.method == 'POST':
        password = request.form.get('newpass')
        confirm_password = request.form.get('newpass2')

        if password != confirm_password:
            message = "Passwords do not match"
            alertStyling = "Red"
        else:
            connection = getCursor()
            connection.execute(
                """update user set user.password = %s WHERE user_id = %s;""", (password, user_id,))
            message = "Password is changed successfully"
            alertStyling = "Green"

            c = getCursor()
            c.execute("""select first_name,last_name, phone, address, enrolment_date,part_full_time,thesis_title,phone
            from student
            where student.user_id = %s;""", (user_id,))
            student = c.fetchall()

            cur4 = getCursor()
            cur4.execute(
                """SELECT email_address,department_id from user where user_id = %s;""", (user_id,))
            user = cur4.fetchall()

        return render_template('/student/personalinfo.html', message=message, infoDetails=student, alertStyling=alertStyling, user=user)
    elif request.method == "GET":
        section = '3'  # To make the nav tabs active
        connection = getCursor()
        connection.execute(
            """select password from user where user_id = %s;""", (user_id,))
        password = connection.fetchall()
        active = 'profile'  # For the left nav bar become active
        return render_template('/student/change-password.html', password=password, section=section, active=active)


# Report Section


@app_student.route('/student/report/intro', methods=['GET', 'POST'])
def report_intro():
    message = request.args.get('message')
    alertStyling = request.args.get('alertStyling')
    user_id = request.cookies.get('user_id')

    if request.method == 'POST':
        term = request.form.get('report')
        c1 = getCursor()
        c1.execute("""select report_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                                join user on student.user_id = user.user_id
                                where user.user_id = %s and term = %s;""", (user_id, term,))
        student_report = c1.fetchall()
        # If the report exists, get the report_id
        if student_report:
            report_id = student_report[0][0]
        # If the report does not exist, create a new report.
        else:
            c2 = getCursor()
            c2.execute("""INSERT INTO 6_month_report (student_id, report_progress_id, due_date, term, chair_action)
                SELECT student_id,1,
                CASE
                    WHEN EXISTS (SELECT * FROM 6_month_report JOIN student ON 6_month_report.student_id = student.student_id WHERE student.user_id =%s AND YEAR(due_date) = YEAR(CURRENT_DATE) AND MONTH(due_date) = 6 AND DAY(due_date) = 30) THEN DATE_FORMAT(CURRENT_DATE, '%Y-12-31')
                    ELSE DATE_FORMAT(CURRENT_DATE, '%Y-06-30')END,
              %s,NULL FROM student WHERE user_id = %s;""", (user_id, term, user_id,))
            c2.fetchall()
            report_id = c2.lastrowid
            c3 = getCursor()
            c3.execute(
                """INSERT INTO updated_time (report_id) VALUES (%s);""", (report_id,))

        return redirect(url_for('app_student.report_sectionA', term=term))
    else:
        # When entering the page, get all existing reports under this userid, the status of the report and the latest update time

        c1 = getCursor()
        c1.execute("""SELECT subquery.report_id,6_month_report.term,6_month_report.report_progress_id, MAX(updated_time),6_month_report.due_date AS latest_time,
        CASE WHEN 6_month_report.due_date > CURDATE() THEN 'ontime' ELSE 'overdue' END AS due_status
            FROM ( SELECT report_id, GREATEST(
                           COALESCE(sec_A, '1900-01-01'),
                           COALESCE(sec_B, '1900-01-01'),
                           COALESCE(sec_C, '1900-01-01'),
                           COALESCE(sec_D, '1900-01-01'),
                           COALESCE(sec_F, '1900-01-01'),
                           COALESCE(sec_E_main, '1900-01-01'),
                           COALESCE(sec_E_associate, '1900-01-01'),
                           COALESCE(sec_E_other, '1900-01-01'),
                           COALESCE(convenor, '1900-01-01'),
                           COALESCE(completed_date, '1900-01-01') ) AS updated_time
            FROM updated_time) AS subquery
        JOIN 6_month_report ON subquery.report_id = 6_month_report.report_id
        JOIN student ON student.student_id = 6_month_report.student_id
        WHERE student.user_id = %s GROUP BY subquery.report_id ORDER BY 6_month_report.due_date DESC LIMIT 1;""", (user_id,))

        report_progress = c1.fetchall()
        if report_progress:
            term_order = ('1st', '2nd', '3rd', '4th', '5th', '6th')
            current_term = report_progress[0][1]
            current_index = term_order.index(current_term)
            next_index = (current_index + 1) % len(term_order)
            next_term = term_order[next_index]
            report_progress[0] += (next_term,)
        active = 'report'  # For the left nav bar become active
        return render_template('/student/report/intro.html', report_progress=report_progress, message=message, alertStyling=alertStyling, active=active)

# Section A Report - Beibei


@app_student.route('/student/report/sectionA', methods=['GET', 'POST'])
def report_sectionA():

    user_id = request.cookies.get('user_id')
    message = ''
    alertStyling = ''

    if request.method == 'POST':
        term = request.form.get('term')
        submit_value = request.form.get('submit')
        c1 = getCursor()
        c1.execute("""select report_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                                            join user on student.user_id = user.user_id
                                            where user.user_id = %s and term = %s;""", (user_id, term,))
        student_report = c1.fetchall()
        report_id = student_report[0][0]
        # Get the form of the submitted report, whether it is saved in draft or submitted.
        if submit_value == 'Save Draft':
            content_status = 'Draft'
        else:
            content_status = 'Submitted'
        c3 = getCursor()
        c3.execute(
            """SELECT scholar_id from sectionA_scholar where report_id = %s; """, (report_id,))
        scholar_exist = c3.fetchall()

        # If the scholarship information for this report is already recorded in the database, delete it all and insert the updated information from the user.
        if scholar_exist:
            c4 = getCursor()
            c4.execute(
                """DELETE FROM sectionA_scholar where report_id = %s; """, (report_id,))

        for index in range(5):
            scholar_name = request.form.get(
                "scholarship{}-name".format(index))
            scholar_value = request.form.get(
                "scholarship{}-value".format(index))
            scholar_tenure = request.form.get(
                "scholarship{}-tenure".format(index))
            scholar_enddate = request.form.get(
                "scholarship{}-enddate".format(index))

            if scholar_name != "" or scholar_value != "" or scholar_tenure != "" or scholar_enddate != "":
                print('report_id', report_id)
                if scholar_name is not None or scholar_value is not None or scholar_tenure is not None or scholar_enddate is not None:
                    c5 = getCursor()
                    c5.execute(
                        """INSERT INTO sectionA_scholar (report_id, scholar_name, scholar_value, scholar_tenure,
                        scholar_end_date,content_status) VALUES (%s, %s, %s, %s, %s,%s);""",
                        (report_id, scholar_name, scholar_value, scholar_tenure, scholar_enddate, content_status,))
        # If the employment information for this report already has a record in the database, delete it all and insert the updated information from the user.
        c6 = getCursor()
        c6.execute(
            """SELECT id from sectionA_employment where report_id = %s; """, (report_id,))
        employment_exist = c3.fetchall()
        if employment_exist:
            c7 = getCursor()
            c7.execute(
                """DELETE FROM sectionA_employment where report_id = %s; """, (report_id,))

        for index in range(5):
            employ_teaching = request.form.get(
                "employment{}-teaching".format(index))
            employ_research = request.form.get(
                "employment{}-research".format(index))
            employ_other = request.form.get(
                "employment{}-other".format(index))

            if employ_teaching != "" or employ_research != "" or employ_other != "":
                if employ_teaching is not None or employ_research is not None or employ_other is not None:
                    c5 = getCursor()
                    c5.execute(
                        """INSERT INTO sectionA_employment (report_id, teaching, research, other,content_status) VALUES (%s, %s, %s, %s, %s);""",
                        (report_id, employ_teaching, employ_research, employ_other, content_status,))
        # Update the time at the time of submission
        current_datetime = datetime.now()
        c8 = getCursor()
        c8.execute("""UPDATE updated_time SET sec_A = %s WHERE report_id = %s; """,
                   (current_datetime, report_id,))
        message = 'You have successfully saved the draft.'
        alertStyling = 'Green'

        return redirect(url_for('app_student.report_sectionA', term=term, report_id=report_id, message=message, alertStyling=alertStyling))

    else:
        scholar_id = request.args.get('scholar_id')
        employment_id = request.args.get('employment_id')
        message = request.args.get('message')
        alertStyling = request.args.get('alertStyling')
        if scholar_id is not None:
            c1 = getCursor()
            c1.execute(
                """DELETE FROM sectionA_scholar where scholar_id = %s; """, (scholar_id,))
            message = 'You have successfully deleted a scholarship record.'
            alertStyling = "Green"

        elif employment_id is not None:
            c1 = getCursor()
            c1.execute(
                """DELETE FROM sectionA_employment where id = %s; """, (employment_id,))
            message = 'You have successfully deleted a employment record.'
            alertStyling = "Green"

        # Get to users' personal information
        connection1 = getCursor()
        connection1.execute("""select CONCAT(s.first_name,' ', s.last_name), s.student_id,enrolment_date, address, s.phone,email_address,part_full_time,thesis_title from student s left join user on s.user_id = user.user_id
                where s.user_id = %s;""",
                            (user_id,))
        students_list = connection1.fetchall()
        # Get to users' supervisor information
        supervisor_list = []
        for supervisor_type in ['main', 'associate', 'other']:
            connection2 = getCursor()
            connection2.execute("""select CONCAT(supervisor.first_name,' ',supervisor.last_name) from student_supervisor
                        join supervisor on student_supervisor.supervisor_id = supervisor.supervisor_id
                        join student on student_supervisor.student_id = student.student_id
                        join user on user.user_id = student.user_id
                        where student.user_id = %s and supervisor_type = %s ;""", (user_id, supervisor_type,))
            supervisor = connection2.fetchall()
            if not supervisor:
                supervisor_list.append('')
            else:
                supervisor_list.append(supervisor[0][0])
        # Get to users' scholarship information
        term = request.args['term']
        connection3 = getCursor()
        connection3.execute("""select scholar_name,scholar_value,scholar_tenure,scholar_end_date,content_status,scholar_id from sectionA_scholar join 6_month_report on sectionA_scholar.report_id = 6_month_report.report_id
                join student on student.student_id = 6_month_report.student_id
                join user on student.user_id = user.user_id
                where user.user_id = %s and term = %s;""",
                            (user_id, term,))
        scholar_list = connection3.fetchall()
        # Get to users' employment information
        connection4 = getCursor()
        connection4.execute("""select sectionA_employment.report_id,teaching,research,other,content_status,id from sectionA_employment join 6_month_report on sectionA_employment.report_id = 6_month_report.report_id
                join student on student.student_id = 6_month_report.student_id
                join user on student.user_id = user.user_id
                where user.user_id = %s and term = %s;""",
                            (user_id, term,))
        employment_list = connection4.fetchall()

        # Get to users' report's status,if the status is completed, the submit button needs to be hidden on the page
        con1 = getCursor()
        con1.execute("""select report_progress_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                join user on user.user_id = student.user_id
                where student.user_id = %s and term = %s;""",
                     (user_id, term,))
        progress_list = con1.fetchall()
        progress_id = progress_list[0][0]
        section = 'sectionA'  # To make the nav tabs active
        active = 'report'  # For the left nav bar become active
        return render_template('/student/report/sectionA.html', students_list=students_list, supervisor_list=supervisor_list, scholar_list=scholar_list, employment_list=employment_list, term=term, progress_id=progress_id, message=message, alertStyling=alertStyling, section=section, active=active)

# Section B Report - Beibei


@app_student.route('/student/report/sectionB', methods=['GET', 'POST'])
def report_sectionB():
    user_id = request.cookies.get('user_id')
    term = request.args.get('term')
    if request.method == 'GET':
        message = request.args.get('message')
        alertStyling = request.args.get('alertStyling')
        # Get the report's sectionB information
        connection1 = getCursor()
        connection1.execute("""select sectionB_1.report_id, induction_program, Mutual_expectation, MEA, Intellectual_Property, Thesis_proposal_seminar, Research_proposal_approved,
            PG_conference_presentation, Thesis_Results_Seminar,content_status from sectionB_1 join 6_month_report on sectionB_1.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id
                    join user on student.user_id = user.user_id
                    where user.user_id = %s and term = %s;""",
                            (user_id, term,))
        sectionB_1_list = connection1.fetchall()
        if sectionB_1_list:
            sectionB_1 = sectionB_1_list[0]
        else:
            sectionB_1 = []

        connection2 = getCursor()
        connection2.execute("""select sectionB_2_committee.report_id,Human_Ethics, Health_and_Safety, Animal_Ethics, Institutional_Biological_Safety, Radiation_Protection_Officer,content_status from sectionB_2_committee
            join 6_month_report on sectionB_2_committee.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id
                    join user on student.user_id = user.user_id
                    where user.user_id = %s and term = %s;""",
                            (user_id, term,))
        sectionB_2_list = connection2.fetchall()
        if sectionB_2_list:
            sectionB_2 = sectionB_2_list[0]
        else:
            sectionB_2 = []

         # Get to users' report's status,if the status is completed, the submit button needs to be hidden on the page
        con1 = getCursor()
        con1.execute("""select report_progress_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                join user on user.user_id = student.user_id
                where student.user_id = %s and term = %s;""",
                     (user_id, term,))
        progress_list = con1.fetchall()
        progress_id = progress_list[0][0]
        section = 'sectionB'  # To make the nav tabs active
        active = 'report'  # For the left nav bar become active
        return render_template('/student/report/sectionB.html', sectionB_1=sectionB_1, sectionB_2=sectionB_2, term=term, message=message, alertStyling=alertStyling, progress_id=progress_id, section=section, active=active)

    elif request.method == 'POST':
        submit_value = request.form.get('submit')
        term = request.form.get('term')
        if submit_value == 'Save Draft':
            content_status = 'Draft'
        else:
            content_status = 'Submitted'
        #  get the report's id
        c1 = getCursor()
        c1.execute("""select report_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                                        join user on student.user_id = user.user_id
                                        where user.user_id = %s and term = %s;""", (user_id, term,))
        student_report = c1.fetchall()
        report_id = student_report[0][0]

        # If the sectionB_1 information for this report already has a record in the database, delete it all and insert the updated information from the user.
        c2 = getCursor()
        c2.execute(
            """SELECT id from sectionB_1 where report_id = %s; """, (report_id,))
        sectionB_1_exist = c2.fetchall()
        if sectionB_1_exist:
            c3 = getCursor()
            c3.execute(
                """DELETE FROM sectionB_1 where report_id = %s; """, (report_id,))

        sectionB_1_fields = {
            'induction_study': 'induction_date',
            'mutual_study': 'mutual_date',
            'MEA_study': 'MEA_date',
            'intellectual_study': 'intellectual_date',
            'thesis_study': 'thesis_date',
            'research_study': 'research_date',
            'pg_conference': 'pg_date',
            'thesis_results': 'thesis_results_date'
        }

        form_data = {}
        form_data['report_id'] = report_id
        for field, date_field in sectionB_1_fields.items():
            value = request.form.get(field)
            if value == 'uncompleted':
                date_value = None
            else:
                date_value = request.form.get(date_field)

            form_data[field] = date_value

        form_data['content_status'] = content_status
        connection3 = getCursor()
        insert_query = """
            INSERT INTO sectionB_1 (
                report_id,induction_program, Mutual_expectation, MEA, Intellectual_Property,
                Thesis_proposal_seminar, Research_proposal_approved, PG_conference_presentation,
                Thesis_Results_Seminar, content_status
            )VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"""
        connection3.execute(insert_query, tuple(form_data.values()))

        c4 = getCursor()
        c4.execute(
            """SELECT id from sectionB_2_committee where report_id = %s; """, (report_id,))
        sectionB_2_exist = c4.fetchall()
        if sectionB_2_exist:
            c5 = getCursor()
            c5.execute(
                """DELETE FROM sectionB_2_committee where report_id = %s; """, (report_id,))

        human_ethics = request.form.get('human_ethics')
        health_safety = request.form.get('health_safety')
        animal_ethics = request.form.get('animal_ethics')
        bio_safety = request.form.get('bio_safety')
        radiation_protection = request.form.get('radiation_protection')
        c6 = getCursor()
        c6.execute("""INSERT INTO sectionB_2_committee (report_id,Human_Ethics, Health_and_Safety, Animal_Ethics, Institutional_Biological_Safety, Radiation_Protection_Officer,content_status) VALUES
        (%s,%s,%s,%s,%s,%s,%s); """, (report_id, human_ethics, health_safety, animal_ethics, bio_safety, radiation_protection, content_status,))

        current_datetime = datetime.now()
        c7 = getCursor()
        c7.execute("""UPDATE updated_time SET sec_B = %s WHERE report_id = %s; """,
                   (current_datetime, report_id,))
        message = 'You have successfully saved the draft.'
        alertStyling = 'Green'

        return redirect(url_for('app_student.report_sectionB', term=term, message=message, alertStyling=alertStyling))

# Section C Report - Sabrina


@app_student.route('/student/report/sectionC', methods=['GET', 'POST'])
def report_sectionC():
    # Grab current user id that is logged on and prepare database
    user_id = request.cookies.get('user_id')
    term = request.args.get('term')
    cur = getCursor()
    content_status = ''
    saved = 0

    # Form posted
    if request.method == 'POST':
        submit_value = request.form.get('submit')
        term = request.form.get('term')
        report_id = request.form.get('report_id')

        if submit_value == 'Save Draft':
            content_status = 'Draft'
        else:
            content_status = 'Submitted'

        # Grab existing sectionC other titles
        cur.execute(
            """select id from sectionC_1_other where report_id = %s;""", (report_id,))
        other_exist = cur.fetchall()

        # check if other exist, it will be deleted if it is
        if other_exist:
            cur.execute(
                """delete from sectionC_1_other where report_id = %s;""", (report_id,))

        # Insert new other data
        for index in range(5):
            title = request.form.get("other-title-{}".format(index))
            select = request.form.get("other-{}".format(index))
            comment = request.form.get("other-comment-{}".format(index))

            if title != "" or select != "" or comment != "":
                if title is not None or select is not None or comment is not None:

                    cur.execute("""
                    insert into sectionC_1_other (report_id, other_title,other,
                    comment,content_status)
                    values(%s,%s,%s,%s,%s);""", (report_id, title, select, comment, content_status))

        # Section C Part 1 Table Update (not comments)
        Access_Psuper = request.form.get('access-sup-principal')
        Access_Asuper = request.form.get('access-sup-associate')
        Psuper_expertise = request.form.get('sup-expert-principal')
        Asuper_expertise = request.form.get('sup-expert-associate')
        Qua_Psuper = request.form.get('quality-feedback-principal')
        Qua_Asuper = request.form.get('quality-feedback-associate')
        TL_Psuper = request.form.get('timeliness-principal')
        TL_Asuper = request.form.get('timeliness-associate')
        Courses_avail = request.form.get('courses')
        Workspace = request.form.get('workspace')
        Com_facility = request.form.get('comp-facilities')
        ITS_support = request.form.get('its-support')
        Res_software = request.form.get('research')
        Lib_facility = request.form.get('library')
        T_L_cen_support = request.form.get('teaching-support')
        Stat_support = request.form.get('statistical')
        Res_equipment = request.form.get('research-eq')
        Tech_support = request.form.get('technical-support')
        Finan_resources = request.form.get('financial')

        # Check whether empty
        cur.execute(
            """select report_id from sectionC_1 where report_id = %s;""", (report_id,))
        current_sectionC_part1 = cur.fetchall()

        if current_sectionC_part1:
            cur.execute("""update sectionC_1 set Access_Psuper = %s,
            Access_Asuper=%s, Psuper_expertise=%s, Asuper_expertise=%s, Qua_Psuper=%s,Qua_Asuper=%s,
            TL_Psuper=%s, TL_Asuper=%s, Courses_avail=%s, Workspace=%s, Com_facility=%s,
            ITS_support=%s, Res_software=%s,Lib_facility=%s,T_L_cen_support=%s,
            Stat_support=%s, Res_equipment=%s, Tech_support=%s, Finan_resources=%s
            where report_id = %s;""",
                        (Access_Psuper, Access_Asuper,
                         Psuper_expertise, Asuper_expertise,
                         Qua_Psuper, Qua_Asuper, TL_Psuper, TL_Asuper,
                         Courses_avail, Workspace, Com_facility,
                         ITS_support, Res_software, Lib_facility, T_L_cen_support,
                         Stat_support, Res_equipment, Tech_support, Finan_resources,
                         report_id))
        else:
            cur.execute("""insert into sectionC_1 (Access_Psuper, Access_Asuper, Psuper_expertise, Asuper_expertise, Qua_Psuper, Qua_Asuper, 
            TL_Psuper, TL_Asuper, Courses_avail, Workspace, Com_facility, ITS_support, 
            Res_software, Lib_facility, T_L_cen_support, Stat_support, Res_equipment, Tech_support, Finan_resources,report_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ;""",
                        (Access_Psuper, Access_Asuper,
                         Psuper_expertise, Asuper_expertise,
                         Qua_Psuper, Qua_Asuper, TL_Psuper, TL_Asuper,
                         Courses_avail, Workspace, Com_facility,
                         ITS_support, Res_software, Lib_facility, T_L_cen_support,
                         Stat_support, Res_equipment, Tech_support, Finan_resources,
                         report_id))

        # Section C Part 1 Comments Only
        comment_1 = request.form.get('access-sup-principal-comment')
        comment_2 = request.form.get('access-sup-associate-comment')
        comment_3 = request.form.get('sup-expert-principal-comment')
        comment_4 = request.form.get('sup-expert-associate-comment')
        comment_5 = request.form.get('quality-feedback-principal-comment')
        comment_6 = request.form.get('quality-feedback-associate-comment')
        comment_7 = request.form.get('timeliness-principal-comment')
        comment_8 = request.form.get('timeliness-associate-comment')
        comment_9 = request.form.get('courses-comment')
        comment_10 = request.form.get('workspace-comment')
        comment_11 = request.form.get('comp-facilities-comment')
        comment_12 = request.form.get('its-support-comment')
        comment_13 = request.form.get('research-comment')
        comment_14 = request.form.get('library-comment')
        comment_15 = request.form.get('teaching-support-comment')
        comment_16 = request.form.get('statistical-comment')
        comment_17 = request.form.get('research-eq-comment')
        comment_18 = request.form.get('technical-support-comment')
        comment_19 = request.form.get('financial-comment')
        # comment_20 = request.form.get('other-comment')
        cur.execute("""update sectionC_1 set
        comment_1=%s,comment_2=%s,comment_3=%s,
        comment_4=%s,comment_5=%s,comment_6=%s,
        comment_7=%s,comment_8=%s,comment_9=%s,
        comment_10=%s,comment_11=%s,comment_12=%s,
        comment_13=%s,comment_14=%s,comment_15=%s,
        comment_16=%s,comment_17=%s,comment_18=%s,
        comment_19=%s where report_id = %s;""",
                    (comment_1, comment_2, comment_3,
                     comment_4, comment_5, comment_6,
                     comment_7, comment_8, comment_9,
                     comment_10, comment_11, comment_12,
                     comment_13, comment_14, comment_15,
                     comment_16, comment_17, comment_18,
                     comment_19,  report_id))

        # Section C Part 2 Questions Update
        meeting = request.form.get('meeting')
        feedback = request.form.get('feedback')
        feedbackSupervisor = request.form.getlist('feedback-supervisor')

        cur.execute(
            """select report_id from sectionC_2 where report_id = %s;""", (report_id,))
        current_sectionC_2 = cur.fetchall()

        if current_sectionC_2:
            cur.execute("""update sectionC_2 set
            meeting_frequ=%s, period_feedback=%s
            where report_id = %s;""", (meeting, feedback, report_id))
        else:
            cur.execute("""insert into sectionC_2 (report_id, meeting_frequ, period_feedback, content_status) values(%s,%s,%s,content_status);""",
                        (report_id, meeting, feedback))

        # Delete all existing entries with the same report id
        cur.execute(
            """delete from sectionc_2_receive_feedback where report_id = %s;""", (report_id,))

        # insert new entries from the report_id given
        for feedback in feedbackSupervisor:
            cur.execute(
                """insert into sectionc_2_receive_feedback (report_id,receive_feedback,content_status) values (%s,%s,%s);""", (report_id, feedback, content_status))

        if 'submit' in request.form:
            current_datetime = datetime.now()
            cur.execute("""UPDATE updated_time SET sec_C = %s WHERE report_id = %s; """,
                        (current_datetime, report_id,))
            saved = 1

    # From Beibei - Get
    cur.execute("""select report_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                                       join user on student.user_id = user.user_id
                                       where user.user_id = %s and term = %s;""", (user_id, term,))
    student_report = cur.fetchall()
    report_id = student_report[0][0]

    if saved == 1:
        message = 'You have successfully saved the draft.'
        alertStyling = 'Green'
    else:
        message = ''
        alertStyling = ''

    # Grab existing values from section C part 1
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

    # Grab any existing values available for the currently form for section C part 2
    cur.execute(
        """select meeting_frequ, period_feedback from sectionc_2 where report_id = %s; """, (report_id,))
    sectionc_part2 = cur.fetchall()

    # grab only receive_feedback
    cur.execute(
        """select receive_feedback from sectionc_2_receive_feedback where report_id = %s; """, (report_id,))
    sectionc_part2_receive_feedback = cur.fetchall()

    # Grab draft or complete status
    # Section C_1
    cur.execute("""select sectionc_1.report_id, content_status from sectionc_1
            join 6_month_report on sectionc_1.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id
                    join user on student.user_id = user.user_id
                    where user.user_id = %s and term = %s;""", (user_id, term))
    sectionC1_status = cur.fetchall()
    if sectionC1_status:
        sectionC1_status = sectionC1_status[0][1]

    # Section C_2
    cur.execute("""select sectionc_2.report_id, content_status from sectionc_2
            join 6_month_report on sectionc_2.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id
                    join user on student.user_id = user.user_id
                    where user.user_id = %s and term = %s;""", (user_id, term))
    sectionC2_status = cur.fetchall()
    if sectionC2_status:
        sectionC2_status = sectionC2_status[0][1]

    # # Section C_2 feedback multiple
    cur.execute("""select distinct sectionc_2_receive_feedback.report_id, content_status from sectionc_2_receive_feedback
            join 6_month_report on sectionc_2_receive_feedback.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id
                    join user on student.user_id = user.user_id
                    where user.user_id = %s and term = %s;""", (user_id, term))
    sectionC2_feedback = cur.fetchall()
    if sectionC2_feedback:
        sectionC2_feedback = sectionC2_feedback[0][1]

    # Get to users' report's status,if the status is completed, the submit button needs to be hidden on the page
    con1 = getCursor()
    con1.execute("""select report_progress_id from 6_month_report join student on student.student_id = 6_month_report.student_id
            join user on user.user_id = student.user_id
            where student.user_id = %s and term = %s;""",
                 (user_id, term,))
    progress_list = con1.fetchall()
    progress_id = progress_list[0][0]
    section = 'sectionC'  # To make the nav tabs active
    active = 'report'  # For the left nav bar become active

    return render_template('/student/report/sectionC.html', sectionc_part1=sectionc_part1, sectionc_part1_other=sectionc_part1_other,
                           sectionc_part1_comments=sectionc_part1_comments,
                           sectionc_part2=sectionc_part2, sectionc_part2_receive_feedback=sectionc_part2_receive_feedback,
                           sectionC1_status=sectionC1_status, sectionC2_status=sectionC2_status,
                           sectionC2_feedback=sectionC2_feedback, message=message, alertStyling=alertStyling, term=term,
                           report_id=report_id, content_status=content_status, progress_id=progress_id, section=section, active=active)


# Section D Report - Sabrina
@ app_student.route('/student/report/sectionD', methods=['GET', 'POST'])
def report_sectionD():
    # Grab current user id that is logged on and prepare database
    user_id = request.cookies.get('user_id')
    term = request.args.get('term')
    cur = getCursor()
    message = ''
    alertStyling = ''
    content_status = ''

    if request.method == 'POST':
        term = request.form.get('term')
        report_id = request.form.get('report_id')
        # --------- update section 1: objectives
        # Check for existing data in database
        cur.execute(
            """select objective_id from sectiond_1_objective where report_id = %s;""", (report_id,))
        first_obj_exist = cur.fetchall()

        if first_obj_exist:
            cur.execute(
                """delete from sectiond_1_objective where report_id = %s; """, (report_id,))

        # Only add up to 6 rows but need to set a limit in javascript
        for index in range(5):
            obj_content = request.form.get(
                "first-content-{}".format(index))
            status = request.form.get("first-status-{}".format(index))
            comment = request.form.get("first-comment-{}".format(index))
            obj_change_reason = request.form.get(
                "first-changes-{}".format(index))

            if obj_content != "" or status != "" or comment != "" or obj_change_reason != "":
                if obj_content is not None or status is not None or comment is not None or obj_change_reason is not None:
                    cur.execute(
                        """insert into sectiond_1_objective (report_id,obj_content,status,comment,obj_change_reason,content_status) values(%s,%s,%s,%s,%s,'Draft');""",
                        (report_id, obj_content, status, comment, obj_change_reason))

        # -------------- Update section 2: covid and section3: achievements
        covid = request.form.get('covid')
        achievements = request.form.get('achievements')

        # Check if existing covid details
        cur.execute(
            """select covid_id from sectiond_2_covid where report_id = %s;""", (report_id,))
        covid_details_exist = cur.fetchall()

        if covid_details_exist:
            cur.execute(
                """delete from sectiond_2_covid where report_id = %s;""", (report_id,))

        # Check if existing achievements details
        cur.execute(
            """select achiev_id from sectiond_3_achievements where report_id = %s;""", (report_id,))
        achievement_exist = cur.fetchall()

        if achievement_exist:
            cur.execute(
                """delete from sectiond_3_achievements where report_id = %s;""", (report_id,))

        if covid != '':
            cur.execute(
                """insert into sectiond_2_covid set comment = %s, report_id = %s,content_status ='Draft';""", (covid, report_id))

        if achievements != '':
            cur.execute("""insert into sectiond_3_achievements set achievement = %s, report_id = %s,content_status='Draft';""",
                        (achievements, report_id))

        # --------------- update section 4: objectives
        # Check if existing 4th objective details
        cur.execute(
            """select obj_id from sectiond_4_objective where report_id = %s;""", (report_id,))
        fourth_obj_exist = cur.fetchall()

        if fourth_obj_exist:
            cur.execute(
                """delete from sectiond_4_objective where report_id = %s;""", (report_id,))

        for index in range(5):
            objective = request.form.get(
                "first-objective-{}".format(index))
            target = request.form.get("first-target-{}".format(index))
            problem = request.form.get("first-problem-{}".format(index))

            if objective != "" or target != "" or problem != "":
                if objective is not None or target is not None or problem is not None:
                    cur.execute(
                        """insert into sectiond_4_objective (report_id,objective,target,problem,content_status) values(%s,%s,%s,%s,'Draft');""",
                        (report_id, objective, target, problem))

        # --------------- update section 5: objectives
        # Check if existing 5th objective details (cost)
        cur.execute(
            """select item_id from sectiond_5_objective where report_id = %s;""", (report_id,))
        fifth_obj_exist = cur.fetchall()

        if fifth_obj_exist:
            cur.execute(
                """delete from sectiond_5_objective where report_id = %s;""", (report_id,))

        for index in range(5):
            item = request.form.get("first-item-{}".format(index))
            amount = request.form.get("first-amount-{}".format(index))
            note = request.form.get("first-note-{}".format(index))

            if item != "" or amount != "" or note != "":
                if item is not None or amount is not None or note is not None:
                    cur.execute(
                        """insert into sectiond_5_objective (report_id,item,amount,note) values(%s,%s,%s,%s);""",
                        (report_id, item, amount, note))

        if 'save-draft' in request.form:

            current_datetime = datetime.now()
            cur.execute("""UPDATE updated_time SET sec_D = %s WHERE report_id = %s; """,
                        (current_datetime, report_id,))

            message = 'You have successfully saved the draft.'
            alertStyling = 'Green'

    # Get statements
    cur.execute("""select report_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                                       join user on student.user_id = user.user_id
                                       where user.user_id = %s and term = %s;""", (user_id, term,))
    student_report = cur.fetchall()
    report_id = student_report[0][0]
    # get section d Objectives (1)
    cur.execute(
        """select obj_content, status, comment, obj_change_reason from sectiond_1_objective where report_id = %s;""", (report_id,))
    sectionD_1_objective = cur.fetchall()

    if all(data is None for row in sectionD_1_objective for data in row):
        sectionD_1_objective = ''

    for objective in sectionD_1_objective:
        print(objective)

    # get section d covid (2)
    cur.execute(
        """select comment from sectiond_2_covid where report_id = %s;""", (report_id,))
    sectionD_2_covid = cur.fetchall()

    # get section d achievements (3)
    cur.execute(
        """select achievement from sectiond_3_achievements where report_id = %s;""", (report_id,))
    sectionD_3_achievements = cur.fetchall()

    # get section d objective (4)
    cur.execute(
        """select objective, target, problem from sectiond_4_objective where report_id = %s;""", (report_id,))
    sectionD_4 = cur.fetchall()

    # get section d payment (5)
    cur.execute(
        """select item, amount, note from sectiond_5_objective where report_id = %s;""", (report_id,))
    sectionD_5 = cur.fetchall()

    # get report status
    cur.execute("""select distinct content_status from sectiond_1_objective
            join 6_month_report on sectiond_1_objective.report_id = 6_month_report.report_id
                    join student on student.student_id = 6_month_report.student_id
                    join user on student.user_id = user.user_id
                    where user.user_id = %s and term = %s;""", (user_id, term))
    content_status = cur.fetchall()
    if content_status:
        content_status = content_status[0][0]

    # Get to users' report's status,if the status is completed, the submit button needs to be hidden on the page
    con1 = getCursor()
    con1.execute("""select report_progress_id from 6_month_report join student on student.student_id = 6_month_report.student_id
            join user on user.user_id = student.user_id
            where student.user_id = %s and term = %s;""",
                 (user_id, term,))
    progress_list = con1.fetchall()
    progress_id = progress_list[0][0]
    section = 'sectionD'  # To make the nav tabs active
    active = 'report'  # For the left nav bar become active
    return render_template('/student/report/sectionD.html', sectionD_1_objective=sectionD_1_objective, sectionD_2_covid=sectionD_2_covid,
                           sectionD_3_achievements=sectionD_3_achievements, sectionD_4=sectionD_4, sectionD_5=sectionD_5, term=term, message=message, alertStyling=alertStyling,
                           report_id=report_id, content_status=content_status, progress_id=progress_id, section=section, active=active)

# Section F (Beibei)


@app_student.route('/student/report/sectionF', methods=['GET', 'POST'])
def report_sectionF():
    user_id = request.cookies.get('user_id')
    user_name = request.cookies.get('user_name')
    if request.method == 'GET':
        term = request.args.get('term')
        message = request.args.get('message')
        alertStyling = request.args.get('alertStyling')
        c1 = getCursor()
        c1.execute("""SELECT s.supervisor_id,CONCAT(s.first_name, ' ', s.last_name,' - ',ss.supervisor_type)
            FROM student AS st JOIN student_supervisor AS ss ON st.student_id = ss.student_id
            JOIN supervisor AS s ON ss.supervisor_id = s.supervisor_id
            WHERE st.user_id = %s;""", (user_id,))
        supervisor_list = c1.fetchall()
        c2 = getCursor()
        c2.execute("""select sectionF.report_id, supervisor_id, comment, talk_option,content_status from sectionF join 6_month_report on sectionF.report_id = 6_month_report.report_id
                            join student on student.student_id = 6_month_report.student_id 
                            join user on student.user_id = user.user_id
                            where user.user_id = %s and term = %s;""",
                   (user_id, term,))
        sectionF_list = c2.fetchall()
        if sectionF_list:
            sectionF = sectionF_list[0]
        else:
            sectionF = []

        # Get to users' report's status,if the status is completed, the submit button needs to be hidden on the page
        con1 = getCursor()
        con1.execute("""select report_progress_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                join user on user.user_id = student.user_id
                where student.user_id = %s and term = %s;""",
                     (user_id, term,))
        progress_list = con1.fetchall()
        progress_id = progress_list[0][0]
        section = 'sectionF'  # To make the nav tabs active
        active = 'report'  # For the left nav bar become active
        return render_template('/student/report/sectionF.html', sectionF=sectionF, term=term, supervisor_list=supervisor_list, user_name=user_name,
                               message=message, alertStyling=alertStyling, progress_id=progress_id, section=section, active=active)
    elif request.method == 'POST':
        term = request.form.get('term')
        supervisor_id = request.form.get('supervisor-name')
        comment = request.form.get('comments')
        talk_option = request.form.get('contact-person')
        submit_value = request.form.get('submit')

        # If the sectionF information for this report already has a record in the database, delete it all and insert the updated information from the user.
        c1 = getCursor()
        c1.execute("""SELECT f.id from sectionF f join 6_month_report r on r.report_id = f.report_id
         join student on student.student_id = r.student_id
         join user on student.user_id = user.user_id
         where user.user_id = %s and term = %s;""", (user_id, term,))

        sectionF_exist = c1.fetchall()
        if sectionF_exist:
            c2 = getCursor()
            c2.execute("""select report_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                                                    join user on student.user_id = user.user_id
                                                    where user.user_id = %s and term = %s;""", (user_id, term,))
            student_report = c2.fetchall()
            report_id = student_report[0][0]
            c3 = getCursor()
            c3.execute(
                """DELETE FROM sectionF WHERE report_id = %s;""", (report_id,))

        # Get the form of the submitted report, whether it is saved in draft or submitted.
        if submit_value == 'Save Draft':
            if comment is not None and talk_option is not None:
                content_status = 'Draft'
                message = 'You have successfully saved the draft.'

                c4 = getCursor()
                c4.execute("""INSERT INTO sectionF (report_id, supervisor_id, comment, talk_option, content_status)
                    SELECT r.report_id, %s, %s, %s, %s
                    FROM 6_month_report r JOIN student s ON r.student_id = s.student_id
                    WHERE s.user_id = %s AND r.term = %s;""", (supervisor_id, comment, talk_option, content_status, user_id, term,))
                alertStyling = "Green"

                current_datetime = datetime.now()
                c5 = getCursor()
                c5.execute("""UPDATE updated_time ut join 6_month_report r on r.report_id = ut.report_id
                    join student on student.student_id = r.student_id
                    join user on student.user_id = user.user_id SET sec_F = %s
                    where user.user_id = %s and term = %s;""", (current_datetime, user_id, term,))
            else:
                message = 'Note that you did not fill in Section F'
                alertStyling = 'Yellow'

            return redirect(url_for('app_student.report_sectionF', term=term, message=message, alertStyling=alertStyling))
        elif 'submit-all' in request.form:
            cur = getCursor()
            # Get Report_id
            cur.execute("""select report_id from 6_month_report join student on student.student_id = 6_month_report.student_id
                                                join user on student.user_id = user.user_id
                                                where user.user_id = %s and term = %s;""", (user_id, term,))
            student_report = cur.fetchall()
            report_id = student_report[0][0]

            if comment is not None and talk_option is not None:
                content_status = 'Submitted'

                cur.execute(
                    """update 6_month_report set report_progress_id = 2 where report_id = %s;""", (report_id,))

                # Check initial report status
                cur.execute(
                    """select main_check from 6_month_report where report_id = %s;""", (report_id,))
                initial_status = cur.fetchall()

                if initial_status[0][0] == 'reject':
                    cur.execute(
                        """update 6_month_report set main_check = 'in progress' where report_id = %s""", (report_id,))

                # Insert changes to section F (Repeated code from above)
                c4 = getCursor()
                c4.execute("""INSERT INTO sectionF (report_id, supervisor_id, comment, talk_option, content_status)
                    SELECT r.report_id, %s, %s, %s, %s
                    FROM 6_month_report r JOIN student s ON r.student_id = s.student_id
                    WHERE s.user_id = %s AND r.term = %s;""", (supervisor_id, comment, talk_option, content_status, user_id, term,))

                current_datetime = datetime.now()
                c5 = getCursor()
                c5.execute("""UPDATE updated_time ut join 6_month_report r on r.report_id = ut.report_id
                    join student on student.student_id = r.student_id
                    join user on student.user_id = user.user_id SET sec_F = %s
                    where user.user_id = %s and term = %s;""", (current_datetime, user_id, term,))

                message = "Form submitted!"
                alertStyling = "Green"
            else:
                # Check initial report status
                cur.execute(
                    """select main_check from 6_month_report where report_id = %s;""", (report_id,))
                initial_status = cur.fetchall()

                if initial_status[0][0] == 'reject':
                    cur.execute(
                        """update 6_month_report set main_check = 'in progress' where report_id = %s""", (report_id,))

                cur = getCursor()
                cur.execute(
                    """update 6_month_report set report_progress_id = 2 where report_id = %s;""", (report_id,))

                # check if Section F exists and delete it
                cur.execute(
                    """select id from sectionf where report_id = %s;""", (report_id,))
                sectionF_exist_check = cur.fetchall()

                if sectionF_exist_check:
                    cur.execute(
                        """delete id from sectionf where report_id = %s;""", (report_id,))

                message = "Form submitted but Section F was left empty"
                alertStyling = "Green"

            # update status of other sections
            cur = getCursor()
            cur.execute(
                """update sectionc_1 set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectionc_1_other set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectionc_2 set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectionc_2_receive_feedback set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectiond_1_objective set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectiond_2_covid set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectiond_3_achievements set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectiond_4_objective set content_status = "Submitted" where report_id = %s;""", (report_id,))
            cur.execute(
                """update sectiond_5_objective set content_status = "Submitted" where report_id = %s;""", (report_id,))

            # update submited time of all sections
            current_datetime = datetime.now()
            cur2 = getCursor()
            cur2.execute("""update updated_time set sec_A = %s, sec_B = %s, sec_C = %s, sec_D = %s, sec_F = %s where report_id = %s;""",
                         (current_datetime, current_datetime, current_datetime, current_datetime, current_datetime, report_id))

            # Send a reminder to the student's MAIN supervisor.
            cur.execute("""INSERT INTO reminder (user_id, student_id, reminder_info)
               SELECT sup.user_id, ss.student_id, CONCAT('The student (', s.first_name, ' ', s.last_name, ') has submitted his/her ', %s, ' report, please check it.')
               FROM supervisor sup
               JOIN student_supervisor ss ON ss.supervisor_id = sup.supervisor_id
               JOIN 6_month_report r ON r.student_id = ss.student_id
               JOIN student s ON r.student_id = s.student_id
               WHERE r.report_id = %s AND ss.supervisor_type = 'main';
               """, (term, report_id,))

            return redirect(url_for('app_student.report_intro', term=term, message=message, alertStyling=alertStyling))

# View previous reports (Beibei)


@app_student.route('/student/history_report', methods=['GET', 'POST'])
def history_report():
    user_id = request.cookies.get('user_id')
    connection1 = getCursor()
    connection1.execute("""SELECT report_id,term,due_date FROM 6_month_report r JOIN student s
    ON s.student_id = r.student_id WHERE s.user_id = %s AND r.report_progress_id=6;""", (user_id,))

    report_list = connection1.fetchall()

    active = 'history-rep'  # For the left nav bar become active
    show_button = 'No'
    if request.args.get('report_id'):
        report_id = request.args.get('report_id')
        connection1 = getCursor()
        connection1.execute(
            """SELECT report_id,term,due_date,student_id FROM 6_month_report r WHERE r.student_id = (select student_id from 6_month_report where report_id=%s) AND r.report_progress_id=6;""",
            (report_id,))
        show_button = 'Yes'
    elif request.args.get('student_id'):
        student_id = request.args.get('student_id')
        connection1 = getCursor()
        connection1.execute("""SELECT report_id,term,due_date,student_id FROM 6_month_report r WHERE r.student_id = %s AND r.report_progress_id=6;""",
                            (student_id,))
        show_button = 'Yes'
    else:
        user_id = request.cookies.get('user_id')
        connection1 = getCursor()
        connection1.execute("""SELECT report_id,term,due_date,r.student_id FROM 6_month_report r JOIN student s
        ON s.student_id = r.student_id WHERE s.user_id = %s AND r.report_progress_id=6;""", (user_id,))

    report_list = connection1.fetchall()
    return render_template('/student/history_report.html', report_list=report_list, active=active, show_button=show_button)
