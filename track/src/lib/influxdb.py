from .utils import Location

import logging
import os

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class UpdateSender:
    def __init__(self) -> None:
        self.server = os.environ.get("INFLUXDB_URL")
        self.bucket = os.environ.get("INFLUXDB_ORG")
        self.org = os.environ.get("INFLUXDB_BUCKET")
        self.INFLUX_TOKEN = os.environ.get("INFLUXDB_TOKEN")

        self.write_client = influxdb_client.InfluxDBClient(url="http://influxdb:8086", token=self.INFLUX_TOKEN, org=self.org)
        self.write_api = self.write_client.write_api(write_options=SYNCHRONOUS)

    def send_update(self, location: Location):
        point = {
            'measurement': 'gpstrack',
            'time': str(location.lts),
            'tags': {
                'source': 'mobilepi'
            },
            'fields': {
                'lat': float(location.lat),
                'lon': float(location.lon),
                'alt': float(location.alt),
                'gts': str(location.gts)
            }
        }
        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        except Exception as e:
            logging.error("%s", e)
        logging.debug("Sent update to influxdb")
