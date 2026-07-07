from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class NTPCInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.new_taipei.yingge_65000080,
            fullname="新北市立鶯歌陶瓷博物館",
            code_name="NTPC",
            external_link="https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.949406697655782, 121.3520648774411"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/238680127"),
                wiki=Wiki(
                    wikidata="Q7012025",
                    wikipedia="zh:新北市立鶯歌陶瓷博物館",
                ),
                google_maps=GoogleMaps(plus_code="W9X2+PR 南靖里 新北市鶯歌區"),
            ),
            venue_type=VenueType.MUSEUM,
        )
