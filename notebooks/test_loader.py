import sys
sys.path.append('.')  # so Python finds the src/ folder

from src.data_loader import load_clean_data

df = load_clean_data()

print("Shape:", df.shape)
print()
print("Dtypes:\n", df.dtypes)
print()
print("Date range:", df['date'].min(), "to", df['date'].max())
print()
print("Missing values:\n", df.isnull().sum())
print()
print(df.head(3))

df.to_csv('data/clean_data.csv', index=False)
print("✅ clean_data.csv saved successfully")
