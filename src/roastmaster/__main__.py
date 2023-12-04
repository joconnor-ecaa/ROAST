"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Roastmaster."""


if __name__ == "__main__":
    main(prog_name="roastmaster")  # pragma: no cover
