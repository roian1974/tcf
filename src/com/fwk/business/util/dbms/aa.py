PATH = "/tmp"

class DB(object):
  def __init__(self):
    connected = False
    while not connected:
      try:
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "pool1",
                                                          **config.dbconfig)
        self.__cnx = cnxpool.get_connection()
      except mysql.connector.errors.PoolError:
        print("Sleeping.. (Pool Error)")
        sleep(5)
      except mysql.connector.errors.DatabaseError:
        print("Sleeping.. (Database Error)")
        sleep(5)

    self.__cur = self.__cnx.cursor(cursor_class=MySQLCursorDict)

  def execute(self, query):
    return self.__cur.execute(query)

def isValidFile(self, name):
  return True

def readfile(self, fname):
  d = DB()
  d.execute("""INSERT INTO users (first_name) VALUES ('michael')""")

def main():
  queue = multiprocessing.Queue()
  pool = multiprocessing.Pool(None, init, [queue])
  for dirpath, dirnames, filenames in os.walk(PATH):

    full_path_fnames = map(lambda fn: os.path.join(dirpath, fn),
                           filenames)
    full_path_fnames = filter(is_valid_file, full_path_fnames)
    pool.map(readFile, full_path_fnames)

if __name__ == '__main__':
  sys.exit(main())