FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' > /etc/timezone
RUN mkdir /block_certs_back_end
WORKDIR /block_certs_back_end
COPY . /block_certs_back_end/
RUN pip install -r requirements.txt
