drop schema if exists `639_LU`;
CREATE DATABASE `639_LU`;
USE `639_LU`;


CREATE TABLE department (
  department_id INT AUTO_INCREMENT PRIMARY KEY,
  department_name VARCHAR(100)
);

CREATE TABLE user (
  user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email_address VARCHAR(100) NOT NULL,
  password VARCHAR(50) NOT NULL,
  department_id INT,
  user_role ENUM('student','supervisor','convenor', 'admin', 'chair') NOT NULL,
  admin_reviewed bool NOT NULL, -- When this is true, it means that the admin has approved the newly registered students and supervisors before they can use the system.
  admin_reject bool,
  reminder int NULL, # 0: no reminder, 1: Reminders of incomplete reports 2: Reminder report has been completed
  FOREIGN KEY (department_id) REFERENCES department(department_id) ON DELETE CASCADE
);


CREATE TABLE student (
  student_id INT PRIMARY KEY AUTO_INCREMENT, -- Start from 10001
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone VARCHAR(20),
  enrolment_date VARCHAR(20),
  address VARCHAR(255),
  part_full_time VARCHAR(10),
  thesis_title VARCHAR(255),
  other_email VARCHAR(100),
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
)AUTO_INCREMENT=10001;

CREATE TABLE reminder (
	reminder_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Who will receive the reminder
    student_id INT NOT NULL, -- This reminder about who reports
    type ENUM('message','action','F_section') DEFAULT 'message',  -- This type F_section is added for sending message to students when chair reviewed Section F
	reminder_info VARCHAR(255),
	FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);


CREATE TABLE supervisor (
  supervisor_id INT PRIMARY KEY AUTO_INCREMENT, -- Start from 10001
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone VARCHAR(20),
  is_convenor bool NOT NULL, -- When this is true, it means that the supervisor is also a convenor
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
)AUTO_INCREMENT=10001;


CREATE TABLE staff (
staff_id INT PRIMARY KEY AUTO_INCREMENT,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
phone VARCHAR(20),
user_id INT NOT NULL,
FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
)AUTO_INCREMENT=10001;


CREATE TABLE student_supervisor (
  student_id INT,
  supervisor_id INT,
  supervisor_type ENUM('main', 'associate', 'other') NOT NULL,  -- according to the 6MR, there are three types of supervisor
  PRIMARY KEY(student_id,supervisor_id),
  FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
  FOREIGN KEY (supervisor_id) REFERENCES supervisor(supervisor_id) ON DELETE CASCADE
);


CREATE TABLE report_progress (
  report_progress_id INT PRIMARY KEY,
  in_charge_role ENUM('student', 'supervisor', 'convenor', 'admin', 'chair','null')  -- when report at the chair, it means student have submitted F section to complain; the value 'null' means report has been marked completed by admin


);


CREATE TABLE 6_month_report (
  report_id INT PRIMARY KEY AUTO_INCREMENT,
  student_id INT NOT NULL,
  report_progress_id INT NOT NULL,
  due_date DATE,    -- report due date according to project introduction
  term ENUM('1st', '2nd', '3rd','4th', '5th', '6th' ) NOT NULL,  -- related to Section B last part for report term
  chair_action  VARCHAR(255),
  main_check ENUM('confirm','reject','in progress','checked'),
  main_message VARCHAR(255),
  FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
  FOREIGN KEY (report_Progress_id) REFERENCES report_progress(report_progress_id) ON DELETE CASCADE
);


CREATE TABLE updated_time (
  report_id INT,
  sec_A DATETIME,     -- student submitting or save draft time for section A
  sec_B DATETIME,     -- student submitting or save draft time  for section B
  sec_C DATETIME,     -- student submitting or save draft time  for section C
  sec_D DATETIME,     -- student submitting or save draft time  for section D
  sec_F DATETIME,          -- student submitting or save draft time for section F
  sec_E_main DATETIME,    -- principal or main supervisor report submitting or save draft time
  sec_E_associate DATETIME,     -- associate supervisor report submitting or save draft time
  sec_E_other DATETIME,        -- other supervisor report submitting or save draft time
  convenor DATETIME,          -- convenor report submitting or save draft time
  completed_date DATETIME,  -- mark 'done' by admin
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
) ;


CREATE TABLE sectionA_scholar (
  scholar_id INT PRIMARY KEY AUTO_INCREMENT,
  report_id INT NOT NULL,
  scholar_name VARCHAR(50) ,
  scholar_value DECIMAL(10,2) ,
  scholar_tenure VARCHAR(255) ,
  scholar_end_date DATE NOT NULL,
  content_status ENUM('Draft', 'Submitted') NOT NULL,
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
) ;


CREATE TABLE sectionA_employment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    teaching VARCHAR(255),
    research VARCHAR(255),
    other VARCHAR(255),
    content_status ENUM('Draft', 'Submitted') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionB_1 (           --  if each column field is Null, indicating not completed. otherwise there should be a completed date
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    induction_program DATE,
    Mutual_expectation DATE,
    MEA DATE,
    Intellectual_Property DATE,
    Thesis_proposal_seminar DATE,
    Research_proposal_approved DATE,
    PG_conference_presentation DATE,
    Thesis_Results_Seminar DATE,
    content_status ENUM('Draft', 'Submitted') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionB_2_committee (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    Human_Ethics ENUM('needed', 'approval given', 'not needed'),
    Health_and_Safety ENUM('needed', 'approval given', 'not needed'),
    Animal_Ethics ENUM('needed', 'approval given', 'not needed'),
    Institutional_Biological_Safety ENUM('needed', 'approval given', 'not needed'),
    Radiation_Protection_Officer ENUM('needed', 'approval given', 'not needed'),
    content_status ENUM('Draft', 'Submitted') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionC_1 (       -- comment 1 to 20 is coresponding to items from top 'Access_Psuper' to 'other' respectively
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    Access_Psuper ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Access_Asuper ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Psuper_expertise ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Asuper_expertise ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Qua_Psuper ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Qua_Asuper ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    TL_Psuper ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    TL_Asuper ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Courses_avail ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Workspace ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Com_facility ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    ITS_support ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Res_software ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Lib_facility ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    T_L_cen_support ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Stat_support ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Res_equipment ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Tech_support ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    Finan_resources ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
	comment_1 VARCHAR(255),
    comment_2 VARCHAR(255),
    comment_3 VARCHAR(255),
    comment_4 VARCHAR(255),
    comment_5 VARCHAR(255),
    comment_6 VARCHAR(255),
    comment_7 VARCHAR(255),
    comment_8 VARCHAR(255),
    comment_9 VARCHAR(255),
    comment_10 VARCHAR(255),
    comment_11 VARCHAR(255),
    comment_12 VARCHAR(255),
    comment_13 VARCHAR(255),
    comment_14 VARCHAR(255),
    comment_15 VARCHAR(255),
    comment_16 VARCHAR(255),
    comment_17 VARCHAR(255),
    comment_18 VARCHAR(255),
    comment_19 VARCHAR(255),
    content_status ENUM('Draft', 'Submitted') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionC_1_other (
	id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    other_title VARCHAR(255),
    other ENUM('very good', 'good', 'satisfied', 'unsatisfied', 'not relevant'),
    comment VARCHAR(255),
    content_status ENUM('Draft', 'Submitted') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionC_2 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    meeting_frequ ENUM('Weekly', 'Fortnightly', 'Monthly', 'Every 3 months', 'Half yearly','Not at all'),
    period_feedback ENUM('1 week', '2 weeks', '1 month', '3 months'),
    content_status ENUM('Draft', 'Submitted') NOT NULL,
    -- receive_feedback ENUM('Softcopy ', 'Comments on submitted material', 'Verbally', 'On a separate letter'),
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionC_2_receive_feedback (
	id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    receive_feedback ENUM('Softcopy ', 'Comments on submitted material', 'Verbally', 'On a separate letter'),
    content_status ENUM('Draft', 'Submitted') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionE (                    --  supervisor1 refer to main supervisor, supervisor2 refers to associate one, and 3 refers to other, which could be identified in the student_supervisor table
  id INT PRIMARY KEY AUTO_INCREMENT,
  supervisor_id int NOT NULL,
  report_id INT NOT NULL,
  supervisor_answer1 ENUM('Excellent', 'Good', 'Satisfactory', 'Below Average', 'Unsatisfactory'),
  supervisor_answer2 ENUM('Excellent', 'Good', 'Satisfactory', 'Below Average', 'Unsatisfactory'),
  supervisor_answer3 ENUM('Excellent', 'Good', 'Satisfactory', 'Below Average', 'Unsatisfactory'),
  supervisor_answer4 ENUM('Excellent', 'Good', 'Satisfactory', 'Below Average', 'Unsatisfactory'),
  supervisor_answer5 ENUM('Excellent', 'Good', 'Satisfactory', 'Below Average', 'Unsatisfactory'),
  supervisor_response ENUM('Yes', 'No', 'N/A'),
  supervisor_comments VARCHAR(255),
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE,
  FOREIGN KEY (supervisor_id) REFERENCES supervisor(supervisor_id) ON DELETE CASCADE
);

CREATE TABLE sectionE_Convenor(
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    user_id int NOT NULL,
    Convenor_highlight VARCHAR(255),
    Convenors_to_complete ENUM('G', 'O', 'R'), -- G for green, O for orange, R for red,
    FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE,
    Foreign key (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);



CREATE TABLE sectionD_1_objective (
  objective_id INT PRIMARY KEY AUTO_INCREMENT,
  report_id INT NOT NULL,
  obj_content VARCHAR(255) ,
  status ENUM('complete', 'incomplete'),
  comment VARCHAR(255),
  obj_change_reason VARCHAR(255),
  content_status ENUM('Draft', 'Submitted') NOT NULL,
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);


CREATE TABLE sectionD_2_covid (
  covid_id INT PRIMARY KEY AUTO_INCREMENT,
  report_id INT NOT NULL,
  comment VARCHAR(255),
  content_status ENUM('Draft', 'Submitted') NOT NULL,
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionD_3_achievements (
    achiev_id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    achievement VARCHAR(255),
    content_status ENUM('Draft', 'Submitted') NOT NULL,
	FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionD_4_objective (
  obj_id INT PRIMARY KEY AUTO_INCREMENT,
  report_id INT NOT NULL,
  objective VARCHAR(255),
  target VARCHAR(255),
  problem VARCHAR(255),
  content_status ENUM('Draft', 'Submitted') NOT NULL,
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
);

CREATE TABLE sectionD_5_objective (
  item_id INT PRIMARY KEY AUTO_INCREMENT,
  report_id INT NOT NULL,
  item VARCHAR(255),
  amount DECIMAL(10,2),
  note VARCHAR(255),
  content_status ENUM('Draft', 'Submitted') NOT NULL,
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
  );

  CREATE TABLE sectionF (
  id INT PRIMARY KEY AUTO_INCREMENT,
  report_id INT NOT NULL,
  supervisor_id INT NOT NULL,
  comment VARCHAR(255),
  talk_option  ENUM('a', 'b'),
  content_status ENUM('Draft', 'Submitted') NOT NULL,
  FOREIGN KEY (report_id) REFERENCES 6_month_report(report_id) ON DELETE CASCADE
  )


-- other notes:
-- 1. data type ENUM(val1, val2, val3, ...)	A string object that can have only one value, chosen from a list of possible values.
