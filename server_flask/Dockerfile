FROM python:3.8.8
WORKDIR /server_code
ENV FLASK_APP=server.py FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
# Wait for Fuseki to be ready with this script
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /scripts
RUN ["chmod", "+x", "/scripts/wait-for-it.sh"]

ENTRYPOINT [ "/scripts/wait-for-it.sh", "-t", "15", "fuseki:3030", "--"]
CMD ["python3", "server.py"]