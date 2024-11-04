import pathlib
import tempfile
import uuid

import pytest

from helpers.storage.helper import Exhibition, ExhibitionItem, Information


def test_exhibition_data(fake_exhibition_data: dict):
    ed = ExhibitionItem.model_validate(fake_exhibition_data)
    assert ed.title == fake_exhibition_data["title"]
    assert ed.date == fake_exhibition_data["date"]
    assert ed.address == fake_exhibition_data["address"]
    assert ed.figure == fake_exhibition_data["figure"]
    assert ed.source_url == fake_exhibition_data["source_url"]

    this_uuid = uuid.uuid5(
        uuid.UUID("00000000-0000-0000-0000-000000000000"),
        fake_exhibition_data["source_url"],
    ).hex

    assert ed.UUID == this_uuid


@pytest.mark.asyncio
async def test_exhibition_storage(
    fake_exhibition_data: dict, fake_exhibition_information: dict
):
    es = Exhibition(information=Information.model_validate(fake_exhibition_information))
    es.items = [
        ExhibitionItem.model_validate(fake_exhibition_data),
        ExhibitionItem.model_validate(fake_exhibition_data),
    ]
    with tempfile.TemporaryDirectory() as tmp_dir:
        await es.save_to_local("QAQ", folder=pathlib.Path(tmp_dir))
        assert (pathlib.Path(tmp_dir) / "QAQ.json").exists() is True


def test_exhibition_sort(fake_exhibition_data: dict):
    min_obj = ExhibitionItem()
    max_obj = ExhibitionItem.model_validate(fake_exhibition_data)
    all_obj = sorted([max_obj, min_obj])

    assert id(all_obj[0]) == id(min_obj)
    assert id(min(all_obj)) == id(min_obj)

    assert id(all_obj[-1]) == id(max_obj)
    assert id(max(all_obj)) == id(max_obj)
