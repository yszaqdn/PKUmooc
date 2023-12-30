'''
To run, 
`python manage.py shell < create_static_data.py`

Instructions:
老师: (5) 张老师 + 智能
学生: (20) 王X 明 + 计算机
课程: (10)
课程材料: (3)

位学生至少要有3次作业提交
至少一半的作业已经由教师打分

需要有的查询：
讨论区发帖次数前十的用户
有些学生作业逾期未交
'''

from user_info.models import User,Student,Teacher
from course.models import Course, Material, Picture, Homework, Problem, Choice, Submission, ForumSection, Post
import random
from django.utils import timezone

random.seed(111)

#=== 老师 (5) ===

dept_list = ["计算机","化学","生物","数学","智能"]
name_list = [
    "李从阳", "李绮琴", "李欣跃", "李天宇", "李兴为",
    "李罗", "李明明", "李语柳", "李冰安", "李纬",
    "王玛丽", "王奇略", "王辰", "王煜", "王莺语",
    "王展", "王淳美", "王紫琼", "王艾", "王藉",
    "王雅青", "陈子默", "陈水蓝", "陈智刚", "陈诗",
    "陈谨", "陈笑笑", "陈莎", "陈诗珊", "陈曼容",
    "陈天禄", "陈思美", "张萦怀", "张笑槐", "张又夏",
    "张书文", "张思懿", "张礼骞", "张迎南", "张访天",
    "张骞魁", "张爰爰", "张自珍", "杨斯斯", "杨以彤",
    "杨怀蕾", "杨千易", "杨胤雅", "杨捷", "杨高原",
    "杨米", "杨向明", "杨问风", "杨冰枫", "黄云水",
    "黄瑾瑜", "黄志", "黄芷蓝", "黄耀", "黄又松",
    "黄皎", "黄坚秉", "黄浩博", "黄恨真", "黄安青",
    "赵夜南", "赵乐和", "赵晶燕", "赵绮晴", "赵琳芳",
    "赵梦容", "赵阳冰", "赵卿", "赵沛容", "赵伟茂",
    "赵经略", "詹芮歆", "费舜钟", "柳玲辰", "潘仪跃",
    "倪苓斯", "彭锟淳", "裴湘曼", "俞奕羚", "贾轶宜",
    "计铎和", "花镇涛", "陈旺意", "骆露韵", "陈莹熹",
    "祁一亮", "柏诗野", "鲁欢薇", "伊竹嘉", "左圣玺",
    "史秋倩", "翟锁冶", "毛韶怡", "唐想里", "房原舟",
    "支一成"
]
sex = ["Female", "Male"]

for i in range(2,7): #control i in single digit range, else add extra line to control username
    number = random.randint(10000000000,19999999999) # phone number
    username = f"880000000{i}" # needs to be 10 digits
    user = User.objects.create_user(username=username, password='project123', email=f'{username}@stu.pku.edu.cn')
    if i == 3:
        Teacher(dept="智能", name =random.choice(name_list), 
            sex = random.choice(sex), phone = str(number), id = username,user=user).save()
    elif i == 2:
        Teacher(dept=random.choice(dept_list), name ="张老师", 
            sex = random.choice(sex), phone = str(number), id = username,user=user).save()
    else:
        Teacher(dept=random.choice(dept_list), name =random.choice(name_list), 
            sex = random.choice(sex), phone = str(number), id = username,user=user).save()

#=== 学生: (20) ===
grades = list(range(20, 25))

for i in range(21,45): #control i in double digit range, else edit username to account
    number = random.randint(10000000000,19999999999) # phone number
    grade = random.choice(grades)
    username = f"{grade}000000{i}" # needs to be 10 digits
    user = User.objects.create_user(username=username, password='project123', email=f'{username}@stu.pku.edu.cn')
    if i == 21:
        Student(dept="计算机", name ="王照明", grade = 2000+grade,
            sex = "Male", phone = str(number), id = username,user=user).save()
    else:
        Student(dept=random.choice(dept_list), name =random.choice(name_list), grade = 2000+grade,
            sex = random.choice(sex), phone = str(number), id = username,user=user).save()
    



#=== 课程: (15) ===
course_list = ["社会发展理论","嵌入式系统","智能硬件应用实验","中国教育及其文化基础","教育实践与教育创新",
               "教育与人工智能","数字媒体创意设计","固体散射谱学简介","凝聚态物理导论","数值天气预报",
               "量子场论","表面物理","原子、分子光谱","天体物理专题","平衡态统计物理",
               "生物物理导论","大气探测原理","	全球环境与气候变迁","天体物理前沿","印度概况",
               "军事理论","核物理与粒子物理专题实验","	孙子兵法导读","毛泽东思想","马克思主义发展史",
               ]


'''course (10) #default everyone is enrolled in all courses for simplicity, # teachers randomly picked
    |__Material (8) # only some students read material - random number easy to control 
    |__Homework (3)
    |__Problems (5) 
    |__Submissions (5) # at least half should be marked - random number easy to control 
                       # every student min 3 submissions - after creatino of data, loop through 
'''


session_list = ["Spring","Summer","Fall","Winter"]

for course_id in range(1,16): #check if there are constraints on course id
    course_year = random.randint(2023, 2024)
    x = Course(id=course_id,title = random.choice(course_list),year=course_year,session=random.choice(session_list))
    x.save()
    #adding many to many fields:
    for student in Student.objects.all():
        x.students.add(student)
    for teacher in random.choices(Teacher.objects.all(),k=random.randint(1,len(Teacher.objects.all()))):
        x.teachers.add(teacher)
    # # dont use this:
    #     # teachers = random.choices(Teacher.objects.all(),k=random.randint(1,len(Teacher.objects.all()))),
    #     # students = Student.objects.all()) # 为简单起见，每学生已注册所有课程。


#=== 资料: (8) ===
material_id = 1
for rel_course in Course.objects.all():
    for material_count in range(1,9):
    # course = random.choice(Course.objects.all())
        x = Material(id=material_id, title = f"主题{material_id}",
                # to add foreign key, reference their primary key??
                course = rel_course,
                teacher = random.choice(rel_course.teachers.all()),
                content = f"这是主题{material_id}的主要内容，考试会考"
                )
        x.save()
        material_id+=1 #not redundant, else only last course is saved...
        # many to many for students
        for student in random.choices(rel_course.students.all(),k=random.randint(1,len(rel_course.students.all()))):
            x.students.add(student)


#=== 作业: (5) ===
end_times = ["2024-01-01 00:00:00.000000+00:00",
             "2023-12-30 14:00:00.000000+00:00"] # 之后可以手动改一下时间

homework_id =1
for course in Course.objects.all():
    for homework_count in range(1,6):
        # homework_id = 2
        end_time = random.choice(end_times)
        Homework(id = homework_id, title=f"主题{homework_id}",
                teacher = random.choice(course.teachers.all()),
                submit_end_time = end_time,
                view_end_time = end_time,
                course = course).save()
        homework_id+=1


# assume default problem score is 100...
        
#=== Submissions ===
"""
学生至少要有3次作业提交
至少一半的作业已经由教师打分"""
checked_more_than_half = [True, True, True, False]

for homework in Homework.objects.all():
    course = homework.course
    students_lst = course.students.all()
    num_students_submitted = random.randint(0,len(students_lst)+1)
    for student in random.choices(students_lst, k=num_students_submitted):
        checked_by_teacher = random.choice(checked_more_than_half)
        Submission(student = student,
            homework = homework,
            is_submitted = True,
            is_checked = checked_by_teacher,
            score = random.randint(0,100) if checked_by_teacher else -1).save()


#=== 板块 （15）Forum Section + 老师的 default post （15）===
#default create forum for each course

for course in Course.objects.all():  
    # default create forum for each course
    forum_section = ForumSection(course=course,name=f"{course.title}板块")
    forum_section.save()
    # also create default post by one tutor
    author_picked = random.choice(course.teachers.all())
    Post(section=forum_section,
         section_id = forum_section.id,
         author=author_picked.user,
         content=f"欢迎大家来到{course.title}，请大家做一下自我介绍"
         ).save()

#=== Post Section ===
for forum_section in ForumSection.objects.all():
    # 大概 1-5 posts
    num_posts = random.randint(1,5)
    for i in range(0,num_posts):
        forum_course = forum_section.course
        author_picked= random.choice(forum_course.students.all())
        Post(section = forum_section,
            section_id = forum_section.id,
            author=author_picked.user,
            content=f"主题{random.randint(1,5)}的作业怎么做第{random.randint(1,20)}题").save()





#=====================================================
# user = User.objects.create_user(username='1', password='project123', email='1@stu.pku.edu.cn')
# Teacher(dept="计算机学院", name ="张一山", sex = "Male", phone = "12312341233", id = "1",user=user).save()

# user = User.objects.create_user(username='2', password='project123', email='2@stu.pku.edu.cn')
# Teacher(dept="化学学院", name ="王琴", sex = "Female", phone = "9924524354", id = "2",user=user).save()

# user = User.objects.create_user(username='3', password='project123', email='3@stu.pku.edu.cn')
# Teacher(dept="生物学院", name ="陈伟", sex = "Male", phone = "8235729875", id = "3",user=user).save()

# user = User.objects.create_user(username='4', password='project123', email='4@stu.pku.edu.cn')
# Teacher(dept="计算机学院", name ="林佳怡", sex = "Female", phone = "6564563562", id = "4",user=user).save()

# user = User.objects.create_user(username='5', password='project123', email='5@stu.pku.edu.cn')
# Teacher(dept="数学学院", name ="韦神", sex = "Male", phone = "876375385", id = "5",user=user).save()


# user = User.objects.create_user(username='100', password='project123', email='100@stu.pku.edu.cn')
# Student(dept="数学学院", name ="张美丽", sex = "Female", phone = "876375385", id = "100",grade=2020,user=user).save()
