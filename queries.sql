-- to test in terminal:
-- `
-- sqlite3 db.sqlite3
-- .mode box
-- `

------------------------------------------------------------------------
--找出 2023 年9 月1 日之后在讨论区发帖次数前十的用户，按照发帖次数进行降序排序；若次数相同，则按照学号/工号升序排序；

SELECT u.username, COUNT(cp.id) as post_count
FROM user_info_user u
JOIN course_post cp ON u.id = cp.author_id
WHERE cp.created_at > '2023-09-01'
GROUP BY u.id
ORDER BY post_count DESC, u.username
LIMIT 10;
/

------------------------------------------------------------------------
--查找张老师所讲授的课程中，每位学生的作业逾期未交次数，包括学生的姓名、学号和该学生的作业逾期未交次数，按照逾期次数从大到小排序

-- find who was the homework assigned to by 张老师 
CREATE TEMPORARY TABLE homework_Zhang_assigned_to AS
SELECT hw.id, ccs.student_id
from course_homework hw
JOIN user_info_teacher u_t on  hw.teacher_id = u_t.user_id
JOIN course_course_students ccs on ccs.course_id = hw.course_id
where name == '张老师'
/

-- select students that have submitted the homework
CREATE TEMPORARY TABLE students_who_submitted AS
SELECT student_id, homework_id
FROM course_submission cs
WHERE homework_id IN 
(SELECT DISTINCT id FROM homework_Zhang_assigned_to)
/

-- (First table - Second table)
SELECT s.name, u.username, FirstMinusSecond.num_unsubmitted_hw
FROM user_info_student s
JOIN user_info_user u on s.user_id = u.id
Join (SELECT student_id, count(id) as num_unsubmitted_hw
        FROM homework_Zhang_assigned_to HZAT
        WHERE NOT EXISTS (SELECT student_id from students_who_submitted SWS
            where HZAT.student_id = SWS.student_id and HZAT.id = SWS.homework_id)
        GROUP BY student_id 
        ORDER BY num_unsubmitted_hw DESC) FirstMinusSecond 
            on s.user_id = FirstMinusSecond.student_id
/

------------------------------------------------------------------------
-- 查找“王X 明”（姓“王”；名字的第二个字为“明”，第一个字不限；名字可以有
-- 三个及以上的字）学生在所有课程中所有需要提交但未提交的作业，按照作业的截止
-- 时间从早到晚排序。

-- homework assigned to “王X 明”
CREATE TEMPORARY TABLE HisHomework AS
select id as hw_id, ch.course_id
from course_homework ch
where ch.course_id in (select course_id 
                        from course_course_students ccs
                        where student_id == (select s.user_id
                                            FROM user_info_student s
                                            WHERE s.name like '王_明')) 

CREATE TEMPORARY TABLE HisIncompleteHW AS
SELECT hw_id
from HisHomework 
WHERE hw_id not in (SELECT homework_id
                from course_submission
                WHERE student_id == (select s.user_id
                                    FROM user_info_student s
                                    WHERE s.name like '王_明')) 
                    
                    -- normal for the counts to not add up since 2nd part is not unique

select hw_id, ch.submit_end_time
from HisIncompleteHW iHW
JOIN course_homework ch on ch.id = iHW.hw_id
ORDER BY ch.submit_end_time

------------------------------------------------------------------------
-- 查找每门课程的学习进度（即已学习课程材料的数量）低于平均值的学生的学号及姓名，
-- 按照已学习材料数量从小到大排序。

CREATE TEMPORARY TABLE StudyProgressAllStudentsEnrolled AS
select ccs.course_id, ccs.student_id, count(ReadMaterialStudents.material_id) as materials_read
from course_course_students ccs
LEFT JOIN (select cm.id as material_id, cm.course_id, cms.student_id
            from course_material_students cms
            join course_material cm on cm.id = cms.material_id) ReadMaterialStudents
        ON (ccs.student_id = ReadMaterialStudents.student_id
                and ccs.course_id = ReadMaterialStudents.course_id)
GROUP BY ccs.student_id, ccs.course_id
/

CREATE TEMPORARY TABLE Avg_progress AS
select course_id, AVG(pg.materials_read) as avg_progress
from StudyProgressAllStudentsEnrolled pg
GROUP BY course_id
/

select belowAvgStudents.course_id, s.name, u.username
from user_info_student s
JOIN user_info_user u on s.user_id = u.id
JOIN (select pg.student_id, pg.materials_read, ap.course_id
        from StudyProgressAllStudentsEnrolled pg 
        JOIN Avg_progress ap on ap.course_id = pg.course_id
        where pg.materials_read < ap.avg_progress) belowAvgStudents
    on s.user_id = belowAvgStudents.student_id
/

------------------------------------------------------------------------
-- 查找计算机系学生选修的所有课程，以及在每门课程中所有作业的平均分。

-- courses that computer sci students take + relevant hw id
SELECT csStu_hw.course_id, csStu_hw.hw_id, Avg(cs.score)  
FROM (SELECT s.user_id, ccs.course_id, ch.id as hw_id
        FROM user_info_student s
        JOIN course_course_students ccs ON ccs.student_id = s.user_id
        JOIN course_homework ch ON ch.course_id = ccs.course_id
        WHERE s.dept == '计算机') csStu_hw
JOIN course_submission cs on cs.homework_id = csStu_hw.hw_id
WHERE cs.score != -1 
GROUP BY csStu_hw.course_id 


------------------------------------------------------------------------
-- 查找课程总活跃度最高的（课程活跃度即学生在该课程讨论区发帖的总数）教师姓名
-- 和工号，并列出其开设的每门课程的活跃度。

CREATE TEMPORARY TABLE activity_levels AS
select cfs.course_id, count(section_id) as activity_level
from course_post cp
join course_forumsection cfs on cfs.id = cp.section_id
WHERE cp.author_id in 
    (select user_id from user_info_student) --author is student
GROUP BY section_id
ORDER BY activity_level desc
/

CREATE TEMPORARY TABLE teachers_w_HAL AS
select DISTINCT(cct.teacher_id)
from course_course_teachers cct
join (select course_id, al1.activity_level
        from activity_levels al1
        where (select al1.activity_level = max(al2.activity_level)
                from activity_levels al2)) CoursesHighestActivityLevel
                -- possible to have more than one course w highest activity levels
        on cct.course_id = CoursesHighestActivityLevel.course_id
/

select coursesTopCherTeach.teacher_id , al.course_id,al.activity_level
from (select course_id, cct.teacher_id
        from course_course_teachers cct
            where cct.teacher_id in 
        (select teacher_id from teachers_w_HAL)) coursesTopCherTeach
JOIN activity_levels al on al.course_id=coursesTopCherTeach.course_id
/

------------------------------------------------------------------------
-- 查找智能学院教师的所有合作者（即在同一门课程中任教的教师），包括教师工号、
-- 姓名、合作次数，按照合作次数排序。

-- cleaned collaborators version (tuple pair version)
CREATE TEMPORARY TABLE collabZhiNengTeachers AS
SELECT cct1.teacher_id as t1_id, cct2.teacher_id as t2_id, count(*) as collab_count
FROM course_course_teachers cct1
JOIN course_course_teachers cct2 on 
    (cct1.course_id = cct2.course_id and cct1.teacher_id < cct2.teacher_id)
    -- list of all collaborators, does not include themselves
WHERE cct1.teacher_id in (SELECT t.user_id 
                            from user_info_teacher t
                            WHERE dept == '智能') -- first teacher from this dept
GROUP BY cct1.teacher_id, cct2.teacher_id
ORDER BY collab_count DESC
/

-- for each collaborator, sum all their collab counts, rank
SELECT t2_id, t.name, u.username, sum(collab_count) as all_collabs
from collabZhiNengTeachers
JOIN user_info_teacher t on t2_id=t.user_id
JOIN user_info_user u on u.id = t.user_id
GROUP BY t2_id
ORDER BY all_collabs DESC



------------------------------------------------------------------------
-- drafts and testing



-- SELECT s.user_id
-- FROM user_info_student s
-- WHERE s.name like '王_明' 


-- CREATE TEMPORARY TABLE teachers_w_HAL_1 AS
-- select DISTINCT(cct.teacher_id)
-- from course_course_teachers cct
-- join (select course_id, al1.activity_level
--         from activity_levels al1
--         where (select al1.activity_level = max(al2.activity_level)
--                 from activity_levels al2)) CoursesHighestActivityLevel
--                 -- possible to have more than one course w highest activity levels
--         on cct.course_id = CoursesHighestActivityLevel.course_id
-- ORDER BY teacher_id
-- LIMIT 1
-- / -- use this to test the last part; change teachers_w_HAL to teachers_w_HAL_1


-- -- smaller course_course_teachers
-- CREATE TEMPORARY TABLE Smaller_cct AS
-- select cct.course_id, cct.teacher_id
-- from course_course_teachers cct 
-- where cct.teacher_id == 266 or cct.teacher_id == 264 or cct.teacher_id == 267
-- /