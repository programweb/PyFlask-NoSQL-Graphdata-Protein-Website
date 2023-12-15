FROM python:3.8

COPY requirements.txt /opt/
# Run pip3 install --upgrade pip
RUN pip3 install -r /opt/requirements.txt --verbose

WORKDIR /opt
#COPY . .

ENV FLASK_APP=app
ENV FLASK_DEBUG=1
CMD  ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
