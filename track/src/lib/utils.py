import json

class Location:
    def __init__(self, lat, lon, alt, gts, lts) -> None:
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.gts = gts
        self.lts = lts

    def __repr__(self) -> str:
        return json.dumps(
            {"lat": self.lat, "lon": self.lon, "alt": self.alt, "gts": self.gts, "lts": self.lts}
        )
