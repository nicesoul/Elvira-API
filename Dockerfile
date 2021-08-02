FROM python:3.7.11-slim-buster
COPY . /API
WORKDIR /API
RUN pip install -r API/requirements.txt
ENTRYPOINT ["python"]
CMD ["API/elvira_01.py"]
