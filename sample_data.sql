-- Sample data for school service (run after alembic upgrade head)
-- Tables: class, subject, teacher, time_table (order matters for FKs)

-- Classes
INSERT INTO class (id, name) VALUES (1, 'Class 10-A');
INSERT INTO class (id, name) VALUES (2, 'Class 10-B');
INSERT INTO class (id, name) VALUES (3, 'Class 9-A');

-- Subjects
INSERT INTO subject (id, name) VALUES (1, 'Mathematics');
INSERT INTO subject (id, name) VALUES (2, 'Physics');
INSERT INTO subject (id, name) VALUES (3, 'English');
INSERT INTO subject (id, name) VALUES (4, 'Chemistry');

-- Teachers
INSERT INTO teacher (id, first_name, last_name, user_name) VALUES (1, 'Rajesh', 'Kumar', 'r.kumar');
INSERT INTO teacher (id, first_name, last_name, user_name) VALUES (2, 'Priya', 'Sharma', 'p.sharma');
INSERT INTO teacher (id, first_name, last_name, user_name) VALUES (3, 'Amit', 'Singh', 'a.singh');
INSERT INTO teacher (id, first_name, last_name, user_name) VALUES (4, 'Sneha', 'Patel', 's.patel');

-- Subject–teacher mapping (which teachers can teach which subjects)
INSERT INTO subject_teachers (subject_id, teacher_id) VALUES (1, 1);   -- Maths: Rajesh
INSERT INTO subject_teachers (subject_id, teacher_id) VALUES (2, 2);   -- Physics: Priya
INSERT INTO subject_teachers (subject_id, teacher_id) VALUES (3, 3);   -- English: Amit
INSERT INTO subject_teachers (subject_id, teacher_id) VALUES (4, 4);   -- Chemistry: Sneha
INSERT INTO subject_teachers (subject_id, teacher_id) VALUES (1, 2);   -- Maths: Priya (also)
INSERT INTO subject_teachers (subject_id, teacher_id) VALUES (3, 4);   -- English: Sneha (also)

-- Timetable (day: 1=Mon .. 5=Fri, period: 1..8)
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (1, 1, 1, 1, 1, 1);   -- Mon P1: 10-A, Maths, R.Kumar
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (2, 1, 2, 1, 2, 2);   -- Mon P2: 10-A, Physics, P.Sharma
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (3, 1, 3, 1, 3, 3);   -- Mon P3: 10-A, English, A.Singh
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (4, 2, 1, 1, 1, 1);   -- Tue P1: 10-A, Maths
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (5, 2, 2, 2, 2, 2);   -- Tue P2: 10-B, Physics
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (6, 3, 1, 3, 4, 4);   -- Wed P1: 9-A, Chemistry, S.Patel
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (7, 4, 1, 1, 3, 3);   -- Thu P1: 10-A, English
INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (8, 5, 2, 2, 1, 1);

INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (9, 1, 1, 1, 2, 3);

INSERT INTO time_table (id, day, period, class_id, teacher_id, subject_id) VALUES (10, 1, 1, 1, 3, 4);
