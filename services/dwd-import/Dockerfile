FROM osgeo/gdal:ubuntu-small-latest


RUN apt-get update -y; \
    apt-get install -y python3-pip

WORKDIR /usr/src/app

COPY src/requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY src /usr/src/app

#RUN useradd -ms /bin/bash dummy
#USER dummy

ENV INFLUXDB_V2_URL=http://host.docker.internal:8086
ENV INFLUXDB_V2_ORG=teuto
ENV INFLUXDB_V2_TOKEN=ttm-influx-token
ENV INFLUXDB_V2_TIMEOUT=6000
ENV INFLUXDB_V2_CONNECTION_POOL_MAXSIZE=25
ENV INFLUXDB_V2_AUTH_BASIC=false
ENV TMM_BUCKET=tmm-bucket

CMD [ "python3", "dwd_import.py"]