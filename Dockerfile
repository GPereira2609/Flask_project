FROM python:3.10-slim-buster
EXPOSE 5000
WORKDIR /usr/src/app
COPY ..
RUN python -m pip install -r requirements.txt
CMD ["python", "./app.py"]