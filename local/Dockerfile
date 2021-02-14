FROM python:3.7

WORKDIR /app

RUN pip install boto3

COPY setup_local.py /app/setup_local.py

ENTRYPOINT ["python", "setup_local.py"]