from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, Wiki
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType

BASE_URL = "https://www.afmc.gov.tw"


class AfmcHall1Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="桃園展演中心",
            code_name="AfmcHall1",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.017555022836635, 121.29841018064276"),
                raw_coordinates="25.017555022836635, 121.29841018064276",
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/304360932",
                    amenity="theatre",
                ),
                wiki=Wiki(
                    wikidata="Q11112020",
                    wikipedia="zh:桃園展演中心",
                ),
            ),
            location_code=Taiwan.taoyuan.taoyuan_68000010,
            venue_type=VenueType.EXPO_CENTER,
        )


class AfmcHall2Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="中壢藝術館",
            code_name="AfmcHall2",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                location_code=Taiwan.taoyuan.zhongli_68000020,
                geo_point=GeoPoint(raw_coordinates="24.958508250916836, 121.22748825365926"),
                raw_coordinates="24.958508250916836, 121.22748825365926",
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/109846806",
                    amenity="theatre",
                ),
                wiki=Wiki(
                    wikidata="Q17014888",
                    wikipedia="zh:中壢藝術館",
                ),
            ),
            location_code=Taiwan.taoyuan.zhongli_68000020,
            venue_type=VenueType.MUSEUM,
        )


class AfmcHall3Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="桃園光影文化館",
            code_name="AfmcHall3",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.999357351659583, 121.30748928249685"),
                raw_coordinates="24.999357351659583, 121.30748928249685",
            ),
            location_code=Taiwan.taoyuan.taoyuan_68000010,
            venue_type=VenueType.ART_MUSEUM,
        )


class AfmcHall4Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="桃園藝文廣場",
            code_name="AfmcHall4",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.017657555942453, 121.30002828249722"),
                raw_coordinates="25.017657555942453, 121.30002828249722",
            ),
            location_code=Taiwan.taoyuan.zhongli_68000020,
            venue_type=VenueType.ART_MUSEUM,
        )


class AfmcHall5Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="A8藝文中心",
            code_name="AfmcHall5",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.06063397917656, 121.36993362482592"),
                raw_coordinates="25.06063397917656, 121.36993362482592",
            ),
            location_code=Taiwan.taoyuan.guishan_68000070,
            venue_type=VenueType.ART_MUSEUM,
        )


class AfmcHall6Information:
    @staticmethod
    def get_information() -> Information:
        return Information(
            fullname="桃園陽光劇場",
            code_name="AfmcHall6",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.02441059026342, 121.21753328064304"),
                raw_coordinates="25.02441059026342, 121.21753328064304",
            ),
            location_code=Taiwan.taoyuan.dayuan_68000060,
            venue_type=VenueType.ART_MUSEUM,
        )
