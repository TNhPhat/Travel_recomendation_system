import pandas as pd
from sqlalchemy import create_engine

USER = "tnphat"
PASS = "your_password"
HOST = "your_public_ip"   # Vd: 34.122.10.10
PORT = 5432
DB   = "your_database"

engine = create_engine(f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")

table = "location"  # bảng bạn muốn tải

df = pd.read_sql(f'SELECT * FROM {table}', engine)
df.to_csv(f"{table}.csv", index=False)

print("Downloaded xong!")
