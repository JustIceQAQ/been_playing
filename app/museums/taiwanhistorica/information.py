from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class TaiwanHistoricaInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.nantou.nantou_10008010,
            fullname="國史館臺灣文獻館",
            code_name="TaiwanHistorica",
            external_link="https://www.th.gov.tw/News/232/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="23.936085705151037, 120.7005354733869"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/233598767"),
                wiki=Wiki(
                    wikidata="Q10926785",
                    wikipedia="zh:國史館臺灣文獻館",
                ),
                google_maps=GoogleMaps(plus_code=None),
            ),
            venue_type=VenueType.MUSEUM,
        )
