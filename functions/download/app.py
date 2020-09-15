import csv
import ftplib
import hashlib
import json
import os
import tempfile
import sys
import time

import mysql.connector
from tqdm import tqdm
import pandas as pd

sql = mysql.connector.connect(host="localhost", user='root', password="Test1234@", database='traineeboats')

rootUrl = 'ftp.ais.dk'
with ftplib.FTP(rootUrl) as ftp:
    ftp.login()
    files = ftp.nlst("/ais_data")
    files = [x for x in files if ".csv" in x]
    files = sorted(files, reverse=True)
    for file in files:
        if file.lower().endswith(".csv"):
            tmpFile = tempfile.NamedTemporaryFile()

            file_copy = tmpFile.name
            size = ftp.size(file)
            bar = tqdm(size, total=size, desc=file_copy + " : " + file, unit_scale=True, unit_divisor=1024)

            with open(file_copy, 'wb') as fp:
                def file_write(data):
                    fp.write(data)
                    bar.update(len(data))


                res = ftp.retrbinary('RETR ' + file, file_write)
                if not res.startswith('226 Transfer complete'):

                    print('Download failed')
                    if os.path.isfile(file_copy):
                        os.remove(file_copy)
                bar.close()
                cursor = sql.cursor()

                df = pd.read_csv(file_copy, chunksize=1000, na_filter='')
                length = sum(1 for line in open(file_copy))
                bar = tqdm(size, total=length, desc="uploading : " + file_copy)
                for chunk in df:
                    val = []
                    for index, row in chunk.iterrows():
                        val1 = (
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                            row[11], row[17], row[19],
                            row[20], row[21])
                        j = json.dumps(val1).encode('utf-8')
                        hash1 = hashlib.sha256(j).hexdigest()
                        val1 = val1 + (hash1,)
                        val.append(val1)
                        bar.update()

                    cursor.executemany(
                        "INSERT IGNORE INTO fact_ais(timestamp, mobile_status, mmsi, latitude, longitude, nav_status, rot, sog, cog, heading, imo, callsign, position_device, destination, eta, source_type, hash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        val)
                    sql.commit()
                bar.close()
                print("done")
                os.remove(file_copy)
