from helpers.storage.coordinate import Coordinate, GeoPoint, GoogleMaps, OpenStreetMap, Wiki
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType


class SSHMInformation:
    @staticmethod
    def get_information() -> Information:
        return Information(
            location_code=Taiwan.new_taipei.bali_65000230,
            fullname="新北市立十三行博物館",
            code_name="SSHM",
            external_link="https://www.sshm.ntpc.gov.tw/submenu?usein=2&psid=0G244574557570145140",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.156992481305682, 121.40486107034219"),
                open_street_map=OpenStreetMap(osm_url="https://www.openstreetmap.org/way/230093070"),
                wiki=Wiki(
                    wikidata="Q7496482",
                    wikipedia="zh:新北市立十三行博物館",
                ),
                google_maps=GoogleMaps(plus_code="5C43+PW 頂罟里 新北市八里區"),
            ),
            venue_type=VenueType.MEMORIAL,
        )
