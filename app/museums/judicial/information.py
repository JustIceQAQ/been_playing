from helpers.storage.coordinate import Coordinate, GeoPoint, GoogleMaps, OpenStreetMap, Wiki
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class JudicialInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.tainan.west_central_67000370,
            fullname="司法博物館",
            code_name="Judicial",
            external_link="https://www.judicial.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.98932000952443, 120.20118433329041"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/274594793"),
                wiki=Wiki(
                    wikidata="Q10911353",
                    wikipedia="zh:原臺南地方法院",
                ),
                google_maps=GoogleMaps(plus_code="X6Q2+MF 中西區 臺南市"),
            ),
            venue_type=VenueType.MUSEUM,
        )
