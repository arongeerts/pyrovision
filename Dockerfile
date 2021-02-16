FROM python:3.7

WORKDIR /app

# Install terraform
ENV TF_VERSION=0.14.6
ADD https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip terraform_${TF_VERSION}_linux_amd64.zip
RUN unzip terraform_${TF_VERSION}_linux_amd64.zip
RUN mv terraform /usr/local/bin/
RUN terraform --version

# Install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Set config file
COPY local/config.yaml /app/config.yaml
ENV PYROVISION_CONFIG_FILE /app/config.yaml

# Run app
COPY ./pyrocore /app/pyrocore
COPY ./pyrovision /app/pyrovision
CMD ["uvicorn", "pyrovision.api.api:app", "--host", "0.0.0.0", "--port", "8080"]
