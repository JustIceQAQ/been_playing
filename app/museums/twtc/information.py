from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, OpenStreetMapKeys, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class TwTcInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="台北世貿中心",
            code_name="TwTc",
            external_link="https://twtc.com.tw/exhibition?p=home",
            location_code=Taiwan.taipei.xinyi_63000020,
            branch_coordinates=[
                Coordinate(
                    location_code=Taiwan.taipei.xinyi_63000020,
                    name="世貿一館",
                    geo_point=GeoPoint(
                        raw_coordinates="25.03358007614386, 121.56240955530657",
                    ),
                    open_street_map=OpenStreetMap(
                        osm_url="https://www.openstreetmap.org/way/137077752",
                        keys=OpenStreetMapKeys(
                            amenity="exhibition_centre",
                        ),
                    ),
                    google_maps=GoogleMaps(plus_code="2HM6+9X 西村里 臺北市信義區"),
                ),
                Coordinate(
                    location_code=Taiwan.taipei.nangang_63000090,
                    name="南港展覽館1館",
                    geo_point=GeoPoint(
                        raw_coordinates="25.056650206854755, 121.61812883883394",
                    ),
                    open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/73567713"),
                    google_maps=GoogleMaps(plus_code="3J49+J6 三重里 臺北市南港區"),
                ),
                Coordinate(
                    location_code=Taiwan.taipei.nangang_63000090,
                    name="南港展覽館2館",
                    raw_coordinates="25.05610107423643, 121.61623519926233",
                    geo_point=GeoPoint(
                        raw_coordinates="25.05610107423643, 121.61623519926233",
                    ),
                    open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/558011740"),
                    wiki=Wiki(
                        wikidata="Q28409336",
                        wikipedia="zh:台北南港展覽館2館",
                    ),
                    google_maps=GoogleMaps(plus_code="3J48+CF 三重里 臺北市南港區"),
                ),
                Coordinate(
                    location_code=Taiwan.taichung.xitun_66000060,
                    name="臺中國際會展中心",
                    geo_point=GeoPoint(
                        raw_coordinates="24.19381567538611, 120.65129562551822",
                    ),
                    open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/1305878545"),
                    wiki=Wiki(
                        wikidata="Q28410924",
                        wikipedia="zh:臺中國際會展中心",
                    ),
                    google_maps=GoogleMaps(plus_code="5MV2+FG 港尾里 臺中市西屯區"),
                ),
            ],
            venue_type=VenueType.EXPO_CENTER,
        )
