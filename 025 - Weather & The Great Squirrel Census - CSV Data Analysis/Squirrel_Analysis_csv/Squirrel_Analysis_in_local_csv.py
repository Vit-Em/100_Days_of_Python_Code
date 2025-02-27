import pandas as pd
data = pd.read_csv("2018_Squirrel_Data.csv")

grey_squirrels_cont = len(data[data["Primary Fur Color"] == "Gray"])
black_squirrels_cont = len(data[data["Primary Fur Color"] == "Black"])
cinnamon_squirrels_cont = len(data[data["Primary Fur Color"] == "Cinnamon"])

data_dict = {
    "Fur Color": ["Gray", "Black", "Cinnamon"],
    "Count": [grey_squirrels_cont, black_squirrels_cont, cinnamon_squirrels_cont]
}
df = pd.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")