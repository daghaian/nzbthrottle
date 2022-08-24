FROM python:3.6-alpine3.7
#Copy all project files
COPY . /nzbthrottle

#Set current directory
WORKDIR /nzbthrottle

RUN \
  echo "** BRANCH: ${BRANCH} COMMIT: ${COMMIT} **" && \
  echo "** Upgrade all packages **" && \
  apk add -y gcc libffi-dev musl-dev linux-headers && \
  apk --no-cache -U upgrade && \
  echo "** Install PIP dependencies **" && \
  pip install --no-cache-dir --upgrade pip setuptools && \
  pip install --no-cache-dir --upgrade -r /nzbthrottle/requirements.txt

ENTRYPOINT [ "python", "./throttle.py" ]
