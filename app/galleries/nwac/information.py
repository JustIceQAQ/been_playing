from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, OpenStreetMapKeys, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class NWACInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.kaohsiung.gushan_64000020,
            fullname="內惟藝術中心",
            code_name="NWAC",
            external_link="https://www.nwac.org.tw/tw/appreciate-art",
            branch_coordinates=Coordinate(
                location_code=Taiwan.kaohsiung.gushan_64000020,
                address="804407高雄市鼓山區馬卡道路329號",
                geo_point=GeoPoint(raw_coordinates="22.657349239890017, 120.28221485039553"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/1111577600",
                    keys=OpenStreetMapKeys(
                        tourism="museum",
                        museum="art",
                        air_conditioning="yes",
                    ),
                ),
                wiki=Wiki(
                    wikidata="Q115133489",
                    wikipedia=None,
                ),
                google_maps=GoogleMaps(plus_code="M74J+VW 龍水里 高雄市鼓山區"),
            ),
            venue_type=VenueType.ART_VILLAGE,
        )
