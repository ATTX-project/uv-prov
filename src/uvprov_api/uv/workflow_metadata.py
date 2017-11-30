import xmltodict
from HTMLParser import HTMLParser
from uvprov_api.utils.logs import app_logger
from uvprov_api.utils.db import connect_DB, empty_workflows_DB
from uvprov_api.uv.activity_metadata import determine_status

artifact_id = 'UnifiedViews'  # Define the ETL agent
agent_role = 'ETL'  # Define Agent type


class WorkflowGraph(object):
    """Create WorkflowGraph class."""

    @classmethod
    def workflow(cls):
        """Build workflow graph with associated information."""
        workflow_list = []

        db_cursor = connect_DB()

        # test_workflows = cls.fetch_workflows(db_cursor, workflow_list, modifiedSince)
        # if test_workflows == "No workflows":
        #     db_cursor.connection.close()
        #     return workflow_list
        # else:
        #    cls.fetch_steps_sequence(db_cursor, workflow_graph)
        cls.fetch_steps(db_cursor, workflow_list)
        db_cursor.connection.close()
        return workflow_list

    @staticmethod
    def fetch_steps(db_cursor, workflow_list):
        """Create Steps ID and description."""
        # Get steps information
        db_cursor.execute("""
        SELECT dpu_instance.id AS 'stepId', dpu_instance.name AS 'stepTitle',
        dpu_instance.description AS 'description',
        dpu_template.name AS 'templateName',
        dpu_instance.configuration AS 'configuration',
        ppl_model.id AS 'workflowId',
        ppl_model.description AS 'description',
        ppl_model.name AS 'workflowTitle',
        ppl_model.visibility AS 'visibility',
        exec_pipeline.id AS 'activityId',
        exec_pipeline.status AS 'status'
        FROM exec_pipeline, ppl_model, dpu_template, dpu_instance, ppl_node,ppl_graph
        WHERE ppl_node.instance_id=dpu_instance.id AND
        ppl_node.graph_id = ppl_graph.id AND
        ppl_graph.pipeline_id = ppl_model.id AND
        dpu_instance.dpu_id = dpu_template.id AND
        exec_pipeline.pipeline_id = ppl_model.id
        """)

        result_set = db_cursor.fetchall()

        for row in result_set:
            workflow_graph = dict()
            workflow_graph["provenance"] = dict()
            workflow_graph["payload"] = dict()
            workflow_graph["provenance"]["agent"] = dict()
            workflow_graph["provenance"]["agent"]["ID"] = artifact_id
            workflow_graph["provenance"]["agent"]["role"] = agent_role

            graph = workflow_graph["provenance"]
            graph["context"] = dict()
            graph["context"]["activityID"] = str(row['activityId'])
            graph["context"]["workflowID"] = str(row['workflowId'])
            graph["context"]["stepID"] = str(row['stepId'])

            graph["activity"] = dict()
            graph["activity"]["status"] = determine_status(row['status'])
            graph["activity"]["configuration"] = parse_config(row['configuration'])
            graph["activity"]["type"] = "StepExecution"
            graph["activity"]["title"] = str(row["stepTitle"])

            app_logger.info('Construct provenance information for Step{0}.' .format(row['stepId']))

            workflow_list.append(workflow_graph)
        # return graph

    # @staticmethod
    # def fetch_steps_sequence(db_cursor, graph):
    #     """Create Steps sequence."""
    #     # Get steps linkage
    #     db_cursor.execute("""
    #     SELECT
    #       FromStep.instance_id AS 'fromStep',
    #       ToStep.instance_id AS 'toStep'
    #     FROM ppl_edge
    #     INNER JOIN ppl_node AS FromStep
    #       ON FromStep.id=ppl_edge.node_from_id
    #     INNER JOIN ppl_node AS ToStep
    #       ON ToStep.id=ppl_edge.node_to_id
    #     """)
    #
    #     result_set = db_cursor.fetchall()
    #
    #     for row in result_set:
    #         graph.add((URIRef("{0}step{1}".format(ATTXBase, row['fromStep'])), PWO.hasNextStep, URIRef("{0}step{1}".format(ATTXBase, row['toStep']))))
    #         app_logger.info('Fetch steps sequence between steps Step{0} and Step{1}.'.format(row['fromStep'], row['toStep']))
    #     return graph


def parse_config(config):
    """Parse metadata specific configuration."""
    data = ''
    try:
        soup = xmltodict.parse(config)
        base = soup["object-stream"]["MasterConfigObject"]["configurations"]["entry"]
        if len(base) is 1:
            data = HTMLParser().unescape(str(base["string"][1]))
        else:
            app_logger.info('Config information cannot be extracted.')
        return data
    except Exception as error:
        app_logger.error('Something is wrong: {0}'.format(error))


def workflow_get_output():
    """Construct the Ouput for the Get request."""
    data = WorkflowGraph()
    workflow_graph = data.workflow()
    if len(workflow_graph) > 0:
        result = workflow_graph
    elif len(workflow_graph) == 0:
        if empty_workflows_DB() == 0:
            result = []
        else:
            result = None
    app_logger.info('Constructed Output for UnifiedViews Workflow metadata enrichment finalized.')
    return result
