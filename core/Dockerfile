FROM python:3

# setup mongodb so that we can use mongodump from inside this container
# instructions here: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add - && \
	echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list && \
	apt-get update && \
	apt-get install -y mongodb-org



WORKDIR /usr/src/app

COPY requirements.txt ./
# jupyter is required to convert notebooks into script files
RUN pip install --no-cache-dir -r requirements.txt && pip install jupyter

COPY . .


WORKDIR /usr/src/app


EXPOSE 5000

# CMD python ./launcher.py collection
CMD sh launcher.sh
