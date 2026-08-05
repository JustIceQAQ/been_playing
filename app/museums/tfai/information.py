from helpers.storage.coordinate import Coordinate, GeoPoint, GoogleMaps, OpenStreetMap, OpenStreetMapKeys, Wiki
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class TFAIInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="國家電影及視聽文化中心",
            code_name="TFAI",
            external_link="https://www.tfai.org.tw/zh/program/index",
            branch_coordinates=Coordinate(
                location_code=Taiwan.new_taipei.xinzhuang_65000050,
                geo_point=GeoPoint(raw_coordinates="25.056266080543743, 121.44711925387705"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/1019205802", keys=OpenStreetMapKeys(wheelchair="yes")
                ),
                wiki=Wiki(
                    wikidata="Q9685293",
                    wikipedia="zh:國家電影及視聽文化中心",
                ),
                google_maps=GoogleMaps(plus_code="3C4W+CR 中原里 新北市新莊區"),
            ),
            venue_type=VenueType.MUSEUM,
        )
