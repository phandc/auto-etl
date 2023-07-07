FROM python:3.8-slim

ENV APP_PATH opt/api-management
RUN mkdir -p ${APP_PATH}
WORKDIR $APP_PATH

COPY requirements.txt ./
RUN pip install --no-cache-dir -U -r requirements.txt 
COPY . .

CMD python -u main.py