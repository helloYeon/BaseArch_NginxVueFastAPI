FROM python:3.11

##############################
# initialize
##############################
WORKDIR /app

COPY backend/src/requirements.txt /app/
ENV PATH=$PATH:/app/site-packages/bin

##############################
# apt
##############################
RUN apt update && apt -y upgrade
RUN apt -y install vim apt-utils wget

##############################
# SQL*Plus for Oracle
##############################
RUN apt install -y libaio1 build-essential
RUN cd /tmp && \
    wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip && \
    wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-sqlplus-linuxx64.zip && \
    unzip -o instantclient-basic-linuxx64.zip && \
    unzip -o instantclient-sqlplus-linuxx64.zip && \
    mkdir -p /opt/oracle/instantclient && \
    mv instantclient_*/* /opt/oracle/instantclient && \
    rm -rf instantclient-basic-linuxx64.zip instantclient-sqlplus-linuxx64.zip

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH
ENV PATH=/opt/oracle/instantclient:$PATH

##############################
# python
##############################
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install --force-reinstall -r requirements.txt
RUN pip install debugpy

RUN apt-get update
RUN apt-get install -y chromium
RUN apt-get install -y chromium-driver

##############################
# alias & cmd
##############################
RUN echo 'alias ll="ls -al"' >> ~/.bashrc
RUN echo 'alias p3="python3"' >> ~/.bashrc

# use uvicorn
CMD ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

# use gunicorn
# CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker" ,"-b", "0.0.0.0:8000"]

##############################
# memo
##############################
# RUN pip install -r requirements.txt
# RUN mkdir -p packages
# RUN pip install -r requirements.txt
# entrypoint.shに実行権限を付与
# RUN chmod 755 entrypoint.sh
# COPY src/be /app/
# # RUN export PATH=$PATH:/usr/local/scala/scala-2.11.7/bin
# RUN echo "333333333333333333333333"
# RUN echo $PATH
# RUN alias ll='ls -al'
# CMD ["tail","-F",""]
