from helpers.storage.coordinate import Coordinate, GeoPoint, GoogleMaps, OpenStreetMap, OpenStreetMapKeys, Wiki
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class HuaShan1914Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="華山1914文化創意產業園區",
            code_name="HuaShan1914",
            external_link="https://www.huashan1914.com/w/huashan1914/exhibition",
            branch_coordinates=Coordinate(
                google_maps=GoogleMaps(plus_code="2GVH+JP 梅花里 臺北市中正區"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/relation/5177809",
                    keys=OpenStreetMapKeys(
                        amenity="arts_centre",
                        landuse="retail",
                        tourism="attraction",
                        type="multipolygon",
                    ),
                ),
                wiki=Wiki(wikidata="Q14594864", wikipedia="zh:華山1914文化創意產業園區"),
                geo_point=GeoPoint(raw_coordinates="25.044242402011122, 121.5292898083939"),
                raw_coordinates="25.044242402011122, 121.5292898083939",
            ),
            venue_type=VenueType.CREATIVE_PARK,
        )
