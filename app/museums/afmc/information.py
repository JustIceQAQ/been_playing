from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, OpenStreetMapKeys, Wiki, GoogleMaps
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
                    keys=OpenStreetMapKeys(
                        amenity="theatre",
                    ),
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
                address="320003桃園市中壢區中央里中美路16號",
                geo_point=GeoPoint(raw_coordinates="24.958508250916836, 121.22748825365926"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/109846806",
                    keys=OpenStreetMapKeys(
                        amenity="theatre",
                    ),
                ),
                wiki=Wiki(
                    wikidata="Q17014888",
                    wikipedia="zh:中壢藝術館",
                ),
                google_maps=GoogleMaps(plus_code="X65G+8X 中央里 桃園市中壢區"),
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
                location_code=Taiwan.taoyuan.taoyuan_68000010,
                address="330028桃園市桃園區永安里埔新路12號",
                geo_point=GeoPoint(raw_coordinates="24.9993184568463, 121.30744636786362"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/546054453"),
                google_maps=GoogleMaps(plus_code="X8X4+MX 永安里 桃園市桃園區"),
            ),
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
                location_code=Taiwan.taoyuan.zhongli_68000020,
                address="330桃園市桃園區同安里中正路1188號",
                geo_point=GeoPoint(raw_coordinates="25.017657555942453, 121.30002828249722"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/256114883"),
                google_maps=GoogleMaps(plus_code="278X+XX 同安里 桃園市桃園區"),
            ),
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
                location_code=Taiwan.taoyuan.guishan_68000070,
                address="333桃園市龜山區復興一路8號機場捷運A8長庚醫院站 Global mall 3樓",
                geo_point=GeoPoint(raw_coordinates="25.06063397917656, 121.36993362482592"),
                google_maps=GoogleMaps(plus_code="3969+5X 龜山區 桃園市"),
            ),
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
                location_code=Taiwan.taoyuan.dayuan_68000060,
                address="337002桃園市大園區青峰里領航北路四段216號",
                geo_point=GeoPoint(raw_coordinates="25.02441059026342, 121.21753328064304"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/185227330"),
                google_maps=GoogleMaps(plus_code="26F9+M2 青峰里 桃園市大園區"),
            ),
            venue_type=VenueType.ART_MUSEUM,
        )
