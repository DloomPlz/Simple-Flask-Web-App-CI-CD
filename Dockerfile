# this dockerfile inherit from https://github.com/docker-library/python/blob/38dcdb4320c8668416205e044ee50489c059da18/3.7/stretch/slim/Dockerfile
FROM python:3-slim

# we add a user that will run our app so it's not run by root
RUN groupadd -g 999 flaskou && useradd -r -u 999 -g flaskou flaskou

WORKDIR /home/flaskou

# we copy our app inside the container, the folder will be created
# we chown the folder to the user flaskou
COPY --chown=flaskou:flaskou . ./

# we install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# we switch user to the one we created earlier
USER flaskou

# we run some useful commands like creating the database and creating the first admin
RUN flask reset-db && \
	flask create-admin "root" "root@mail.com" "toor"

# we share this folder with the host
VOLUME /home/flaskou

# finally we run our app
CMD [ "gunicorn", "-b :5000", "wsgi:app" ]

# we expose the port 5000 so the host can access it
EXPOSE 5000