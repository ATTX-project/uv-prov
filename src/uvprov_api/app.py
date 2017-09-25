import falcon
from uvprov_api.api.activity import Activity
from uvprov_api.api.workflow import Workflow
from uvprov_api.api.healthcheck import HealthCheck, RunProv
from uvprov_api.utils.logs import main_logger

api_version = "0.2"  # TO DO: Figure out a better way to do versioning


def create():
    """Create the API endpoint."""
    do_activity = Activity()
    do_workflow = Workflow()

    uvprov_api = falcon.API()
    uvprov_api.add_route('/health', HealthCheck())
    uvprov_api.add_route('/provjob', RunProv())
    uvprov_api.add_route('/%s/activity' % (api_version), do_activity)
    uvprov_api.add_route('/%s/workflow' % (api_version), do_workflow)
    main_logger.info('UVProvenance-API endpoint is running.')
    return uvprov_api


# if __name__ == '__main__':
#     create()
