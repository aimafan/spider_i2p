import click
from spider_i2p import __version__
from spider_i2p.myutils.logger import logger
from spider_i2p.handle.statistic import statistic


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--version", "show_version", is_flag=True,
    help="Show spider i2p version and exit."
)
def main(ctx, show_version):
    if show_version:
        import sys
        logger.info(f"spider_i2p version: "
                    f"{__version__}")
        sys.exit()


main.add_command(statistic)



if __name__ == '__main__':
    main()
