FROM python:3.7.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "app.py"
#ENV FLASK_ENV "development"
#ENV FLASK_DEBUG True


COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0