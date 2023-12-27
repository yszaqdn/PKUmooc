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
