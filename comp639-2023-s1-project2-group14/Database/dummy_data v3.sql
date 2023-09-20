USE `639_LU`;

INSERT INTO department (department_name)
VALUES
('DEM'),
('DTSS'),
('SOLA');



INSERT INTO user (email_address, password, department_id, user_role, admin_reviewed) VALUES
('john.doe@lincolnuni.ac.nz', 'password', 1, 'student', true),
('jane.doe@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('vic.smith@lincolnuni.ac.nz', 'password', null, 'admin', true), -- admin is not part of any department.
('bob.smith@lincolnuni.ac.nz', 'password', 1, 'student', true),
('sara.johnson@lincolnuni.ac.nz', 'password', 1, 'student', true),
('mike.lee@lincolnuni.ac.nz', 'password', 1, 'student', true),
('emily.chen@lincolnuni.ac.nz', 'password', 1, 'student', true),
('david.kim@lincolnuni.ac.nz', 'password', 1, 'student', true),
('amy.garcia@lincolnuni.ac.nz', 'password', 1, 'student', true),
('tom.brown@lincolnuni.ac.nz', 'password', 1, 'student', true),
('lisa.nguyen@lincolnuni.ac.nz', 'password', 1, 'student', true),
('sarah.johnson@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('mark.lee@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('susan.wong@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('michael.chen@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('robert.garcia@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('laura.brown@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('john.davis@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('elizabeth.taylor@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('steven.clark@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),
('karen.allen@lincolnuni.ac.nz', 'password', 1, 'supervisor', true),

('tomas.smith@lincolnuni.ac.nz', 'password', 2, 'student', true),
('jerry.johnson@lincolnuni.ac.nz', 'password', 2, 'student', true),
('mike.bush@lincolnuni.ac.nz', 'password', 2, 'student', true),
('lucy.chen@lincolnuni.ac.nz', 'password', 2, 'student', true),
('david.wang@lincolnuni.ac.nz', 'password', 2, 'student', true),
('ashley.garcia@lincolnuni.ac.nz', 'password', 2, 'student', true),
('berlienda.brown@lincolnuni.ac.nz', 'password', 2, 'student', true),
('lisa2.nguyen@lincolnuni.ac.nz', 'password', 2, 'student', true),
('sarah2.johnson@lincolnuni.ac.nz', 'password', 2, 'student', true),
('william.lee@lincolnuni.ac.nz', 'password', 2, 'student', true),



('tommy.bulin@lincolnuni.ac.nz', 'password', 3, 'student', true),
('alex.johnson@lincolnuni.ac.nz', 'password', 3, 'student', true),
('vic.bush@lincolnuni.ac.nz', 'password', 3, 'student', true),
('anthony.chen@lincolnuni.ac.nz', 'password', 3, 'student', true),
('stuart.wang@lincolnuni.ac.nz', 'password', 3, 'student', true),
('david1.garcia@lincolnuni.ac.nz', 'password', 3, 'student', true),
('mishelle.brown@lincolnuni.ac.nz', 'password', 3, 'student', true),
('lisa3.nguyen@lincolnuni.ac.nz', 'password', 3, 'student', true),
('sarah3.johnson@lincolnuni.ac.nz', 'password', 3, 'student', true),
('richel.lee@lincolnuni.ac.nz', 'password', 3, 'student', true),


('linda.bulin@lincolnuni.ac.nz', 'password', 3, 'student', false),
('sammuel.johnson@lincolnuni.ac.nz', 'password', 3, 'student', false),
('jash.bush@lincolnuni.ac.nz', 'password', 3, 'student', false),
('anthony.sun@lincolnuni.ac.nz', 'password', 3, 'student', false),
('stuart.charters@lincolnuni.ac.nz', 'password', 3, 'student', false),
('david1.malisha@lincolnuni.ac.nz', 'password', 3, 'student', false),
('mishelle.ash@lincolnuni.ac.nz', 'password', 3, 'student', false),
('lisa4.nguyen@lincolnuni.ac.nz', 'password', 3, 'student', false),
('sarah4.johnson@lincolnuni.ac.nz', 'password', 3, 'student', false),
('richel.green@lincolnuni.ac.nz', 'password', 3, 'student', false),



('Hall.Jane@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('Nicholson.Craig@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('Bui.Thuy@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('Brodala.Dorota@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('Mather.Rosemary@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('Sawada.Miyoko@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('Ajai1.Keshav@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('Ridden.Jan@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('steven1.clark@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),
('karen1.allen@lincolnuni.ac.nz', 'password', 2, 'supervisor', true),


('sarah1.johnson@lincolnuni.ac.nz', 'password', 3, 'supervisor', true),
('mark.blinda@lincolnuni.ac.nz', 'password', 3, 'supervisor', true),
('susan.wang@lincolnuni.ac.nz', 'password', 3, 'supervisor', true),
('michael.sun@lincolnuni.ac.nz', 'password', 3, 'supervisor', true),
('bush.garcia@lincolnuni.ac.nz', 'password', 3, 'supervisor', true),
('loon.brown@lincolnuni.ac.nz', 'password', 3, 'supervisor', false),
('mishely.davis@lincolnuni.ac.nz', 'password', 3, 'supervisor', false),
('jerrylin.taylor@lincolnuni.ac.nz', 'password', 3, 'supervisor', false),
('stephen.clark@lincolnuni.ac.nz', 'password', 3, 'supervisor', false),
('camoron.allen@lincolnuni.ac.nz', 'password', 3, 'supervisor', false),


('blindar.davis@lincolnuni.ac.nz', 'password', null, 'chair', true), -- chair is not part of any department.
('jashley.taylor@lincolnuni.ac.nz', 'password', 1, 'convenor', true),
('ross.clark@lincolnuni.ac.nz', 'password', 2, 'convenor', true),
('joee.allen@lincolnuni.ac.nz', 'password', 3, 'convenor', true);




INSERT INTO student (first_name, last_name, phone, enrolment_date, address, part_full_time, thesis_title, user_id)
VALUES
  ('john','Doe','555-1234','2021-07-01','123 Main St','Full-time','The Effects of Climate Change on Ecosystems',1),
  ('bob','Smith','555-5678','2021-10-01','456 Elm St','Part-time','Sustainable Water Management in Developing Countries',4),
 ('sara','Johnson','555-9012','2021-09-22','789 Oak St','Full-time','Sustainable Agriculture in Sub-Saharan Africa',5),
 ('mike','Lee','555-3456','2022-09-30','321 Pine St','Full-time','Urban Planning for Resilient Cities',6),
  ('emily','chen','555-7890','2022-09-01','654 Cedar St','Part-time','Renewable Energy in Asia',7),
 ('david','kim','555-2345','2021-10-01','987 Maple St','Full-time','Green Infrastructure in the United States',8),
  ('amy','garcia','555-6789','2021-09-01','432 Birch St','Full-time','Circular Economy in Europe',9),
 ('tom','brown','555-0123','2021-09-01','765 Walnut St','Part-time','Corporate Sustainability in Latin America',10),
('lisa','nguyen','555-4567','2021-11-01','321 Oakwood St','Full-time','Conservation Biology in Australia',11),
('tomas','smith','555-8901','2023-09-01','654 Cherry St','Full-time','Green Buildings in North America',22),
 ('jerry','johnson','555-1234','2023-09-02','655 Cherry St','Part-time','The Effects of Climate Change on New Zealand',23),
('mike','bush','555-5678','2023-09-03','656 Cherry St','Full-time','Sustainable forest Management in Developing Countries',24),
 ('lucy','chen','555-9012','2023-09-04','657 Cherry St','Part-time','Sustainable Agriculture in Asia',25),
 ('david','wang','555-3456','2023-09-05','658 Cherry St','Full-time','Rural Planning for Sydney',26),
 ('ashley','garcia','555-7890','2022-08-06','659 Cherry St','Part-time','Renewable Energy in Chongqing',27),
('berlienda','brown','555-2345','2022-10-07','660 Cherry St','Full-time','Green Infrastructure in Christchurch',28),
 ('lisa2','nguyen','555-6789','2022-09-08','661 Cherry St','Part-time','Circular Economy in USA',29),
 ('sarah2','johnson','555-0123','2021-09-09','662 Cherry St','Full-time','Corporate Sustainability in Africa',30),
 ('william','lee','555-4567','2021-09-10','663 Cherry St','Part-time','Conservation Biology in New Zealand',31),
('tommy','bulin','555-8901','2021-09-11','664 Cherry St','Full-time','Green House Gas in North America',32),
 ('alex','johnson','555-1234','2021-09-12','665 Cherry St','Part-time','Cows Breath in New Zealand',33),
 ('vic','bush','555-5678','2022-09-13','666 Cherry St','Full-time','The Effects of Climate Change on Chang Jiang River',34),
 ('anthony','chen','555-9012','2022-09-14','667 Cherry St','Part-time','Sustainable Plastic Management in Developing Countries',35),
 ('stuart','wang','555-3456','2022-09-15','668 Cherry St','Full-time','Sustainable Agriculture in Africa',36),
 ('david1','garcia','555-7890','2022-09-16','669 Cherry St','Part-time','Urban Vechles for Resilient Cities',37),
 ('mishelle','brown','555-2345','2022-09-17','670 Cherry St','Full-time','Renewable Water in Asia',38),
 ('lisa3','nguyen','555-6789','2021-09-18','671 Cherry St','Part-time','Green Infrastructure in the China',39),
 ('sarah3','johnson','555-0123','2021-09-19','672 Cherry St','Full-time','Circular Economy in Japan',40),
 ('richel','lee','555-4567','2021-09-20','673 Cherry St','Part-time','Corporate Sustainability in North Korean',41),
 ('linda','bulin','555-8901','2022-09-21','674 Cherry St','Full-time','Conservation Biology in India',42),
 ('sammuel','johnson','555-1234','2022-09-22','675 Cherry St','Part-time','Green Buildings in South America',43),
 ('jash','bush','555-5678','2022-09-23','676 Cherry St','Full-time','Green Buildings in South America',44),
 ('anthony','sun','555-9012','2021-09-24','677 Cherry St','Part-time','The Effects of Rain on Ecosystems',45),
 ('stuart','charters','555-3456','2021-09-25','678 Cherry St','Full-time','Flood Prevention Research',46),
 ('david1','malisha','555-7890','2023-09-26','679 Cherry St','Part-time','Population Research in Arab',47),
 ('mishelle','ash','555-2345','2023-09-27','680 Cherry St','Full-time','Urban Planning for inland cities',48),
 ('lisa4','nguyen','555-6789','2023-09-28','681 Cherry St','Part-time','solar power reliablity ',49),
 ('sarah4','johnson','555-0123','2021-09-29','682 Cherry St','Full-time','transportation research ',50),
 ('richel','green','555-4567','2021-09-30','683 Cherry St','Part-time','Circular Economy in Latin America',51);



INSERT INTO supervisor (first_name, last_name, phone, is_convenor, user_id)
VALUES
('jane','doe','555-1234',0,2),
 ('sarah','johon','555-5678',0,12),
 ('mark','lee','555-9012',0,13),
 ('susan','wong','555-3456',0,14),
 ('michael','chen','555-7890',0,15),
 ('robert','garcia','555-2345',0,16),
 ('laura','brown','555-6789',0,17),
 ('john','davis','555-2345',0,18),
 ('elizabeth','taylor','555-9012',0,19),
 ('steven','clark','555-3456',0,20),
 ('karen','allen','555-3457',0,21),
 ('Hall','jane','555-3458',0,52),
 ('Nicholson','craig','555-3459',0,53),
 ('Bui','thuy','555-3460',0,54),
 ('Brodala','dorota','555-3461',0,55),
 ('Mather','rosermary','555-3462',0,56),
 ('Sawada','myoko','555-3463',0,57),
 ('Ajai1','keshav','555-3464',0,58),
 ('Ridden','jane','555-3465',0,59),
 ('steven1','clark','555-3466',0,60),
 ('karen1','allen','555-3467',0,61),
 ('sarah1','johson','555-3468',0,62),
 ('mark','blenda','555-3469',0,63),
('susan','wang','555-3470',0,64),
 ('michael','sun','555-3471',0,65),
 ('bush','garcia','555-3472',0,66),
 ('loon','brown','555-3473',0,67),
 ('mishely','davis','555-3474',0,68),
 ('jerrylin','taylor','555-3475',0,69),
 ('stephen','clark','555-3476',0,70),
 ('camoron','allen','555-3477',0,71),
  ('jashley','taylor','555-3477',1,73);



INSERT INTO staff (first_name, last_name, phone, user_id) VALUES
('jashley', 'taylor', '+5566778899', 73),
('ross', 'clark', '+6677889900', 74),
( 'joee', 'allen', '+7788990012', 75),
('blindar', 'davis', '+7788990013', 72),
('vic', 'smith', '+7788990015', 3);



INSERT INTO student_supervisor (student_id, supervisor_id, supervisor_type) VALUES
(10001, 10001, 'main'),
(10001, 10002, 'associate'),
-- (10001, 10003, 'other'),
(10002, 10002, 'main'),
(10002, 10003, 'associate'),
(10002, 10004, 'other'),
(10003, 10003, 'main'),
(10003, 10004, 'associate'),
(10003, 10005, 'other'),
(10004, 10032, 'main'),
(10004, 10005, 'associate'),
(10004, 10006, 'other'),
(10005, 10005, 'main'),
(10005, 10006, 'associate'),
(10005, 10007, 'other'),
(10006, 10006, 'main'),
(10006, 10007, 'associate'),
(10006, 10008, 'other'),

(10010, 10013, 'main'),
(10011, 10014, 'associate'),
(10011, 10015, 'other'),
(10012, 10014, 'main'),
(10012, 10015, 'associate'),
(10012, 10016, 'other'),
(10013, 10015, 'main'),
(10013, 10016, 'associate'),
(10013, 10017, 'other'),
(10014, 10016, 'main'),
(10014, 10017, 'associate'),
(10014, 10018, 'other'),
(10015, 10017, 'main'),
(10015, 10018, 'associate'),
(10015, 10019, 'other'),
(10016, 10018, 'main'),
(10016, 10019, 'associate'),
(10016, 10020, 'other'),


(10032, 10022, 'main'),
(10032, 10023, 'associate'),
(10032, 10024, 'other'),
(10033, 10023, 'main'),
(10033, 10024, 'associate'),
(10033, 10025, 'other'),
(10034, 10024, 'main'),
(10034, 10025, 'associate'),
(10034, 10026, 'other'),
(10035, 10025, 'main'),
(10035, 10026, 'associate'),
(10035, 10027, 'other'),
(10036, 10026, 'main'),
(10036, 10027, 'associate'),
(10036, 10028, 'other'),
(10037, 10028, 'main'),
(10037, 10029, 'associate'),
(10037, 10030, 'other');



INSERT INTO report_progress (report_progress_id, in_charge_role) VALUES
(1, 'student'),
(2, 'supervisor'),
(3, 'convenor'),
-- (4, 'chair'),
(5, 'admin'),
(6, null);


INSERT INTO 6_month_report (student_id, report_progress_id, due_date, term, chair_action,main_check,main_message) VALUES
(10001, 6, '2022-06-30', '1st', 'Review and provide feedback on student\'s initial report draft.','checked',null),
(10001, 6, '2022-12-31', '2nd', 'Review and provide feedback on student\'s initial report draft.','checked',null),
(10002, 6, '2022-12-31', '1st', 'Review and provide feedback on student\'s progress in developing their report.','checked',null),
(10002, 3, '2023-06-30', '2nd',null,'checked',null),
(10003, 6, '2022-12-31', '4th', 'Review and provide feedback on student\'s methods and analysis.','checked',null),
(10003, 2, '2023-06-30', '5th',null,'checked',null),
(10001, 1, '2023-06-30', '3rd',null,null,null),
(10004, 3, '2023-06-30', '1st', null,'checked',null),
(10005, 3, '2023-06-30', '1st', null,'checked',null),
(10010, 5, '2023-06-30', '2nd', null,'checked',null),
(10010, 6, '2022-12-31', '1st', null,'checked',null),
(10011, 5, '2023-06-30', '1st', null,'checked',null),
(10028, 5, '2023-06-30', '1st', null,'checked',null),
(10006, 3, '2023-06-30', '1st', null,'checked',null),
(10007, 3, '2023-06-30', '1st', null,'checked',null),
(10032, 2, '2023-06-04', '1st', null,null,null),
(10012, 3, '2023-06-04', '1st', null,'checked',null),
(10016, 1, '2023-06-04', '1st', null,null,null);



INSERT INTO updated_time (report_id, sec_A, sec_B, sec_C, sec_D, sec_F, sec_E_main, sec_E_associate, sec_E_other, convenor, completed_date) VALUES
(2, '2022-11-01 12:00:00','2022-11-02 09:00:00','2022-11-02 14:00:00','2022-11-03 19:00:00', '2022-11-05 10:30:00', '2022-11-07 14:20:00', '2022-12-10 16:45:00', '2022-12-13 09:10:00', '2022-12-15 11:00:00', '2022-12-20 17:30:00'),
(7, '2023-04-11 12:00:00', '2023-04-18 12:00:00', '2023-04-20 12:00:00', '2023-04-25 16:00:00',null,null,null,null,null,null),
(3, '2022-11-01 12:00:00','2022-11-02 09:00:00','2022-11-02 14:00:00','2022-11-03 10:30:00', '2022-11-06 11:45:00', '2022-11-08 15:00:00', '2022-11-11 09:30:00', '2022-11-14 10:45:00', '2022-12-16 12:15:00', '2022-12-21 14:30:00'),
(4, '2023-03-11 12:00:00','2023-03-12 09:00:00','2023-04-02 14:00:00','2023-04-04 11:00:00', '2023-04-07 09:00:00', '2023-04-09 12:45:00', '2023-04-09 12:45:00', '2023-04-12 11:45:00',null, null),
(5, '2022-11-11 12:00:00','2022-11-13 09:00:00','2022-11-15 14:00:00','2022-12-05 13:15:00', '2022-12-08 14:30:00', '2022-12-10 10:45:00', '2022-12-13 12:15:00', '2022-12-16 09:00:00', '2022-12-18 11:30:00', '2022-12-23 15:45:00'),
(6, '2023-03-15 12:00:00','2023-03-16 09:00:00','2023-04-05 14:00:00','2023-04-06 09:45:00', '2023-04-09 11:00:00', '2023-04-11 14:15:00', null, null, null,null),
(1, '2022-03-01 12:00:00','2022-03-02 09:00:00','2022-04-02 14:00:00','2022-04-03 19:00:00', '2022-05-05 10:30:00', '2022-05-07 14:20:00', '2022-05-10 16:45:00', '2022-05-13 09:10:00', '2022-05-15 11:00:00', '2022-05-12 17:30:00'),
(8, '2023-03-12 11:00:00','2023-03-12 12:00:00','2023-04-01 13:00:00','2023-04-04 11:00:00', '2023-04-06 09:00:00', '2023-04-09 10:45:00', '2023-04-09 11:45:00', '2023-04-10 10:30:00',null, null),
(9, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', '2023-04-09 15:45:00', '2023-04-10 11:45:00',null, null),
(12, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', '2023-04-09 15:45:00', '2023-04-10 11:45:00','2023-04-12 11:45:00', null),
(13, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', '2023-04-09 15:45:00', '2023-04-10 11:45:00','2023-04-12 11:45:00', null),
(10, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', '2023-04-09 15:45:00', '2023-04-10 11:45:00','2023-04-12 11:45:00', null),
(11, '2022-11-11 12:00:00','2022-11-13 09:00:00','2022-11-15 14:00:00','2022-12-05 13:15:00', '2022-12-08 14:30:00', '2022-12-10 10:45:00', '2022-12-13 12:15:00', '2022-12-16 09:00:00', '2022-12-18 11:30:00', '2022-12-23 15:45:00'),
(14, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', '2023-04-09 15:45:00', '2023-04-10 11:45:00', null, null),
(15, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', '2023-04-09 15:45:00', '2023-04-10 11:45:00', null, null),
(16, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', null, null, null, null),
(17, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00','2023-03-12 11:00:00', '2023-04-08 15:00:00', '2023-04-09 14:45:00', '2023-04-09 15:45:00', '2023-04-10 11:45:00', null, null),
(18, '2023-03-09 08:30:00','2023-03-10 10:00:00','2023-03-11 14:00:00', null,  null,  null, null, null, null, null);

INSERT INTO sectionA_employment (report_id, teaching, research, other,content_status) VALUES
(2, '8 hour/per week; 12 weeks; Supervisor:jane	doe', null, null,'Submitted'),
(7, '7 hours/per week; 10 weeks; Supervisor:jane doe', null, null,'Draft'),
(3, null, '10 hours/per week; 6 months; Supervisor: sarah johon', null,'Submitted'),
(4, null, '8 hours/per week; 3 months; Supervisor: sarah johon', null,'Submitted'),
(5, null, null, ' field trip overseas; 8 hours/per week; 3 months; supervisor: mark	lee','Submitted'),
(6, null, null, 'field trip overseas; 8 hours/per week; 3 months; supervisor: mark	lee','Submitted'),
(8, null, '7 hours/per week; 3 months; Supervisor: Li johon', null,'Submitted'),
(9, null, '5 hours/per week; 5 months; Supervisor: Sam johon', null,'Submitted'),
(12, null, '5 hours/per week; 5 months; Supervisor: Wang johon', null,'Submitted'),
(13, null, '5 hours/per week; 5 months; Supervisor: Zheng johon', null,'Submitted'),
(10, null, '5 hours/per week; 5 months; Supervisor: Nicholson', null,'Submitted'),
(1, null, '5 hours/per week; 5 months; Supervisor: Nicholson', null,'Submitted');




INSERT INTO sectionA_scholar (report_id, scholar_name, scholar_value, scholar_tenure, scholar_end_date,content_status) VALUES
(2, 'Merit-based', 5000.00, '1 year', '2023-08-08','Submitted'),
(2, 'Need-based', 2500.00, '1 year', '2023-08-08','Submitted'),
(7, 'Athletic', 7500.00, '2 years', '2024-05-08','Draft'),
(7, 'Academic', 5500.00, '1 year', '2023-08-08','Draft'),
(3, 'Academic', 10000.00, '2 years', '2024-05-08','Submitted'),
(4, 'Artistic', 3000.00, '1 year', '2023-02-08','Submitted'),
(4, 'Community Service', 1500.00, '1 year', '2024-01-08','Submitted'),
(8, 'Artistic', 3000.00, '3 year', '2023-02-08','Submitted'),
(8, 'Community Service', 1400.00, '1 year', '2024-01-08','Submitted'),
(9, 'Artistic', 3000.00, '2 year', '2023-02-08','Submitted'),
(9, 'Community Service', 1300.00, '1 year', '2024-01-08','Submitted'),
(12, 'Community checking', 1200.00, '1 year', '2024-01-08','Submitted'),
(13, 'library Service', 1100.00, '1 year', '2024-01-08','Submitted'),
(10, 'Community Service', 1300.00, '1 year', '2024-01-08','Submitted'),
(1, 'Community Service', 1300.00, '1 year', '2024-01-08','Submitted');


INSERT INTO sectionB_1 (report_id, induction_program, Mutual_expectation, MEA, Intellectual_Property, Thesis_proposal_seminar, Research_proposal_approved, PG_conference_presentation, Thesis_Results_Seminar,content_status) VALUES
(2, '2022-11-01', '2022-11-02', '2022-11-09', '2022-11-12', '2022-11-20', '2022-11-25', '2022-12-01', '2022-12-07','Submitted'),
(7, '2023-01-01', '2023-01-02',  NULL, NULL,  NULL,  NULL, NULL,  NULL,'Draft'),
(3, '2022-10-03', '2022-11-22', '2022-12-09', '2022-12-12', '2022-12-20', '2022-12-25', '2022-12-26', '2022-12-27','Submitted'),
(4, '2023-01-10', '2023-02-02',  '2023-03-02','2023-04-02',  '2023-04-12',  NULL, NULL,  NULL,'Submitted'),
(3, '2022-10-13', '2022-10-22', '2022-11-09', '2022-11-12', '2022-11-20', '2022-12-05', '2022-12-16', '2022-12-17','Submitted'),
(6,'2023-01-12', '2023-01-22',  '2023-03-02', '2023-03-22',  null,  NULL, NULL,  NULL,'Submitted'),
(8, '2023-01-11', '2023-02-01',  '2023-03-03','2023-04-01',  '2023-04-12',  NULL, NULL,  NULL,'Submitted'),
(9, '2023-01-12', '2023-02-03',  '2023-03-04','2023-04-05',  '2023-04-12',  NULL, NULL,  NULL,'Submitted'),
(12, '2023-01-12', '2023-02-03',  '2023-03-04','2023-04-05',  '2023-04-12',  NULL, NULL,  NULL,'Submitted'),
(13, '2023-01-12', '2023-02-03',  '2023-03-04','2023-04-05',  '2023-04-12',  NULL, NULL,  NULL,'Submitted'),
(10, '2023-01-12', '2023-02-03',  '2023-03-04','2023-04-05',  '2023-04-12',  NULL, NULL,  NULL,'Submitted'),
(1, '2022-04-13', '2022-04-22', '2022-05-09', '2022-05-12', '2022-05-20', '2022-06-05', '2022-06-16', '2022-06-17','Submitted');


INSERT INTO sectionB_2_committee (report_id, Human_Ethics, Health_and_Safety, Animal_Ethics, Institutional_Biological_Safety, Radiation_Protection_Officer,content_status) VALUES
(2, 'needed', 'approval given', 'not needed', 'approval given', 'needed','Submitted'),
(7, 'not needed', 'not needed', 'approval given', 'needed', 'approval given','Draft'),
(3, 'approval given', 'needed', 'needed', 'needed', 'not needed','Submitted'),
(4, 'not needed', 'not needed', 'not needed', 'not needed', 'not needed','Submitted'),
(5, 'approval given', 'not needed', 'not needed', 'needed', 'not needed','Submitted'),
(6, 'needed', 'needed', 'not needed', 'needed', 'needed','Submitted'),
(8, 'approval given', 'not needed', 'not needed', 'needed', 'not needed','Submitted'),
(9, 'needed', 'needed', 'not needed', 'needed', 'needed','Submitted'),
(12, 'needed', 'needed', 'not needed', 'needed', 'needed','Submitted'),
(13, 'needed', 'needed', 'not needed', 'needed', 'needed','Submitted'),
(10, 'needed', 'needed', 'not needed', 'needed', 'needed','Submitted'),
(1, 'needed', 'needed', 'not needed', 'needed', 'needed','Submitted');


INSERT INTO sectionC_1 (report_id, Access_Psuper, Access_Asuper, Psuper_expertise,Asuper_expertise, Qua_Psuper, Qua_Asuper, TL_Psuper, TL_Asuper, Courses_avail, Workspace, Com_facility, ITS_support, Res_software, Lib_facility, T_L_cen_support, Stat_support, Res_equipment, Tech_support, Finan_resources, comment_1, comment_2, comment_3, comment_4, comment_5, comment_6, comment_7, comment_8, comment_9, comment_10, comment_11, comment_12, comment_13, comment_14, comment_15, comment_16, comment_17, comment_18, comment_19,content_status) VALUES
(2, 'very good', 'good', 'satisfied', 'unsatisfied', 'very good', 'satisfied', 'good', 'good', 'very good', 'satisfied', 'unsatisfied', 'very good', 'good', 'very good', 'good', 'very good', 'good', 'good', 'unsatisfied', 'This school has great facilities, but sometimes the equipment in the computer lab can be a bit outdated.', 'The library is a great place to study, but sometimes it can get a bit noisy.', 'The teachers are generally very helpful and knowledgeable, but there are a few who could be more engaging in class.', 'The IT department is very helpful when you have technical problems.', 'Ive had some trouble with the registration process for courses.', null,null,null,null,null,null,null,null,null,null,null,null,null,null,'Submitted'),
(7, 'good', 'satisfied', 'satisfied', 'good', 'satisfied', 'good', 'not relevant', 'good', 'very good', 'unsatisfied', 'satisfied', 'not relevant', 'very good', 'very good', 'satisfied', 'satisfied', 'good', 'good', 'satisfied',  'The facilities are generally pretty good, but sometimes it can be hard to find an available computer in the computer lab.', 'The library is a great resource, but sometimes it can be a bit crowded.', 'The professors are knowledgeable and approachable.', 'The IT department is generally helpful, but sometimes it can take a while to get a response.',null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 'Draft'),
(3, 'satisfied', 'satisfied', 'satisfied', 'very good', 'very good', 'good', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied',  'The facilities are generally pretty good, but the computer lab can get a bit crowded at peak times.', 'The library is a great place to study, and the librarians are always helpful.', 'Most of the professors are knowledgeable and approachable, but there are a few who could be more engaging.', 'The IT department is generally helpful.', null,null,null,null,'Ive had no major issues with the resources available to me at this school.', null, null,null, null, null, null, null, null, null, null, 'Submitted'),
(4, 'satisfied', 'satisfied', 'satisfied', 'very good', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied', null, null, null,null, null,null,null,null,null, null, null,null, null, null, null, null, null, null, 'Submitted'),
(6, 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied', null, null, null,null, null,null,null,null,null, null,null, null, null, null, null, null, null, null, 'Submitted'),
(6, 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied',null, null, null,null, null,null,null,null,null,  null,null, null, null, null, null, null, null, null, 'Submitted'),
(9, 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied',null, null, null,null, null,null,null,null,null,  null,null, null, null, null, null, null, null, null, 'Submitted'),
(12, 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied',null, null, null,null, null,null,null,null,null,  null,null, null, null, null, null, null, null, null, 'Submitted'),
(13, 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied',null, null, null,null, null,null,null,null,null,  null,null, null, null, null, null, null, null, null, 'Submitted'),
(8, 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied',null, null, null,null, null,null,null,null,null,  null,null, null, null, null, null, null, null, null, 'Submitted'),
(10, 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied','satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied', 'satisfied',null, null, null,null, null,null,null,null,null,  null,null, null, null, null, null, null, null, null, 'Submitted'),
(1, 'satisfied', 'satisfied', 'satisfied', 'very good', 'very good', 'good', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'good', 'good', 'satisfied', 'satisfied', 'satisfied', 'satisfied', 'good', 'satisfied',  'The facilities are generally pretty good, but the computer lab can get a bit crowded at peak times.', 'The library is a great place to study, and the librarians are always helpful.', 'Most of the professors are knowledgeable and approachable, but there are a few who could be more engaging.', 'The IT department is generally helpful.', null,null,null,null,'Ive had no major issues with the resources available to me at this school.', null, null,null, null, null, null, null, null, null, null, 'Submitted');

INSERT INTO sectionC_1_other (report_id,other_title,other,comment,content_status) VALUES
(2,'First','good','Comment 1','Submitted'),
(7,'Second-1','very good','Comment 2-1','Draft'),
(3,'Third','satisfied','Comment 3','Submitted'),
(4,'Fourth','unsatisfied','Comment 4','Submitted'),
(5,'Fifth','satisfied','Comment 5','Submitted'),
(6,'Sixth','not relevant','Comment 6','Submitted'),
(9,'Sixth','not relevant','Comment 6','Submitted'),
(12,'Sixth','not relevant','Comment 6','Submitted'),
(13,'Sixth','not relevant','Comment 6','Submitted'),
(8,'Sixth','not relevant','Comment 6','Submitted'),
(10,'Sixth','satisfied','Comment 6','Submitted'),
(1,'Sixth','satisfied','Comment 6','Submitted');

INSERT INTO sectionC_2 (report_id, meeting_frequ, period_feedback,content_status) VALUES
(2, 'Weekly', '1 week','Submitted'),
(7, 'Fortnightly', '2 weeks','Draft'),
(3, 'Monthly', '1 month','Submitted'),
(4, 'Every 3 months', '3 months','Submitted'),
(5, 'Fortnightly', '2 weeks','Submitted'),
(6, 'Not at all', NULL,'Submitted'),
(9, 'Not at all', NULL,'Submitted'),
(12, 'Not at all', NULL,'Submitted'),
(13, 'Not at all', NULL,'Submitted'),
(8, 'Not at all', NULL,'Submitted'),
(10, 'Not at all','2 weeks','Submitted'),
(1, 'Not at all','2 weeks','Submitted');



INSERT INTO sectionC_2_receive_feedback (report_id,receive_feedback,content_status) VALUES
(2,'Comments on submitted material','Submitted'),
(2,'Softcopy','Submitted'),
(7,'Softcopy','Draft'),
(7,'Comments on submitted material','Draft'),
(3,'On a separate letter','Submitted'),
(4,'Verbally','Submitted'),
(5,'Comments on submitted material','Submitted'),
(6,NULL,'Submitted'),
(9,'Comments on submitted material','Submitted'),
(12,'Comments on submitted material','Submitted'),
(13,'Comments on submitted material','Submitted'),
(8,'Comments on submitted material','Submitted'),
(10,'Comments on submitted material','Submitted'),
(1,'Comments on submitted material','Submitted');

INSERT INTO sectionD_1_objective (report_id, obj_content, status, comment, obj_change_reason,content_status) VALUES
(2, 'Analyzing the effectiveness of community-based water management practices.', 'complete',NULL, NULL,'Submitted'),
(2, 'Developing sustainable water management strategies for smallholder farmers.', 'complete', NULL, NULL,'Submitted'),
(7, 'Developing sustainable water management strategies for smallholder farmers.', 'incomplete', 'Need more resources', 'Changed priorities','Draft'),
(7, 'Evaluating the impact of water scarcity on health and livelihoods in rural areas.', 'complete', 'everything is perfect', 'Nothing','Draft'),
(3, 'Evaluating the impact of water scarcity on health and livelihoods in rural areas.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(5, 'Examining the role of agroforestry in promoting food security and climate resilience.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(5, 'Investigating the adoption and impact of conservation agriculture practices.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(6, 'Assessing the effectiveness of agricultural extension services in promoting sustainable farming practices.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(4, 'Developing sustainable water management strategies for smallholder farmers.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(9, 'Developing sustainable water management strategies for smallholder farmers.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(12, 'Developing sustainable water management strategies for smallholder farmers.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(13, 'Developing sustainable water management strategies for smallholder farmers.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(8, 'Developing sustainable water management strategies for smallholder farmers.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(10, 'Investigating the adoption and impact of conservation agriculture practices.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted'),
(1, 'Investigating the adoption and impact of conservation agriculture practices.', 'incomplete', 'Need more resources', 'Changed priorities','Submitted');


INSERT INTO sectionD_2_covid (report_id, comment,content_status) VALUES
(2, "Our research plan was significantly impacted by travel restrictions, which prevented us from conducting field work as planned.",'Submitted'),
(2, "The university closure prevented us from accessing our lab for several months, which delayed our research timeline.",'Submitted'),
(2, "Participant survey opportunities were limited due to the pandemic, which impacted our data collection.",'Submitted'),
(7, "Financial hardship due to the pandemic affected our research budget, and we had to make adjustments to our project plan.",'Draft'),
(7, "We had to prioritize the well-being of our research team, and implemented measures to support their social, emotional, and mental health.",'Draft'),
(3, "The pandemic had a significant impact on our research plan, but we were able to adapt and make changes to our project timeline.",'Submitted'),
(4, "We experienced delays in data collection and analysis due to the pandemic, which affected our ability to meet our research objectives.",'Submitted'),
(5, "Our research team experienced significant stress and anxiety due to the pandemic, which impacted their ability to focus on research tasks.",'Submitted'),
(6, "We had to modify our research methods in order to comply with safety protocols related to the pandemic.",'Submitted'),
(6, "The pandemic created uncertainty and instability in our research environment, which required us to be flexible and adaptable in our approach.",'Submitted'),
(9, "The pandemic created uncertainty and instability in our research environment, which is really hard to focus on study.",'Submitted'),
(12, "The pandemic created uncertainty and instability in our research environment, which is really hard to focus on study.",'Submitted'),
(13, "The pandemic created uncertainty and instability in our research environment, which is really hard to focus on study.",'Submitted'),
(8, "The pandemic created uncertainty and instability in our research environment, which is really hard to focus on study.",'Submitted'),
(10, "Our research team experienced significant stress and anxiety due to the pandemic, which impacted their ability to focus on research tasks.",'Submitted'),
(1, "Our research team experienced significant stress and anxiety due to the pandemic, which impacted their ability to focus on research tasks.",'Submitted');

INSERT INTO sectionD_3_achievements (report_id, achievement,content_status) VALUES
(2, "Presented a poster on my research at the International Conference on Applied Mathematics",'Submitted'),
(2, "Published a paper on the application of machine learning in finance in the Journal of Financial Engineering",'Submitted'),
(7, "Participated in a workshop on data visualization techniques at the Data Science Symposium",'Draft'),
(3, "Participated in a workshop on data visualization techniques at the Data Science Symposium",'Submitted'),
(3, "Organized a panel discussion on the future of artificial intelligence in education",'Submitted'),
(4, "Delivered a talk on the ethics of algorithmic decision making at the Institute for Ethics in AI",'Submitted'),
(5, "Co-authored a book chapter on the history of statistics in social sciences",'Submitted'),
(5, "Won a research grant from the National Science Foundation for my project on predicting stock prices",'Submitted'),
(5, "Developed a new statistical model for analyzing election results, which was presented at a local election commission",'Submitted'),
(5, "Received a teaching award for my innovative use of technology in the classroom",'Submitted'),
(6, "Created a new online course on data analysis and visualization for non-technical audiences",'Submitted'),
(9, "Created a new online advanced programming analysis and visualization for non-technical audiences",'Submitted'),
(12, "Created a new online advanced programming analysis and visualization for non-technical audiences",'Submitted'),
(13, "Created a new online advanced programming analysis and visualization for non-technical audiences",'Submitted'),
(8, "Created a new online advanced programming analysis and visualization for non-technical audiences",'Submitted'),
(10, "Developed a new statistical model for analyzing election results, which was presented at a local election commission",'Submitted'),
(1, "Developed a new statistical model for analyzing election results, which was presented at a local election commission",'Submitted');



INSERT INTO sectionD_4_objective (report_id, objective, target, problem,content_status) VALUES
(2, 'Evaluating the impact of water scarcity on health and livelihoods in rural areas.', '2023-01-01', 'Lack of understanding on the relationship between climate change and marine ecosystems','Submitted'),
(7, 'To develop new machine learning algorithms for predictive maintenance',  '2023-07-01','To achieve a reduction of unplanned downtime by 50%','Draft'),
(7, 'Assessing the effectiveness of agricultural extension services in promoting sustainable farming practices.', '2023-09-01', 'Current drug delivery systems have limitations in targeting cancer cells specifically','Draft'),
(3, 'To develop new machine learning algorithms for predictive maintenance',  '2023-10-01','To achieve a reduction of unplanned downtime by 50%','Submitted'),
(4, 'Evaluating the impact of water scarcity on health and livelihoods in rural areas.', '2023-01-01','To identify gene targets for improving yield and stress tolerance in target crops', 'Submitted'),
(5, 'Assessing the effectiveness of agricultural extension services in promoting sustainable farming practices.', '2023-09-01', 'Current drug delivery systems have limitations in targeting cancer cells specifically','Submitted'),
(6, 'To investigate the relationship between air pollution and respiratory diseases in urban areas', '2023-09-01', 'Lack of comprehensive studies on the relationship between air pollution and respiratory diseases in urban areas','Submitted'),
(9, 'To investigate the connection between air pollution and respiratory diseases in urban areas', '2023-09-01', 'Lack of comprehensive studies on the relationship between air pollution and respiratory diseases in urban areas','Submitted'),
(12, 'To investigate the connection between air pollution and respiratory diseases in urban areas', '2023-09-01', 'Lack of comprehensive studies on the relationship between air pollution and respiratory diseases in urban areas','Submitted'),
(13, 'To investigate the connection between air pollution and respiratory diseases in urban areas', '2023-06-01', 'Lack of comprehensive studies on the relationship between air pollution and respiratory diseases in urban areas','Submitted'),
(10, 'Assessing the effectiveness of agricultural extension services in promoting sustainable farming practices.', '2023-08-01', 'Current drug delivery systems have limitations in targeting cancer cells specifically','Submitted'),
(1, 'Assessing the effectiveness of agricultural extension services in promoting sustainable farming practices.', '2023-08-01', 'Current drug delivery systems have limitations in targeting cancer cells specifically','Submitted');

INSERT INTO sectionD_5_objective (report_id, item, amount, note,content_status) VALUES
(2, 'Laboratory supplies', 2000.00, 'Purchase necessary chemicals and consumables','Submitted'),
(2, 'Fieldwork expenses', 5000.00, 'Travel expenses and equipment rental for field data collection','Submitted'),
(7, 'Laboratory supplies', 2000.00, 'Purchase necessary chemicals and consumables','Draft'),
(7, 'Fieldwork expenses', 5000.00, 'Travel expenses and equipment rental for field data collection','Draft'),
(3, 'Publication fees', 1500.00, 'Expected publication fees for manuscripts in progress','Submitted'),
(4, 'Conference travel', 3000.00, 'Registration fees and travel expenses to present research at upcoming conference','Submitted'),
(5, 'Software licenses', 1000.00, 'Renewal of software licenses for data analysis','Submitted'),
(6, 'Equipment maintenance', 2500.00, 'Routine maintenance and repairs for laboratory equipment','Submitted'),
(9, 'Equipment checking', 500.00, 'Routine maintenance and repairs for classroom carpet','Submitted'),
(12, 'Equipment checking', 500.00, 'Routine maintenance and repairs for classroom carpet','Submitted'),
(13, 'Equipment checking', 500.00, 'Routine maintenance and repairs for classroom carpet','Submitted'),
(8, 'Equipment checking', 500.00, 'Routine maintenance and repairs for classroom carpet','Submitted'),
(10, 'Software licenses', 1000.00, 'Renewal of software licenses for data analysis','Submitted'),
(1, 'Software licenses', 1000.00, 'Renewal of software licenses for data analysis','Submitted');


INSERT INTO sectionE (supervisor_id, report_id, supervisor_answer1, supervisor_answer2, supervisor_answer3, supervisor_answer4, supervisor_answer5, supervisor_response, supervisor_comments)
VALUES
(10001, 2, 'Good', 'Excellent', 'Satisfactory', 'Below Average', 'Unsatisfactory', 'Yes', 'Well done!'),
(10002, 2, 'Good', 'Good', 'Good', 'Below Average', 'Unsatisfactory', 'Yes', 'Well done!'),
(10002, 3, 'Excellent', 'Good', 'Excellent', 'Good', 'Good', 'No', NULL),
(10003, 3, 'Excellent', 'Excellent', 'Excellent', 'Excellent', 'Excellent', 'No', NULL),
(10003, 4, 'Satisfactory', 'Satisfactory', 'Satisfactory', 'Satisfactory', 'Satisfactory', 'N/A', NULL),
(10004, 4,'Good', 'Good', 'Satisfactory', 'Satisfactory', 'Satisfactory', 'N/A', NULL),
(10004, 5, 'Below Average', 'Unsatisfactory', 'Unsatisfactory', 'Unsatisfactory', 'Unsatisfactory', 'Yes', 'Needs improvement'),
(10005, 5, 'Below Average', 'Unsatisfactory', 'Unsatisfactory', 'Unsatisfactory', 'Unsatisfactory', 'No', 'Needs improvement'),
(10005, 6, 'Excellent', 'Good', 'Satisfactory', 'Below Average', 'Unsatisfactory', 'Yes', 'Some comments from supervisor 1'),
(10003, 6, 'Excellent', 'Excellent', 'Satisfactory', 'Excellent', 'Excellent', 'Yes', 'Some comments from supervisor 1'),
(10013, 10, 'Excellent', 'Excellent', 'Satisfactory', 'Excellent', 'Excellent', 'Yes', 'Some comments from supervisor 1'),
(10014, 10, 'Excellent', 'Good', 'Good', 'Excellent', 'Good', 'Yes', 'Some comments from supervisor 1'),
(10006, 12, 'Excellent', 'Good', 'Good', 'Excellent', 'Good', 'Yes', 'Some comments from supervisor suggestion'),
(10007, 13, 'Excellent', 'Good', 'Good', 'Excellent', 'Good', 'Yes', 'Some comments from supervisor suggestion'),
(10004, 8, 'Excellent', 'Good', 'Good', 'Excellent', 'Good', 'Yes', 'Some comments from supervisor suggestion'),
(10005, 9, 'Excellent', 'Good', 'Good', 'Excellent', 'Good', 'Yes', 'Some comments from supervisor suggestion'),
(10001, 1, 'Excellent', 'Good', 'Excellent', 'Excellent', 'Good', 'Yes', 'Great'),
(10002, 1, 'Excellent', 'Excellent', 'Good', 'Excellent', 'Good', 'No', 'Some comments from supervisor suggestion');

INSERT INTO sectionE_Convenor (user_id, report_id, Convenor_highlight, Convenors_to_complete)
VALUES
(73, 2, 'Highlighted comment for Convenor', 'G'),
(73, 3, 'Highlighted comment for Convenor', 'G'),
(73, 5, 'Highlighted comment for Convenor', 'R'),
(73, 1, 'Highlighted comment for Convenor', 'O'),
(74, 10, 'Highlighted comment for Convenor', 'O'),
(74, 11, 'Highlighted comment for Convenor', 'O'),
(74, 12, 'Highlighted comment for Convenor', 'R'),
(75, 13, 'Highlighted comment for Convenor', 'R');


INSERT INTO sectionF (report_id, supervisor_id, comment, talk_option,content_status) VALUES
(2, 10001, "I have concerns about my supervisor's communication skills", 'a','Submitted'),
(3, 10002, "My technical staff are not responsive to my requests for support", 'b','Submitted'),
(4, 10003, "I am worried that identifying concerns about administrative staff may affect my employment", 'b','Submitted'),
(5, 10004, "I am concerned about the way my supervisor speaks to me in meetings", 'a','Submitted'),
(8, 10032, "I am concered about administrative staff may affect my employment", 'b','Submitted'),
(9, 10005, "I am worried about the way my supervisor speaks to me in meetings", 'a','Submitted'),
(10, 10004, "I am concerned about the way my supervisor speaks to me in meetings", 'a','Submitted'),
(1, 10002, "I am concerned about the way my supervisor speaks to me in meetings", 'a','Submitted');
