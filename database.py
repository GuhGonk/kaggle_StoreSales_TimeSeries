import os
import polars as pl
from sqlalchemy import create_engine

def write_db():
    os.makedirs('data', exist_ok=True)
    engine = create_engine('sqlite:///data/train_combined.db')
    df = pl.read_parquet("data/train_combined.parquet")
    df.write_database("train_combined", engine)
    print(os.path.getsize('data/train_combined.db'))

if __name__ == "__main__":
    write_db()