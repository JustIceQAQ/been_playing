from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class HuaLien1913Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.hualien.hualien_10015010,
            fullname="花蓮文化創意產業園區",
            code_name="HuaLien1913",
            external_link="https://hualien1913.nat.gov.tw/%E6%9C%80%E6%96%B0%E6%B4%BB%E5%8B%95/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="23.9763503793684, 121.60487540801596"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/377074887",
                ),
                wiki=Wiki(
                    wikidata="Q22569311",
                    wikipedia="zh:花蓮文化創意產業園區",
                ),
                google_maps=GoogleMaps(plus_code="XJG3+FW 主工里 花蓮縣花蓮市"),
            ),
            venue_type=VenueType.CREATIVE_PARK,
        )
