FROM python:slim
COPY ./requirements.txt .
RUN pip install --upgrade -r requirements.txt
RUN apt update -y && apt install rsync sshpass openssh-client -y
RUN mkdir /.ssh && touch /.ssh/id_rsa && chmod 600 /.ssh/id_rsa

WORKDIR "/app"
COPY . .
CMD ["python", "deploy_autoscaling.py"]
