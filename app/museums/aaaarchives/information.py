from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, OpenStreetMapKeys, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class AAAArchivesInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.new_taipei.linkou_65000170,
            fullname="國家發展委員會檔案管理局",
            code_name="AAAArchives",
            external_link="https://aaa.archives.tw/tw/event/306.html",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.07521442685089, 121.37402598256791"),
                address="244013新北市林口區檔案館路1號行政區",
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/456206409",
                    keys=OpenStreetMapKeys(
                        tourism="museum",
                    ),
                ),
                wiki=Wiki(
                    wikidata="Q124259497",
                    wikipedia="zh:國家檔案館 (中華民國)",
                ),
                google_maps=GoogleMaps(plus_code="39FF+GP 林口區 新北市"),
            ),
            venue_type=VenueType.MUSEUM,
        )
