import pathlib

import click
from code_template import PARSE_CODE, SCRIPT_CODE

ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
SCRIPT_FOLDER = ROOT_DIR / "app"


@click.command()
@click.option("--script_code", prompt="Your Script Code", help="Your Script Code")
def create_exhibition_template(script_code: str):
    app_script_folder = SCRIPT_FOLDER / script_code

    if app_script_folder.exists():
        click.echo(f"{script_code} folder exists!")
        return
    app_script_folder.mkdir()
    with (app_script_folder / "__init__.py").open(mode="a+", encoding="utf-8") as f:
        pass

    with (app_script_folder / "script.py").open(mode="a+", encoding="utf-8") as f:
        f.write(SCRIPT_CODE.format(script_code=script_code))
    with (app_script_folder / "parse.py").open(mode="a+", encoding="utf-8") as f:
        f.write(PARSE_CODE.format(script_code=script_code))

    click.echo(f"{script_code} folder created!")


if __name__ == "__main__":
    create_exhibition_template()
