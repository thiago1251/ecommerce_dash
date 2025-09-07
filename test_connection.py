from db_connection import load_table

try:
    df = load_table("top5_reconocidas")
    print(df.head())
    print("Conexión exitosa")
except Exception as e:
    print(" Error de conexión:", e)
