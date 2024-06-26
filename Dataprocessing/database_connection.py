import os, time
from influxdb_client_3 import InfluxDBClient3, Point


class Dbconnection:
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "Stem voor de Maas"
    host = "https://us-east-1-1.aws.cloud2.influxdata.com"
    client = InfluxDBClient3(host=host, token=token, org=org)
    database = "StemVoorDeMaas"
    db_con = False

    @staticmethod
    def check_database_connection():
        Dbconnection.db_con = True
        return Dbconnection.db_con

    @staticmethod
    def query_data(temperatuur, waterpeil, waterflow, ph_waarde):
        data = [
            Point("Temperatuur").field("Meet-data", temperatuur),
            Point("Waterpeil").field("Meet-data", waterpeil),
            Point("Waterflow").field("Meet-data", waterflow),
            Point("Ph-waarde").field("Meet-data", ph_waarde)
        ]

        for point in data:
            Dbconnection.client.write(database=Dbconnection.database, record=point)
            time.sleep(1)

