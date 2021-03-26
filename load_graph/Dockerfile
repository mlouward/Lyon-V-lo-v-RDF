FROM python:3.8.8
WORKDIR /rdf
RUN pip install rdflib==5.0.0
RUN pip install requests==2.23.0
COPY . .
# Wait for Fuseki to be ready with this script
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /scripts
RUN ["chmod", "+x", "/scripts/wait-for-it.sh"]

ENTRYPOINT [ "/scripts/wait-for-it.sh", "-t", "15", "fuseki:3030", "--"]

CMD ["python3", "jsontordf.py"]