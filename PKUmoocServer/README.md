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

