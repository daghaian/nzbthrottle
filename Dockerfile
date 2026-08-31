FROM python:3.12-alpine
#Copy all project files
COPY . /nzbthrottle

#Set current directory
WORKDIR /nzbthrottle

RUN \
  echo "** Upgrade all packages **" && \
  apk --no-cache -U upgrade && \
  echo "** Install PIP dependencies **" && \
  pip install --no-cache-dir --upgrade pip setuptools && \
  pip install --no-cache-dir --upgrade -r /nzbthrottle/requirements.txt

ENTRYPOINT [ "python", "./throttle.py" ]
