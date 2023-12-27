# PKUmoocServer (Django)

This will help you get started developing with Django.

## Environment Setup
```sh
conda create -n pkumooc python=3.11
conda activate pkumooc
pip install -r requirements.txt
```

## Run the PKUmoocServer
```sh
python manage.py runserver
```

# APIs:
### 用户部分: (密码统一为`project123`)

`/api/register/`: 用于注册, 只允许POST, 接口如下:
```json
{
  "id": "12345678",
  "password": "********",
  "confirmpassword": "********",
  "email": "123@qq.com",
  "phone": "12312341234",
  "name": "张三",
  "sex": "Male"/"Female",
  "dept": "计算机学院",
  "identity": "student"/"teacher",
  "grade": 2023,
}
```
现做了一点修改, 允许了GET操作, 可以在登陆后利用得到的token对`/api/register/`执行GET,
可以得到:
```json
{
  "identity": "student" / "teacher" / "other"
}
```
并得到状态码200. 若未登录就执行GET操作, 会得到
```json
{
  "identity": "login required"
}
```
并得到代表未授权错误的状态码 401. 


另外又把`/api/token/`改了一点, POST成功后返回的信息为
```json
{
  "refresh": "...",
  "access": "...",
  "is_student": "true",
  "is_teacher": "false",
}
```



`/api/token/`: 用于登陆, 只允许POST, 接口如下: (username就是学号或admin)
```json
{
  "username": 12345678,
  "password": "********",
}
```
注意: 这里用了jwt验证, 参考[用户登陆](https://github.com/stacklens/django-vue-tutorial/blob/master/md/250-%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95.md),
不过为了简单, token过期设置为一天, 因此可以不用管token过期刷新的问题


`/admin/`: 管理员后台, 不提供接口, 可查看数据库的情况


## 课程部分
### Course:
`/api/course/`: 可以GET获取课程列表: 
(学生只能看到已选课程, 教师只能看到自己教授的课程).
以及用户必须先登陆才能查看. 
```json
[
  {
    "id": "2000010001",
    "title": "数据库概论",
    "year": 2023,
    "session": "Fall",
    "url": "http://127.0.0.1:8000/api/course/2000010001/",
    "teachers": [
        "张雪山"
    ],
    "students": [
        "张三"
    ]
  }
  ,
  {
    ...
  }
  ...
]
```
对于老师, 有创建课程的权限(POST)
```json
{
  "id": "12345678",
  "title": "数据库概论",
  "year": 2023,
  "session": "Spring" / "Summer" / "Fall" / "Winter",
}
```
另外课程的创建者会默认成为该课程的老师

下面是另一个接口 `/api/course/<str:pk>/`, 例如`/api/course/12345678`, 
允许三种操作, 分别是GET, PUT, DELETE. 只有选课学生和授课老师能GET,
只有授课老师能执行PUT和DELETE. 如果执行GET, 能得到如下内容
```json
{
    "id": "2000010001",
    "title": "数据库概论",
    "year": 2023,
    "session": "Fall",
    "teachers": [
        "张雪山"
    ],
    "students": [
        "张三"
    ]
}
```
后续可根据需要增加新的具体内容

然后没有做PATCH, 但对PUT操作做了一些改进, 
如果不提供teachers或students则不会更改原来的teachers, students. 
若要更改teachers, students, 请传入一个装有学号或工号的列表. 以下是一个PUT例子,
它将老师改成12345678, 不改变学生. (注意, 谨慎操作, 如果自己仍然需要授课,
请修改teachers时务必包含自己, 建议前端加上一次确认防止误触). 
原则上除了初始增加老师和学生外不要PUT. 
另外teachers如果为空, 会返回错误, 且修改无效.
```json
{
  "teachers": [
    "12345678",
  ],
  "session": "Fall",
  "year": 2022,
  "title": "数据库概论"
}
```

### Course: Material
嵌套在`/api/course/<str:pk>/`下, 包括`/api/course/<str:pk1>/material/` 和 `/api/course/<str:pk1>/material/<int:pk>/`两个接口.
前者支持POST, GET方法, 后者支持PUT, GET, DELETE方法. 做了基本的权限控制但仍需改进.

### Course: Material: Picture
嵌套在`/api/course/<str:pk1>/material/<int:pk>/`下, 类似于前者. 另外额外提供了一个下载接口, 可以通过GET方法下载图片.
实际上可以尝试用它传视频, 但可能无法正常播放, 后续如果需要会另外写一个视频接口

