from fastapi import FastAPI
import pyodbc
import os
from dotenv import load_dotenv

app = FastAPI()

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/data/")
def read_data():
    with pyodbc.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 10 * FROM DataHistory1")
        result = cursor.fetchall()
        return {"data": [dict(zip([column[0] for column in cursor.description], row)) for row in result]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
