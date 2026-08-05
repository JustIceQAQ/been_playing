from helpers.storage.coordinate import Coordinate, GeoPoint, GoogleMaps, OpenStreetMap, OpenStreetMapKeys, Wiki
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class TmcInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="台北流行音樂中心",
            code_name="Tmc",
            external_link="https://www.tmc.taipei/tw/blog/show?filter=eyJkaXJlY3Rpb24iOiJsYXN0ZXN0In0=",
            branch_coordinates=Coordinate(
                location_code=Taiwan.taipei.nangang_63000090,
                geo_point=GeoPoint(raw_coordinates="25.05181188396233, 121.59745382637806"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/relation/12329376",
                    keys=OpenStreetMapKeys(amenity="arts_centre"),
                ),
                wiki=Wiki(
                    wikidata="Q7676273",
                    wikipedia="zh:臺北流行音樂中心",
                ),
                google_maps=GoogleMaps(plus_code="3H2X+J2 新光里 臺北市南港區"),
            ),
            venue_type=VenueType.EXPO_CENTER,
        )
