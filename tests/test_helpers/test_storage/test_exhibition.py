import pathlib
import tempfile
import uuid

import pytest

from helpers.storage.helper import ExhibitionData, ExhibitionStorage


def test_exhibition_data(fake_dict: dict):
    ed = ExhibitionData.model_validate(fake_dict)
    assert ed.title == fake_dict["title"]
    assert ed.date == fake_dict["date"]
    assert ed.address == fake_dict["address"]
    assert ed.figure == fake_dict["figure"]
    assert ed.source_url == fake_dict["source_url"]

    this_uuid = uuid.uuid5(
        uuid.UUID("00000000-0000-0000-0000-000000000000"), fake_dict["source_url"]
    ).hex

    assert ed.UUID == this_uuid


@pytest.mark.asyncio
async def test_exhibition_storage(fake_dict: dict):
    es = ExhibitionStorage()
    es.data = [
        ExhibitionData.model_validate(fake_dict),
        ExhibitionData.model_validate(fake_dict),
    ]
    with tempfile.TemporaryDirectory() as tmp_dir:
        await es.save_to_local("QAQ", folder=pathlib.Path(tmp_dir))
        assert (pathlib.Path(tmp_dir) / "QAQ.json").exists() is True
