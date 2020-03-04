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
        
    

## Project
```
----block_certs_back_end
    |----.gitignore
    |----block_certs_back_end
    |    |----asgi.py
    |    |----settings.py
    |    |----urls.py
    |    |----wsgi.py
    |    |----__init__.py
    |----db.sqlite3
    |----manage.py
    |----middleware
    |    |----common.py
    |    |----__init__.py
    |----README.md
    |----requirements.txt
    |----schools
    |    |----admin.py
    |    |----apiviews.py
    |    |----apps.py
    |    |----models.py
    |    |----serializers.py
    |    |----tests.py
    |    |----urls.py
    |    |----views.py
    |    |----__init__.py
    |----students
    |    |----admin.py
    |    |----apiviews.py
    |    |----apps.py
    |    |----auth.py
    |    |----hashers.py
    |    |----models.py
    |    |----serializers.py
    |    |----tests.py
    |    |----urls.py
    |    |----__init__.py
    |----verifier
    |    |----admin.py
    |    |----apps.py
    |    |----models.py
    |    |----tests.py
    |    |----urls.py
    |    |----views.py
    |    |----__init__.py

```

## License

MIT © Jess