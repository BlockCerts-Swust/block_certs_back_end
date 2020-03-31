from django.test import TestCase

# Create your tests here.

introduction_url = "http://www.baidu.com" + "intro/" if  "http://www.baidu.com/".endswith('/') else "/intro/"
print(introduction_url)
