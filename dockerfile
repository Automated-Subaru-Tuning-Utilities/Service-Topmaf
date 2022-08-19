# syntax=docker/dockerfile:1
FROM python:3.10.6-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#copy source code to workdir
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host=0.0.0.0"]

# to run this container:
# cd Service-Lowmaf/
# docker build -t service-topmaf . 
# docker run -p 8001:8000 --name service-topmaf service-topmaf