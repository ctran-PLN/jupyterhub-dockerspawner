import sqlalchemy
from sqlalchemy import create_engine
from cryptography.fernet import Fernet
import os
import json

admin_list=['ctran','jmehta']
class DbConnect:
    """
    Description: Base Database connection class for extension to ANP, PMI and PMT connections
                 Config -> DbConnect -> ANP_Access | PMI_Access | PMT_Access
    """
    def __init__(self):
        self.username = os.environ['JUPYTERHUB_USER']
        self.utype = 'Admin' if (self.username in admin_list) else 'Regular'
        self.permission = ['read', 'write'] if self.utype == 'Admin' else ['read']
        print('You are the %s user, you have %s permission.' % (self.utype, ', '.join(self.permission)))

    def _connect(self, creds):
        connection_string = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (creds)
        return create_engine(connection_string,
                             encoding='utf-8')

    def parse_encrypted(self, sourceDb: str):
        CONFIG_KEY='/etc/jupyter/config.key'
        CONFIG_PATH= '/etc/jupyter/config_encrypted.json'
        with open(CONFIG_KEY, 'rb') as fr:
            crypto = Fernet(fr.read())
        with open(CONFIG_PATH, 'rb') as fr:
            data=json.loads(crypto.decrypt(fr.read()))
        return data[sourceDb]

    def map_to_creds(self, sourceDb: str) -> tuple:
        data=self.parse_encrypted(sourceDb)
        if sourceDb == 'pmi':
            host= 'CLOUDSQL_HOST' if self.utype == 'Admin' else 'CLOUDSQL_HOST_READ'
            return (data['CLOUDSQL_USER'],
                    data['CLOUDSQL_PASSWORD'],
                    data[host],
                    data['CLOUDSQL_PORT'],
                    data['CLOUDSQL_DB_NAME'])

        if sourceDb == 'pmi-prd':
            return (data['PMI_USER'],
                    data['PMI_PASSWORD'],
                    data['PMI_SQL_HOST'],
                    data['PMI_SQL_PORT'],
                    data['PMI_SQL_DB_NAME'])

        if sourceDb == 'pmt':
            return (data['PMT_USER'],
                    data['PMT_PASSWORD'],
                    data['PMT_SQL_HOST'],
                    data['PMT_SQL_PORT'],
                    data['PMT_SQL_COMM_DB_NAME'])

    def execute(self, query: str):
        conn=self.connect()
        with conn.begin() as conn:
            # begin() will invoke commit() or rollback()
            return conn.execute(query)
        # print('Check if connection closed:', conn.closed)

    def connect(self) -> sqlalchemy.engine.base.Engine:
        if self.utype == 'Admin':
            print('You are responsible for closing connections after query.')
            creds=self.map_to_creds(self.sourceDb)
            return self._connect(creds)

class ANP_agent(DbConnect):
    def __init__(self):
        # add super() to inherit all methods
        super().__init__()
        self.sourceDb='anp'

class PMI_agent(DbConnect):
    def __init__(self):
        # add super() to inherit all methods
        super().__init__()
        self.sourceDb='pmi'

class PMT_agent(DbConnect):
    def __init__(self):
        # add super() to inherit all methods
        super().__init__()
        self.sourceDb='pmt'
