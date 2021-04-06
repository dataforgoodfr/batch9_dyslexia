import click
from dyslexia.eval.eval_utils import eval_folder
from pathlib import Path


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--truth_path",
    required=True,
    help="Path to the ground truth folder",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True),
)
@click.option(
    "--hypothesis_path",
    required=True,
    help="Path to the ground prediction folder",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True),
)
def eval_txt_folder(
    truth_path: str,
    hypothesis_path: str,
):
    evaluation = eval_folder(Path(truth_path), Path(hypothesis_path))

    for k, v in evaluation.items():
        click.echo(f"{k} : {v}")


cli.add_command(eval_txt_folder)
