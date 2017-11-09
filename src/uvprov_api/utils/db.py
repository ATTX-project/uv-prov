import pymysql as mysql
from uvprov_api.utils.logs import app_logger
from os import environ

database = {'host': environ['DBHOST'] if 'DBHOST' in environ else "localhost",
            'user': environ['DBUSER'] if 'DBUSER' in environ else "unified_views",
            'pass': environ['DBKEY'] if 'DBKEY' in environ else "s00pers3cur3",
            'db': environ['DBASE'] if 'DBASE' in environ else "unified_views"}


def connect_DB(db_conf=None):
    """Connect to DB by parsing configuration."""
    try:
        conn = mysql.connect(
            host=database['host'],
            port=3306,
            user=database['user'],
            passwd=database['pass'],
            db=database['db'],
            charset='utf8')
        app_logger.info('Connecting to database.')
        # Default curosr is DictCursor
        cursor = conn.cursor(mysql.cursors.DictCursor)
        return cursor
    except Exception as error:
        app_logger.error('Connection Failed!\
            \nError Code is {0};\
            \nError Content is {1};'.format(error.args[0], error.args[1]))
        return error


def empty_workflows_DB():
    """Check if the DB is empty."""
    db_cursor = connect_DB()
    db_cursor.execute("""SELECT EXISTS(SELECT 1 FROM ppl_model) as 'count'""")
    result = db_cursor.fetchone()
    return result['count']


def empty_activities_DB():
    """Check if the DB is empty."""
    db_cursor = connect_DB()
    db_cursor.execute("""SELECT EXISTS(SELECT 1 FROM exec_pipeline) as 'count'""")
    result = db_cursor.fetchone()
    return result['count']
