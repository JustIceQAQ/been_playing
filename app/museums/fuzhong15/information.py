from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class FuZhong15Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.new_taipei.banqiao_65000010,
            fullname="府中15",
            code_name="FuZhong15",
            external_link="https://www.fuzhong15.ntpc.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.0096705639475, 121.4595574225735"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/288089701",
                ),
                wiki=Wiki(
                    wikidata="Q65045652",
                    wikipedia="zh:府中15新北市動畫故事館",
                ),
                google_maps=GoogleMaps(plus_code="2F55+QR 挹秀里 新北市板橋區"),
            ),
            venue_type=VenueType.GALLERY,
        )
