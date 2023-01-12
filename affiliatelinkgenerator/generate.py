import sys
import click
from pathlib import Path
import json
from mysql_connector import update_row, get_all
from logger import logger
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, SpinnerColumn, TimeRemainingColumn, TimeElapsedColumn, MofNCompleteColumn
from affiliate_link_generator import get_link


progress = Progress(
    SpinnerColumn(),
    MofNCompleteColumn(),
    BarColumn(bar_width=None),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    transient=True
)


def terminate(msg='Can not continue. Please consult logs for details'):
    sys.exit(msg)


@click.command()
@click.option("--config", required=True, help="File containing configuration options")
@click.option("--domain", default=None, required=False, help="Only generate for courses from this domain. If none provided, all are generated.")
@click.option('--newonly', is_flag=True, default=False, help="Generates only for the courses who's affiliate link field is empty.")
@click.option('--retry-interval', required=False, default=0, help="Waits this much time in seconds before retrying in case of a HTTP response 429. Default is 0 in which case, retry won't be attempted.")
def main(config, domain, newonly, retry_interval):
    """Simple script that updates the product table with affiliate link."""
    configfile = Path(config)

    if configfile.exists():
        with open(configfile) as f:
            try:
                config = json.loads(f.read())
            except json.JSONDecodeError as e:
                logger(e, level=40)
                terminate()

    processed = 0
    failed = 0
    updated = 0

    products = get_all(config, domain, newonly)

    # with progress:
    #     for product in progress.track(products):
    for product in products:
        link = get_link(config, product, retry_interval)
        if link:
            if update_row(config, product[0], link):
                updated = updated + 1
            else:
                failed = failed + 1
        else:
            failed = failed + 1
        processed = processed + 1

    logger(f'Updated: {updated}')
    logger(f'Failed: {failed}')
    logger(f'Number of records processed: {processed}')
    logger('\n')


if __name__ == '__main__':
    logger('#################### SUMMARY ####################')
    main()
