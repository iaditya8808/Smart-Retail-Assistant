import pandas as pd


df = pd.read_csv("data/retail_sales.csv")

print("Original Shape:", df.shape)

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
df["day"] = df["Date"].dt.day
df["month"] = df["Date"].dt.month
df["year"] = df["Date"].dt.year

print("Cleaned Shape:", df.shape)
print(df.head())

df.to_csv("data/cleaned_retail_sales.csv", index=False)

print("Preprocessing completed successfully")
