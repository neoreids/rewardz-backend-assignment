FROM python:3.9-alpine

RUN mkdir /code
WORKDIR /code

RUN apk update
RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["gunicorn", "--workers=3", "rewardz.wsgi:application", "-b", "0.0.0.0:8080"]
