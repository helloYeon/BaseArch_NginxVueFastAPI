FROM python:3.11

##############################
# initialize
##############################
WORKDIR /app

# COPY backend/src/requirements.txt /app/
COPY backend/src /app
COPY backend/src/requirements.txt /app/
ENV PATH=$PATH:/app/site-packages/bin

##############################
# nginx install
##############################


##############################
# apt
##############################
RUN apt update
RUN apt -y upgrade
RUN apt -y install vim apt-utils

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
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/site-packages:/app

RUN pip install --upgrade pip
RUN pip install --force-reinstall -r requirements.txt

##############################
# alias & cmd
##############################
RUN echo 'alias ll="ls -al"' >> ~/.bashrc
RUN echo 'alias p3="python3"' >> ~/.bashrc

# use uvicorn
#CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# use gunicorn

CMD ["/bin/sh", "-c", "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 & nginx -g 'daemon off;'"]
