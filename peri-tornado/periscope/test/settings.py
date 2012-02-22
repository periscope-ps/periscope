######################################################################
# Mongo Database settings for unit testing
######################################################################
DB_NAME = "periscope_test"
DB_HOST = "127.0.0.1"
DB_PORT = 27017

# Asyncmongo specific connection configurations
ASYNC_DB = {
    'pool_id': DB_HOST + "_pool",
    'host': DB_HOST,
    'port': DB_PORT,
    'mincached': 1,
    'maxcached': 10,
    'maxconnections': 50,
    'dbname': DB_NAME,
}

# Pymonog specific connection configurations
SYNC_DB = {
    'host': DB_HOST,
    'port': DB_PORT,
}
