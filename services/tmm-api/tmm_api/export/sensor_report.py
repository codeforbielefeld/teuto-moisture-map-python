def query(sensor: int, bucket: str):
    return f"""
this_week_data = from(bucket: "{bucket}")
  |> range(start: -7d)
  |> filter(fn: (r) => r["_measurement"] == "moisture")
  |> filter(fn: (r) => r["_field"] == "percent")

this_week_data
  |> filter(fn: (r) => r["device"] == "{sensor}")
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> yield(name: "current")

this_week_data
  |> drop(columns: ["device", "device_brand", "device_model"])
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> yield(name: "currentAverage")

last_year_data= from(bucket: "{bucket}")
  |> range(start: -372d, stop: -365d)
  |> filter(fn: (r) => r["_measurement"] == "moisture")
  |> filter(fn: (r) => r["_field"] == "percent")

last_year_data
  |> filter(fn: (r) => r["device"] == "{sensor}")
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> timeShift(duration: 365d)
  |> yield(name: "previousYear")

last_year_data
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> timeShift(duration: 365d)
  |> yield(name: "previousYearAverage")
"""
