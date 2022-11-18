this_week_data = from(bucket: _bucket)
  |> range(start: -7d)
  |> filter(fn: (r) => r["_measurement"] == "moisture")
  |> filter(fn: (r) => r["_field"] == "percent")
  |> drop(columns: ["device_brand", "device_model"])

this_week_data
  |> filter(fn: (r) => r["device"] == _device)
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> drop(columns: ["device"])
  |> yield(name: "sensor")

this_week_data
  |> drop(columns: ["device"])
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> yield(name: "peers")

last_year_data= from(bucket: _bucket)
  |> range(start: -372d, stop: -356d)
  |> filter(fn: (r) => r["_measurement"] == "moisture")
  |> filter(fn: (r) => r["_field"] == "percent")
  |> drop(columns: ["device_brand", "device_model"])

last_year_data
  |> filter(fn: (r) => r["device"] == _device)
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
//|> timeShift(duration: 356d)
  |> drop(columns: ["device"])
  |> yield(name: "sensorPreviousYear")

last_year_data
  |> drop(columns: ["device"])
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
//|> timeShift(duration: 365d)
  |> yield(name: "peersPreviousYear")
