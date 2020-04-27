# Block_certs_back_end
## Contents
- [Install](#Install)
- [Usage](#Usage)
- [Notice](#Notice)
- [Project](#Project)
- [License](#license)

## Install
> pip install -r requirements.txt

generate requirements.txt

> pip freeze > requirements.txt

If it is too slow, you can execute the following command:

> pip install -i https://mirrors.huaweicloud.com/repository/pypi/simple -r requirements.txt

## Usage

Operating environment:

    asgiref==3.2.3
    Django==3.0.3
    djangorestframework==3.11.0
    pytz==2019.3
    sqlparse==0.3.0


Excute command:

> python manage.py runserver

## Notice
        
Response {"code": 1000, "msg": "操作成功", "data": {...}}
Response {"code": 1001, "msg": "操作失败", "data": {...}}

code:
    1000 login/register successful
    1001 login/register failed
    1002 API-HTTP-AUTHORIZATION 请求头无效或为空

## Common commands

python manage.py makemigrations
