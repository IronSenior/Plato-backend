FROM python:3.9.7

COPY . /app
WORKDIR /app
RUN pip install -e .

ENV FLASK_ENV=production
CMD ["plato"]