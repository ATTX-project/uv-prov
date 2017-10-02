from uvprov_api.app import init_api
import click
import schedule
import time
import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems
from uvprov_api.utils.logs import app_logger
from uvprov_api.utils.messaging import prov_job
import os

interval = {'timer': os.environ['QTIME'] if 'QTIME' in os.environ else 30}


@click.group()
def cli():
    """Run cli tool."""
    pass


@cli.command('server')
@click.option('--host', default='127.0.0.1', help='host uvprovAPI host.')
@click.option('--port', default=4301, help='uvprovAPI server port.')
@click.option('--workers', default=2, help='uvprovAPI server workers.')
@click.option('--log', default='logs/server.log', help='log file for app.')
def server(host, port, log, workers):
    """Run the server with options."""
    options = {
        'bind': '{0}:{1}'.format(host, port),
        'workers': workers,
        'daemon': 'True',
        'errorlog': log
    }
    UVProvApplication(init_api(), options).run()


@cli.command('publisher')
def publisher():
    """Consuming some messages."""
    app_logger.info('UVProvenance publisher started')
    schedule.every(interval["timer"]).minutes.do(prov_job)
    while True:
        schedule.run_pending()
        time.sleep(1)


class UVProvApplication(gunicorn.app.base.BaseApplication):
    """Create Standalone Application uvprov-API."""

    def __init__(self, app, options=None):
        """The init."""
        self.options = options or {}
        self.application = app
        super(UVProvApplication, self).__init__()

    def load_config(self):
        """Load configuration."""
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        """Load configuration."""
        return self.application


# Unless really needed to scale use this function. Otherwise 2 workers suffice.
def number_of_workers():
    """Establish the numberb or workers based on cpu_count."""
    return (multiprocessing.cpu_count() * 2) + 1


def main():
    """Main function."""
    cli()


if __name__ == '__main__':
    main()
