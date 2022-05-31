from datetime import datetime
import json
from influxdb_client import InfluxDBClient
import sys
import os

query_type = os.environ.get('EXPORT_QUERY_TYPE') or 'value'
range = os.environ.get('EXPORT_TIMERANGE') or "-1d"
measurement = os.environ.get('EXPORT_MEASUREMENT') or "moisture"
fieldname = os.environ.get('EXPORT_FIELDNAME') or "percent"

range_start = os.environ.get('EXPORT_RANGE_START') or "2022-05-08T00:00:00Z"
range_stop = os.environ.get('EXPORT_RANGE_STOP') or "2022-05-09T00:00:00Z"

bucket = os.environ.get('TMM_BUCKET')

def export_to_json(path_to_config="config.ini"):

    value_query = 'lat = from(bucket: "tmm-bucket") \
    |> range(start: ' + range_start + ' , stop: ' + range_stop + ') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "latitude") \
    \
    long = from(bucket: "tmm-bucket") \
    |> range(start: ' + range_start + ' , stop: ' + range_stop + ') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "longitude") \
    \
    measurement = from(bucket: "tmm-bucket") \
    |> range(start: ' + range_start + ' , stop: ' + range_stop + ') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "' + fieldname +'") \
    \
    alt = from(bucket: "tmm-bucket") \
    |> range(start: ' + range_start + ' , stop: ' + range_stop + ') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "altitude") \
    \
    union(tables: [alt, lat, long, measurement]) \
    |> group(columns: ["device"], mode: "by") \
    |> pivot(rowKey: ["_time"], columnKey: ["_field"],  valueColumn: "_value") \
    |> group()'

    map_query = 'lat = from(bucket: "tmm-bucket") \
    |> range(start: ' + range +') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "latitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    long = from(bucket: "tmm-bucket") \
    |> range(start: ' + range +') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "longitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    measurement = from(bucket: "tmm-bucket") \
    |> range(start: ' + range +') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "' + fieldname +'") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    alt = from(bucket: "tmm-bucket") \
    |> range(start: ' + range +') \
    |> filter(fn: (r) => r["_measurement"] == "' + measurement +'") \
    |> filter(fn: (r) => r["_field"] == "altitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    union(tables: [alt, lat, long, measurement]) \
    |> group(columns: ["device"], mode: "by") \
    |> pivot(rowKey: ["_time"], columnKey: ["_field"],  valueColumn: "_value") \
    |> group()'

    query = map_query

    if(query_type == 'value'):
        if range_start != None and range_stop != None:
            query = value_query
        else:
            print("Missing time range information. Quitting.")
            return

    with InfluxDBClient.from_config_file(config_file=path_to_config) as client:

        query_api = client.query_api()
        result = query_api.query(query=query)

        jsonObj = {}

        if query_type == 'map':
            mapdataArray = []
            for record in result[0].records:
                jsonRecord = {}
                jsonRecord['device'] = record.values['device']
                jsonRecord['altitude'] = record.values['altitude']
                jsonRecord[fieldname] = record.values[fieldname]
                jsonRecord['latitude'] = record.values['latitude']
                jsonRecord['longitude'] = record.values['longitude']
                if (record.values[fieldname] != None):
                    mapdataArray.append(jsonRecord)
            
            jsonObj['records'] = mapdataArray
        
        elif query_type == 'value':
            valuesArray = []
            # TODO: Fix handling / evaluate CSV export
            for sensor in result[0].records:
                for record in sensor.records:
                    jsonRecord = {}
                    jsonRecord['measurement'] = str(record.get_measurement())
                    jsonRecord[record.get_field()] = str(record.get_value())
                    jsonRecord['timestamp'] = str(record.get_time())
                    jsonRecord['deviceId'] = str(record.values['device'])
                    valuesArray.append(jsonRecord)
            jsonObj['values'] = valuesArray

        else:
            print("unknown query type: "  + str(query_type))

        jsonObj['timestamp'] = str(datetime.now())

        retval = json.dumps(jsonObj)
        print(retval)


args = sys.argv[1:]
path = args[0]

export_to_json(path_to_config=path)