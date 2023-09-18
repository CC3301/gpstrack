from .utils import Location

import logging

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class UpdateSender:
    def __init__(self, server: str, fallback_file: str, cache_size: int) -> None:
        self.server = server
        self.fallback_file = fallback_file

        self.bucket = "gpstrack"
        self.org = "gpstrack"

        self.INFLUX_TOKEN = "PBMq2IX4yiF_Ku5_1JRyQ5E189d-SuG8da9yTywl7ltcMVfxB6e623pLrxL7_ozhe1tmTSq_8hxY98W1_jiAPw=="

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
