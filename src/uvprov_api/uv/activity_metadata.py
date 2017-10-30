from datetime import datetime
from uvprov_api.utils.logs import app_logger
from uvprov_api.utils.db import connect_DB, empty_activities_DB

artifact_id = 'UnifiedViews'  # Define the ETL agent
agent_role = 'ETL'  # Define Agent type


def determine_status(status):
    """Naming convention for activity status."""
    return {
        '2': "failed",
        '4': "failed",
        '5': "success",
        '6': "warning",
    }[str(status)]


class ActivityGraph(object):
    """Create WorkflowGraph class."""

    @classmethod
    def activity(cls):
        """Build activity graph with associated information."""
        activity_list = []

        db_cursor = connect_DB()

        cls.fetch_activities(db_cursor, activity_list)
        # if test_activities == "No workflows":
        #     db_cursor.connection.close()
        #     return activity_list
        # else:
        #     # cls.fetch_metadata(db_cursor, activity_graph["provenance"], modifiedSince)
        #     db_cursor.connection.close()
        db_cursor.connection.close()
        return activity_list

    @staticmethod
    def fetch_activities(db_cursor, activity_list):
        """Create activity ID and description."""
        # Get general workflow information on the last executed workflow
        # Get based only on public workflows and successful pipeline execution
        db_cursor.execute("""
            SELECT exec_pipeline.id AS 'activityId',
            ppl_model.id AS 'workflowId',
            ppl_model.name AS 'title',
            exec_pipeline.t_start AS 'activityStart',
            exec_pipeline.t_end AS 'activityEnd',
            exec_pipeline.t_end AS 'lastChange',
            exec_pipeline.status AS 'status'
            FROM exec_pipeline, ppl_model
            WHERE exec_pipeline.pipeline_id = ppl_model.id
            ORDER BY ppl_model.id
        """)
        # replace last line above with one below if only latest result required
        #  ORDER BY ppl_model.last_change DESC LIMIT 1
        result_set = db_cursor.fetchall()

        if db_cursor.rowcount > 0:
            return ActivityGraph.construct_act_graph(activity_list, result_set)
        else:
            return "No activities"

    @staticmethod
    def construct_act_graph(activity_list, data_row):
        """Test to see if record has been modifed."""
        for row in data_row:

            activity_graph = dict()
            activity_graph["provenance"] = dict()
            activity_graph["payload"] = dict()
            activity_graph["provenance"]["agent"] = dict()
            activity_graph["provenance"]["agent"]["ID"] = artifact_id
            activity_graph["provenance"]["agent"]["role"] = agent_role

            graph = activity_graph["provenance"]

            graph["context"] = dict()
            graph["context"]["activityID"] = str(row['activityId'])
            graph["context"]["workflowID"] = str(row['workflowId'])

            graph["activity"] = dict()
            graph["activity"]["type"] = "WorkflowExecution"
            graph["activity"]["title"] = "{0} Activity{1}".format(row["title"], row['activityId'])
            graph["activity"]["status"] = determine_status(row['status'])
            start_time = datetime.strptime(str(row['activityStart']), '%Y-%m-%d %H:%M:%S')
            graph["activity"]["startTime"] = start_time.strftime('%Y-%m-%dT%H:%M:%S')
            end_time = datetime.strptime(str(row['activityEnd']), '%Y-%m-%d %H:%M:%S')
            graph["activity"]["endTime"] = end_time.strftime('%Y-%m-%dT%H:%M:%S')
            app_logger.info('Construct provenance information for Activity{0}.' .format(row['activityId']))
            activity_list.append(activity_graph)


def activity_get_output():
    """Construct the Ouput for the Get request."""
    data = ActivityGraph()
    activity_graph = data.activity()
    if len(activity_graph) > 0:
        result = activity_graph
    elif len(activity_graph) == 0:
        if empty_activities_DB() == 0:
            result = []
        else:
            result = None
    app_logger.info('Constructed Output for UnifiedViews Activity metadata enrichment finalized.')
    return result
