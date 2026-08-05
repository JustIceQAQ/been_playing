from helpers.storage.coordinate import Coordinate, GeoPoint, GoogleMaps, OpenStreetMap
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class ShungYeArtInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="順益台灣美術館",
            code_name="ShungYeArt",
            external_link="https://www.shungye-art.org/show_now.php",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.046560256806668, 121.51092983908268"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/948948333"),
                google_maps=GoogleMaps(plus_code="2GW6+H9 光復里 臺北市中正區"),
            ),
            venue_type=VenueType.ART_MUSEUM,
        )
