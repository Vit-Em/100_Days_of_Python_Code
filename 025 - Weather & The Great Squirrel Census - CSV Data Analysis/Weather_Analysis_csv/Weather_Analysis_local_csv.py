import pandas as pd

data = pd.read_csv("weather_data1.csv")
print(data["temp"])

data_dict = data.to_dict()
# Get data from rows
print(data[data.day == "Monday"])
print(data[data.temp == data.temp.max()])

monday = data[data.day == "Monday"]
print(monday.condition.iloc[0])
monday_temp = monday.temp.iloc[0]
print((monday_temp * 9 / 5) + 32)  # In Fahrenheit


data = pd.DataFrame(data_dict)

