from datetime import datetime
import json
from influxdb_client import InfluxDBClient
import sys
import os

query_type = os.environ.get('EXPORT_QUERY_TYPE') or 'map'
range = os.environ.get('EXPORT_TIMERANGE') or "-1d"
measurement = os.environ.get('EXPORT_MEASUREMENT') or "moisture"
fieldname = os.environ.get('EXPORT_FIELDNAME') or "percent"

range_start = os.environ.get('EXPORT_RANGE_START') or "2022-08-05T00:00:00Z"
range_stop = os.environ.get('EXPORT_RANGE_STOP') or "2022-08-06T00:00:00Z"

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
        
        if query_type == 'map':
            result = query_api.query(query=query)
            
            jsonObj = {}
            
            mapdataArray = []
            for record in result[0].records:
                jsonRecord = {}
                jsonRecord['time'] = str(record.values["_time"])
                jsonRecord['device'] = record.values['device']
                jsonRecord['altitude'] = record.values['altitude']
                jsonRecord[fieldname] = record.values[fieldname]
                jsonRecord['latitude'] = record.values['latitude']
                jsonRecord['longitude'] = record.values['longitude']
                if (record.values[fieldname] != None):
                    mapdataArray.append(jsonRecord)
            
            jsonObj['records'] = mapdataArray
            jsonObj['timestamp'] = str(datetime.now())
            retval = json.dumps(jsonObj)

            with open("output/" + str(range) + ".json", 'w') as file:
                file.write(retval)
        
        elif query_type == 'value':

            result = query_api.query_csv(query=query)

            with open("output/" + str(range_start) + "__" + str(range_stop) + ".csv", 'a') as file:

                for row in result:
                    file.write(str(row)[1:-1])
                    file.write("\r\n")

        else:
            print("unknown query type: "  + str(query_type))

        
args = sys.argv[1:]
path = args[0]

export_to_json(path_to_config=path)