import "date"

windowSize = duration(v: _windowSize)

// Start x days ago at start of day
t0 = date.truncate(t: now(), unit: windowSize)
start = date.sub(d: duration(v: int(v: windowSize) * (int(v: _records) - 1)), from: t0)
stop = date.add(d: windowSize, to: t0)

// Daily average by sensor, still windowed
daily_average_by_sensor =
    from(bucket: _bucket)
        |> range(start: start, stop: stop)
        |> filter(fn: (r) => r._measurement == "soil" and r._field == "soil_moisture")
        |> drop(columns: ["device_brand", "device_model", "_field"])
        |> window(every: windowSize, createEmpty: false)
        |> mean()
        |> duplicate(column: "_start", as: "_time")

// Result for the selected sensor
daily_average_by_sensor
    |> filter(fn: (r) => r["device"] == _device)
    |> group(columns: ["_time", "_measurement"])
    |> mean()
    |> group()
    |> yield(name: "sensor")

// Result for all sensors
daily_average_by_sensor
    |> group(columns: ["_time", "_measurement"])
    |> mean()
    |> group()
    |> yield(name: "peers")