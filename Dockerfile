FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' > /etc/timezone
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
