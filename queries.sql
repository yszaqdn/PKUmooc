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
