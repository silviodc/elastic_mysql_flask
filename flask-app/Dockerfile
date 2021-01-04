FROM python:3.7-alpine
WORKDIR /code
ENV RABBITMQ_USER=admin
ENV RABBITMQ_PASS=changeme
ENV RABBITMQ_URL=rabbitmq
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
