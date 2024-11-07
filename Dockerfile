FROM gowthamdocker1999/pythonapp:v1

MAINTAINER gowtham

WORKDIR /voteapp

RUN mkdir /voteapp/templates

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY index.html /voteapp/templates

COPY app_mango.py .

CMD ["python","app_mango.py"]

EXPOSE 80
