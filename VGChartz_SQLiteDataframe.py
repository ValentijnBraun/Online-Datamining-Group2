# Some parts are retrieved from ChatGPT (2023)
import pandas as pd
import json
import sqlite3
from tabulate import tabulate

# read json file
df = pd.read_json("C:\\Users\melan\VGChartz\VGChartz\VGChartz.json")

# connect with SQLite-database 
conn = sqlite3.connect("VGChartz_database.db")

# create'VGChartz_database'
df.to_sql("VGChartz_Database", conn, if_exists="replace", index=False)

# add cursor
cursor = conn.cursor()

# run a SQL query to select all information from 'VGChartz_database'
cursor.execute("SELECT * FROM VGChartz_Database")

# Add column names 
headers = ["Game Title", "Console", "Publisher", "VGChartz Score", "Critic Score", "User Score", "Total Shipped", "Release Date", "Last Update", "genre"]

# fetch rows
rows = cursor.fetchall()

# use tabulate for table format
table = tabulate(rows, headers=headers)

# Save as CSV-bestand
with open("VGChartz_Database.csv", "w", newline="", encoding='utf-8-sig') as csvfile:
    csvfile.write(table)

# Sluit de cursor en de verbinding met de database
cursor.close()
conn.close()





