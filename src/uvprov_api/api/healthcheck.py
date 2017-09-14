import falcon
from uvprov_api.utils.logs import app_logger
from uvprov_api.utils.messaging import prov_job


class HealthCheck(object):
    """Create HealthCheck class."""

    def on_get(self, req, resp):
        """Respond on GET request to map endpoint."""
        resp.status = falcon.HTTP_200  # implement 202 when it is needed
        app_logger.info('Finished operations on /health GET Request.')


class RunProv(object):
    """Run prov job."""

    def on_get(self, req, resp):
        """Respond on GET request to map endpoint."""
        prov_job()
        resp.status = falcon.HTTP_202  # implement 202 when it is needed
        app_logger.info('run prov job instead of waiting for scheduled run.')
