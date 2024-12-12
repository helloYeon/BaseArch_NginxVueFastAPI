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
# python
##############################
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install --force-reinstall -r requirements.txt
RUN pip install debugpy

##############################
# alias & cmd
##############################
RUN echo 'alias ll="ls -al"' >> ~/.bashrc
RUN echo 'alias p3="python3"' >> ~/.bashrc

# use uvicorn
CMD ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
