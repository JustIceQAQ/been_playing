from helpers.storage.coordinate import Coordinate, GeoPoint, OpenStreetMap, Wiki, GoogleMaps
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType

{% set venue_type = "" %}
{% if cookiecutter.target_sub_directory == "museums" %}
    {% set venue_type = "VenueType.MUSEUM" %}
{% elif cookiecutter.target_sub_directory == "galleries" %}
    {% set venue_type = "VenueType.GALLERY" %}
{% elif cookiecutter.target_sub_directory == "platform" %}
    {% set venue_type = "VenueType.PLATFORM" %}
{% endif %}

class {{cookiecutter.script_code}}Information:
    @staticmethod
    def get_information() -> Information:
        {% if cookiecutter.target_sub_directory == "platform" %}
        return Information(
            fullname="",
            code_name="",
            external_link="",
            venue_type={{venue_type}},
        )
        {% else %}
        return Information(
            location_code=Taiwan.taipei,
            fullname="",
            code_name="",
            external_link="",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates=None),
                open_street_map=OpenStreetMap(),
                wiki=Wiki(
                    wikidata=None,
                    wikipedia=None,
                ),
                google_maps=GoogleMaps(plus_code=None),
            ),
            venue_type={{venue_type}},
        )
        {% endif %}