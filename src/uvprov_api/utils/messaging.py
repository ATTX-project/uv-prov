import json
from amqpstorm import Connection
from amqpstorm import Message
from uvprov_api.utils.logs import app_logger
from uvprov_api.uv.activity_metadata import activity_get_output
from uvprov_api.uv.workflow_metadata import workflow_get_output
from uvprov_api.utils.broker import broker


class Publisher(object):
    """Provenance message pubblisher."""

    def __init__(self, hostname='127.0.0.1',
                 username='guest', password='guest',
                 queue='base.queue'):
        """Consumer init function."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.queue = queue

    def push(self, message):
        """Push message to message inbox."""
        with Connection(self.hostname, self.username, self.password) as connection:
            with connection.channel() as channel:
                channel.queue.declare(self.queue)
                properties = {
                    'content_type': 'application/json'
                }
                message = Message.create(channel, message, properties)
                message.publish(self.queue)
                app_logger.info('Pushed message: {0}.'.format(message))


def prov_job():
    """Update with latest provenance."""
    try:
        activity_data = activity_get_output()
        workflow_data = workflow_get_output()
        PUBLISHER = Publisher(broker['host'], broker['user'], broker['pass'], broker['queue'])
        PUBLISHER.push(json.dumps(activity_data))
        PUBLISHER.push(json.dumps(workflow_data))
        app_logger.info('UV Provenance job executed.')
    except Exception as error:
        app_logger.error('Something with executing the prov_job: {0}'.format(error))
        raise error
