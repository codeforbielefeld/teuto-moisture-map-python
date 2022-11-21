import "date"

windowSize = duration(v: _windowSize)

// Start x days ago at start of day
t0 = date.truncate(t: now(), unit: windowSize)
start = date.sub(d: duration(v: int(v: windowSize) * (int(v: _records) - 1)), from: t0)
stop = date.add(d: windowSize, to: t0)

// Daily average by sensor, still windowed
daily_average_by_sensor = from(bucket: _bucket)
  |> range(start: start, stop: stop)
  |> filter(fn: (r) => r._measurement == "moisture" and r._field == "percent")
  |> drop(columns: ["device_brand", "device_model", "_field"])
  |> window(every: windowSize, createEmpty: false)
  |> mean()
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