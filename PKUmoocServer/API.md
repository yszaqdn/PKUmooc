**注意**: 以下所有操作建议使用postman测试
# API 行为

### 1. /api/token/ 获取token
* 允许的操作: PUSH
* 请求样例
  ```json
  {
    "username": 2000011111,
    "password": "project123",
  }
  ```
* 返回结果(成功): 状态码 200 OK
  ```json
  {
    "refresh": "eyJ...",
    "access": "eyJ...",
    "is_student": true,
    "is_teacher": false,
  }
  ```
* 返回结果(失败): 状态码 401 Unauthorized
  ```json
  {
    "detail": "No active account found with the given credentials"
  }
  ```

### 2. /api/register/ 注册
* 允许的操作: PUSH
* 请求样例:
  ```json
  {
    "id": 2000010001,
    "password": "project123",
    "email": "orange@qq.com",
    "confirmpassword": "project123",
    "phone": 12312341234,
    "dept": "计算机学院",
    "name": "张三",
    "sex": "Male",
    "identity": "student",
    "grade": 2021,
  }
  ```
* 返回结果(成功): 状态码 200 OK
* 返回结果(失败): 状态码 400 Bad Request
  * 例如创建的用户已经存在:
    ```json
    {
      "id": [
        "A user with that id already exists."
      ]
    }
    ```

### 3. /api/course/ 课程列表
* 需要登陆
* 允许的操作: PUSH, GET
* 权限:
  * 学生只能看到(GET)自己学习的课程, 其他课程不可见, 如果没有会返回空列表
  * 教师只能看到(GET)自己讲授的课程, 其他课程不可见, 如果没有会返回空列表
  * 只有教师能创建(POST)课程, 新创建的课程包含创建者作为唯一的老师, 没有任何学生
  * 既不是老师也不是学生的用户和未登录用户无法访问课程信息
* 请求样例1: 选课学生 GET: 状态码: 200 OK
  ```json
  [
    {
      "id": "1234",
      "title": "数据库概论",
      "year": 2023,
      "session": "Fall",
      "url": "http://127.0.0.1:8000/api/course/1234/",
      "teachers": [
        "张雪山",
      ],
      "students": [
        "w",
        "www",
        "2000011111",
        "2000011111",
        "w",
        "张三",
      ]
    }
  ]
  ```
* 请求样例2: 非选课学生 GET: 状态码: 200 OK
    ```json
    []
    ```

* 请求样例3: 学生 POST: 状态码: 403 Forbidden
  ```json
  {
    "detail": "You do not have permission to perform this action."
  }
  ```

* 请求样例4: 老师
  * 请求 POST:
    ```json
    {
      "id": 12345,
      "title": "数据库概论2",
      "year": 2022
    }
    ```
  * 返回: 状态码 200 OK
    ```json
    {
      "id": "12345",
      "title": "数据库概论2",
      "year": 2022,
      "session": "Fall",
      "url": "http://127.0.0.1:8000/api/course/12345/",
      "teachers": [
        "张雪山"
      ],
      "students": []
    }
    ```

* 请求样例5: 还是老师
  * 请求 POST: 将上面的重复一遍:
  * 返回: 状态码 400 Bad Request
    ```json
    {
      "id": [
        "course with this 课程编号 already exists."
      ]
    }
    ```
* 请求样例6: 未登录用户:
  * 请求 GET: 状态码 401 Unauthorized
  ```json
    {
      "detail":"Authentication credentials were not provided."
    }
  ```

### 4. /api/course/\<str:pk\>/ 课程详细信息
* 需要登陆
* 允许的操作 GET, PUT, DELETE
* 权限:
  * 学生只能查看(GET)所选课程的详细信息
  * 学生无法执行PUT, DELETE或者对未选课程执行GET
  * 老师可以对讲授的课程执行 GET, PUT, DELETE操作
* 请求样例1: 学生 GET 所选课程: 数据库概论(1234), 状态码 200 OK
  ```json
  {
    "id": "1234",
    "title": "数据库概论",
    "year": 2023,
    "session": "Fall",
    "teachers": [
      "张雪山"
    ],
    "students": [
      "w",
      "www",
      "2000011111",
      "2000011111",
      "w",
      "李代波",
      "张三"
    ]
  }
  ```
* 请求样例2: 学生 GET 非所选课程: 数据库概论2(12345), 状态码 403 Forbidden
  ```json
  {
    "detail": "You have no right to access this course"
  }
  ```
* 请求样例3: 老师 GET 所教授课程, 同样例1
* 请求样例4: 老师 GET 未教授课程, 同样例2
* 请求样例5: 学生 PUT, DELETE: 状态码 403 Forbidden:
  ```json
  {
    "detail": "You do not have permission to perform this action."
  }
  ```
* 请求样例6: 老师 PUT 未教授课程, 同样例2
* 请求样例7: 老师 PUT 教授课程
  ```json
  {
    "title": "数据库概论2",
    "year": 2022,
    "session": "Spring",
    "students": [
      2000010001,
      2000011111,
    ]
    teachers: [
      1001001001,
    ]
  }
  ```
  返回的结果: 状态码 200 OK
  ```json
  {
    "id": "12345",
    "title": "数据库概论2",
    "year": 2022,
    "session": "Spring",
    "teachers": [
      "张雪山"
    ],
    "students": [
      "w",
      "张三"
    ]
  }
  ```
* 请求样例8: 老师delete 教授课程
  成功则什么也不返回, 状态码为 204 no content

### 5. /api/course/\<str:pk1\>/homework/ 作业列表
* 权限: 选课的学生和老师, 老师能修改, 学生只能查看
* 允许的操作: GET, POST
* GET 效果: 学生和老师都一样:
  ```json
  [
    {
      "id": 1,
      "title": "作业1",
      "course": "好喜欢数据库概论",
      "teacher": "张雪山",
      "view_begin_time": "2023-12-28T18:15:07.990461+08:00",
      "view_end_time": "2024-01-20T00:00:00+08:00",
      "submit_begin_time": "2023-12-28T18:15:07.990461+08:00",
      "submit_end_time": "2024-01-19T00:00:00+08:00",
      "url": "http://127.0.0.1:8000/api/course/10000/homework/1/"
    }
  ]
  ```

* POST 只允许老师, 最小输入为:
  ```json
  {
    "title": "人工智能",
    "view_end_time": "2024-01-20",
    "submit_end_time": "2024-01-06"
  }
  ```
  返回值: 状态码200
  ```json
  {
    "id": 2,
    "title": "作业2",
    "course": "好喜欢数据库概论",
    "teacher": "张雪山",
    "view_begin_time": "2023-12-29T00:04:38.558722+08:00",
    "view_end_time": "2024-01-20T00:00:00+08:00",
    "submit_begin_time": "2023-12-29T00:04:38.558722+08:00",
    "submit_end_time": "2024-01-06T00:00:00+08:00"
  }
  ```
  完整输入可以包含 view_begin_time 和 submit_begin_time,
  如果不包含就默认创建作业的时间. 另外后端没有做约束(好像没找到好办法),
  所以可能结束时间早于开始时间, 可能的话看前端能不能做一点约束.
  不过好在可以put方法更改.

* 失败的操作可以自行试验, 我对我能想到的操作做了异常处理

### 6. /api/course/\<str:pk1\>/homework/\<int:pk\>/ 作业详细信息
* 权限: 老师能修改, 学生只能查看
* 允许的操作 GET, PUT, DELETE
* GET 操作没什么不同, 就是少了url
  ```json
  {
    "id": 3,
    "title": "作业3",
    "course": "好喜欢数据库概论",
    "teacher": "张雪山",
    "view_begin_time": "2023-12-29T00:20:29.130211+08:00",
    "view_end_time": "2024-01-20T00:00:00+08:00",
    "submit_begin_time": "2023-12-29T00:20:29.130211+08:00",
    "submit_end_time": "2024-01-06T00:00:00+08:00"
  }
  ```

* PUT 和post没区别
* DELETE 直接DELETE

### 7. /api/course/\<str:pk1\>/homework/\<int:pk\>/problem/ 题目列表
* 学生只能查看, 老师可以查看和修改
* 允许的操作 GET, POST,
* 老师 GET 操作:
  ```json
  [
      {
          "id": 1,
          "description": "今天中午吃什么",
          "points": 5,
          "expected_answer": "A",
          "teacher": "张雪山",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "choiceA": "勺园黄焖鸡",
          "choiceB": "家三鸡腿饭",
          "choiceC": "学一牛肉面",
          "choiceD": "原神，启动！",
          "type": "single",
          "url": "http://127.0.0.1:8000/api/course/10000/homework/1/problem/1/",
          "num": 1
      },
      {
          "id": 2,
          "description": "数据库概论是不是绝世好课",
          "points": 5,
          "expected_answer": "那必须的，别问我为什么流泪，问就是高兴",
          "teacher": "张雪山",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "type": "text",
          "url": "http://127.0.0.1:8000/api/course/10000/homework/1/problem/2/",
          "num": 2
      },
      {
          "id": 5,
          "description": "以下和数据库有关的是",
          "points": 4,
          "expected_answer": "ABC",
          "teacher": "张雪山",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "choiceA": "mySQL",
          "choiceB": "Hadoop",
          "choiceC": "Django",
          "choiceD": "原神，启动！",
          "type": "multiple",
          "url": "http://127.0.0.1:8000/api/course/10000/homework/1/problem/5/",
          "num": 3
      }
  ]
  ```
  注意: 学生看不到expected_answer. 

* 通过 POST 可以增加新的题目, POST一个最小的例子:
  ```json
  {
      "description": "描述你现在的精神状态",
      "points": 3,
      "expected_answer": "阴暗地爬行",
      "type": "text"
  }
  ```
  懒得写返回结果了, 状态码为200就是成功了.

* "type" 有 "single", "multiple", "text" 三种, 前两种还需要提供选项("choiceA"到"choiceD")


### 8. /api/course/\<str:pk1\>/homework/\<int:pk2\>/problem/\<int:pk\>/ 题目
提供GET, DELETE操作, 因为PUT还没写(苦涩).

GET同上, 只是少了url. delete可以删除. 老师可以删除, 学生只能GET

### 9. /api/course/\<str:pk1\>/homework/\<int:pk2\>/submission/ 作业记录
* 老师只能查看已提交的作业, 学生可以查看和创建自己的所有作业. 无法查看别人的作业
* 学生GET操作如下:
  ```json
  [
      {
          "id": 2,
          "student": "王二",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "is_submitted": false,
          "is_checked": false,
          "score": -1,
          "remark": "",
          "url": "http://127.0.0.1:8000/api/course/10000/homework/1/submission/2/"
      }
  ]
  ```
  可能有多次. 老师看不到这条, 因为未提交.

* POST操作不需要任何输入, 只是创建一条空的提交记录

### 10. /api/course/\<str:pk1\>/homework/\<int:pk2\>/submission/\<int:pk\>/ 具体提交记录
* 提供GET, PUT和DELETE方法. 
* GET获取带有题目和回答的完整记录
  ```json
  [
      {
          "id": 1,
          "description": "今天中午吃什么",
          "points": 5,
          "teacher": "张雪山",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "choiceA": "勺园黄焖鸡",
          "choiceB": "家三鸡腿饭",
          "choiceC": "学一牛肉面",
          "choiceD": "原神，启动！",
          "type": "single",
          "num": 1,
          "my_answer": "Not done!"
      },
      {
          "id": 2,
          "description": "数据库概论是不是绝世好课",
          "points": 5,
          "teacher": "张雪山",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "type": "text",
          "num": 2,
          "my_answer": "Not done!"
      },
      {
          "id": 5,
          "description": "以下和数据库有关的是",
          "points": 4,
          "teacher": "张雪山",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "choiceA": "mySQL",
          "choiceB": "Hadoop",
          "choiceC": "Django",
          "choiceD": "原神，启动！",
          "type": "multiple",
          "num": 3,
          "my_answer": "Not done!"
      },
      {
          "id": 6,
          "description": "描述你现在的精神状态",
          "points": 3,
          "teacher": "张雪山",
          "homework": "好喜欢数据库概论 : 看不见的人工智能",
          "type": "text",
          "num": 4,
          "my_answer": "Not done!"
      }
  ]
  ```
  注意题号是num不是id. 这里Not done!表示未回答

  然后PUT方法有4个量, 学生两个, 老师两个. 不要求全给. 
  ```json
  {
    "answers": ["A", "喜欢"],
    "submit": false,
    "score": 10,
    "remark": "玩原神玩的"
  }
  ```
  其中answers是一个列表用来输入答案, 必须按照题号顺序填写, 长度不做要求.
  submit是是否提交, 如果设置为true则提交. 提交必须在规定时间完成. 
  提交前老师看不到作业信息. 提交后学生将无法更改. 老师获得部分更改的权力.
  score和remark学生改不了, 只有老师能改. 老师改动这两个值都会触发 is_checked=True

