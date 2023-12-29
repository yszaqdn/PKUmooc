'''
To run, 
`python manage.py shell < create_static_data.py`

Instructions:
老师: (5) 张老师 + 智能
学生: (20) 王X 明 + 计算机
课程: (10)
课程材料: (3)

位学生至少要有3 次作业提交
至少一半的作业已经由教师打分

需要有的查询：
讨论区发帖次数前十的用户
有些学生作业逾期未交
'''

from user_info.models import User,Student,Teacher
import random

random.seed(111)

#=== 老师 (5) ===

dept_list = ["计算机","化学","生物","数学","智能"]
name = [
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

for i in range(2,7):
    number = random.randint(10000000000,19999999999) 
    user = User.objects.create_user(username=str(i), password='project123', email=f'{i}@stu.pku.edu.cn')
    if i == 1:
        Teacher(dept="智能", name =random.choice(name), 
            sex = random.choice(sex), phone = str(number), id = str(i),user=user).save()
    elif i == 2:
        Teacher(dept=random.choice(dept_list), name ="张雪山", 
            sex = random.choice(sex), phone = str(number), id = str(i),user=user).save()
    else:
        Teacher(dept=random.choice(dept_list), name =random.choice(name), 
            sex = random.choice(sex), phone = str(number), id = str(i),user=user).save()

#=== 学生: (20) ===
grade = list(range(20, 25))

for i in range(21,45):
    number = random.randint(10000000000,19999999999) # phone number
    grade = random.choice(grade)
    username = f"{grade}000000{i}" # needs to be 10 digits
    user = User.objects.create_user(username=username, password='project123', email=f'{username}@stu.pku.edu.cn')
    if i == 1:
        Student(dept="计算机", name ="王照明", grade = 2000+grade,
            sex = "Male", phone = str(number), id = username,user=user).save()
    else:
        Student(dept=random.choice(dept_list), name =random.choice(name), grade = 2000+grade,
            sex = random.choice(sex), phone = str(number), id = username,user=user).save()
    
# user = User.objects.create_user(username='100', password='project123', email='100@stu.pku.edu.cn')
# Student(dept="数学学院", name ="张美丽", sex = "Female", phone = "876375385", id = "100",grade=2020,user=user).save()

#=== 课程: (20) ===
course_list = ["计算机","化学","生物","数学","智能"]

# course (10) #default everyone is enrolled in all courses for simplicity, # teachers randomly picked
# |__Material (8) # only some students read material - random number easy to control 
# |__Homework (3)
#   |__Problems (5) 
#   |__Submissions (5) # at least half should be marked - random number easy to control 
                       # every student min 3 submissions - after creatino of data, loop through 













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
