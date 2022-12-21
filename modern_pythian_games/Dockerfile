FROM ubuntu:latest

RUN apt update && apt upgrade -y

RUN apt install -y -q build-essential python3-pip python3-dev
RUN pip3 install -U pip setuptools wheel
RUN pip3 install gunicorn uvloop httptools

COPY requirements.txt /app/requirements.txt
COPY setup.py /app/setup.py

WORKDIR /app

RUN pip3 install -e .
RUN pip3 install -r /app/requirements.txt


COPY service/ /app/service

# ENTRYPOINT /usr/local/bin/gunicorn \
  # -b 0.0.0.0:8000 \
  # -w 4 \
  # -k uvicorn.workers.UvicornWorker main:app \
  # --chdir /app
ENTRYPOINT [ "/usr/local/bin/gunicorn", "-b", "0.0.0.0:8000", "-w", "5", "-k", "uvicorn.workers.UvicornWorker", "service.main:app", "--chdir", "/app" ]  
# CMD ["uvicorn",  "main:app", "--host=0.0.0.0", "--port", "8000"]