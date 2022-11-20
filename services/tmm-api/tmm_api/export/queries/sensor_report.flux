import "date"

// Start x days ago at start of day
start = date.sub(d: 6d, from: today())
stop = date.add(d: 1d, to: today())

// Daily average by sensor, still windowed
daily_average_by_sensor = from(bucket: _bucket)
  |> range(start: start, stop: stop)
  |> filter(fn: (r) => (r["_measurement"] == "moisture" and r["_field"] == "percent"))
  |> drop(columns: ["device_brand", "device_model", "_field"])
  |> window(every: 1d, createEmpty: false)
  |> timeWeightedAvg(unit: 1d)
  |> duplicate(column: "_start", as: "_time")
  
// Result for the selected sensor
daily_average_by_sensor
  |> filter(fn: (r) => r["device"] == _device)
  |> drop(columns: ["device"])
  |> window(every: inf)
  |> drop(columns: ["_start", "_stop"])
  |> yield(name: "sensor")

// Result for all sensors 
daily_average_by_sensor
  |> drop(columns: ["device"])
  |> mean()
  |> duplicate(column: "_start", as: "_time")
  |> drop(columns: ["_start", "_stop"])
  |> yield(name: "peers")