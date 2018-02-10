import pymysql
import sys
import pp

# http://adbancedteam.tistory.com/77?category=943769

def fet(n):
    conn = pymysql.connect(host='192.168.219.153', port=3306, user='root', passwd='root', db='test', charset='utf8',
                           autocommit=True)
    cur = conn.cursor()
    sql = "select * from test”
    # sql += n
    return cur.execute(sql)


ppservers = ()

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print("Starting pp with %s workers" % job_server.get_ncpus())

job1 = job_server.submit(fet, ('005380',), (), ("pymysql",))

result = job1()

print("result : %s" % result)

job_server.print_stats()

