from app.db.session import Base
import app.models # Trigger imports

print("Tables in Base.metadata:")
for table_name, table in Base.metadata.tables.items():
    print(f"\nTable: {table_name}")
    for column in table.columns:
        print(f"  Column: {column.name}, Type: {column.type}, Primary Key: {column.primary_key}")
