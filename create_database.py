# Imports
import os
import sys
#import csv
#import json
#import datetime
import mysql.connector

#Functions
def sql_init():
    # MySQL Connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Atiradeon1",
        database="the_weathermen"
        )
    print(mydb)
    mycursor = mydb.cursor()

    print("Removing old data...")
    mycursor.execute("DROP TABLE IF EXISTS locations")
    print("\ttable(locations) deleted.")

    print("Generating tables...")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS locations (
        loc_index INT PRIMARY KEY,
        city VARCHAR(255),
        state VARCHAR(255),
        loc_date VARCHAR(20),
        totalHigh INT,
        totalLow INT,
        totalUV INT,
        totalSun FLOAT,
        totalSnow FLOAT,
        totalRainfall FLOAT,
        totalHumidity INT,
        totalPressure INT,
        totalWindSpeed INT,
        avgHigh FLOAT,
        avgLow FLOAT,
        avgSun FLOAT,
        avgUV FLOAT,
        avgSnow FLOAT,
        avgRainfall FLOAT,
        avgHumidity FLOAT,
        avgPressure FLOAT,
        avgWindSpeed FLOAT
        )"""
    )
    print("\ttable(locations) created.")

def main():
    sql_init()

if __name__ == '__main__':
    main()
