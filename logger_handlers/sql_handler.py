from logging import StreamHandler
import pyodbc
from logger_handlers import repository

class SQLHandler(StreamHandler):
    def __init__(self, sql_settings):
        StreamHandler.__init__(self)
        self.sql_connection = sql_settings
        self.connect()
        self.validate_logging_table()

    def connect(self):
        """ connects to databases """
        if 'trusted_connection' in self.sql_connection:
            self.sql = pyodbc.connect(
                r'Driver=' + self.sql_connection['driver'] + ';'
                r'Server=' + self.sql_connection['host'] + ';'
                r'Database=' + self.sql_connection['db'] + ';'
                r'Trusted_Connection=yes;'
                r'MARS_Connection=Yes')
        else:
            self.sql = pyodbc.connect(
                r'Driver=' + self.sql_connection['driver'] + ';'
                r'Server=' + self.sql_connection['host'] + ';'
                r'Database=' + self.sql_connection['db'] + ';'
                r'Uid=' + self.sql_connection['user'] + ';'
                r'Pwd=' + self.sql_connection['password'] + ';'
                r'MARS_Connection=Yes')

    def close(self):
        self.sql.close()

    def emit(self, record):
        msg = self.format(record)
        sql = 'INSERT INTO [etl].[log] ([Thread], [Level], [Logger], [Message]) VALUES (?,?,?,?)'
        cursor = self.sql.cursor()
        cursor.execute(sql, record.threadName, record.levelname, record.processName, record.message)
        cursor.commit()

    def dump(self, record):
        print('args: ', record.args)
        #print('asctime: ', record.asctime)
        print('created: ', record.created)
        print('exc_info: ', record.exc_info)
        print('filename: ', record.filename)
        print('funcName: ', record.funcName)
        print('levelname: ', record.levelname)
        print('levelno: ', record.levelno)
        print('lineno: ', record.lineno)
        print('module: ', record.module)
        print('msecs: ', record.msecs)
        print('message: ', record.message)
        print('msg: ', record.msg)
        print('name: ', record.name)
        print('pathname: ', record.pathname)
        print('process: ', record.process)
        print('processName: ', record.processName)
        print('relativeCreated: ', record.relativeCreated)
        print('stack_info: ', record.stack_info)
        print('thread: ', record.thread)
        print('threadName: ', record.threadName)

    def validate_logging_table(self):

        sql = 'SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = \'Log\''
        cursor = self.sql.cursor()
        exists = cursor.execute(sql).fetchone()

        if not exists:
            print('logger_handlers.sql_handler - INFO - Log table does not exist')
            repository.execute_multi_commands(
                cursor,
                repository.get_query(repository.QUERY_CREATE_LOG_TABLE)
            )
            print('logger_handlers.sql_handler - INFO - Log table created')
