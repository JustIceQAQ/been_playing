from helpers.storage.coordinate import Coordinate, GeoPoint, GoogleMaps, OpenStreetMap
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class XZCACInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.new_taipei.xinzhuang_65000050,
            fullname="新莊文化藝術中心",
            code_name="XZCAC",
            external_link="https://www.xzcac.ntpc.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.047496956532754, 121.44417476256956"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/258599429"),
                google_maps=GoogleMaps(plus_code="2CWV+VM 立基里 新北市新莊區"),
            ),
            venue_type=VenueType.CREATIVE_PARK,
        )
