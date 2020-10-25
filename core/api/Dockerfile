FROM python:3

WORKDIR /usr/src/api

COPY requirements.txt ./
# jupyter is required to convert notebooks into script files
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


WORKDIR /usr/src/api


EXPOSE 5000

# CMD python ./launcher.py collection
# CMD sh launcher.sh
CMD python api/main.py > logs_flask.txt
