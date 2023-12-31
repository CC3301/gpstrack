import logging

import gps
from datetime import datetime


from lib.influxdb import UpdateSender
from lib.utils import Location

import os

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.FATAL)

class Track:
    def __init__(self, us: UpdateSender, gps_host: str) -> None:
        self.us = UpdateSender()
        self.gps_host = os.environ.get("GPSD_REMOTE_HOST")
        self.session = gps.gps(host=self.gps_host, mode=gps.WATCH_ENABLE)

    def watch_update(self) -> None:
        try:
            while 0 == self.session.read():
                if not (gps.MODE_SET & self.session.valid):
                    continue
                else:
                    gts = self.session.fix.time # GPS-Timestamp
                    lts = datetime.now().isoformat() # Local-Timestamp

                    if gps.isfinite(self.session.fix.altitude):
                        alt = "%.6f" % self.session.fix.altitude 
                    
                    if gps.isfinite(self.session.fix.latitude):
                        lat = "%.6f" % self.session.fix.latitude

                    if gps.isfinite(self.session.fix.longitude):
                        lon = "%.6f" % self.session.fix.longitude

                    self.us.send_update(
                        Location(lat, lon, alt, gts, lts)
                    )

                    logging.debug("Raw GPS-Time: %s", self.session.fix.time)
                    logging.info("Extracted Data: Lat: %s, Lon %s, Alt: %s, GPS-Time: %s, Local-Time: %s", lat, lon, alt, gts, lts)
                    
        except KeyboardInterrupt:
            #self.us.flush_all()
            logging.info("Shutdown. Bye.")


if __name__ == "__main__":
    Track().watch_update()
