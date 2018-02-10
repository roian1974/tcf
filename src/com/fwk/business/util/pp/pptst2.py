import pymysql
import sys
import pp


def fet(n):
    conn = pymysql.connect(host='192.168.219.153', port=3306, user='root', passwd='root', db='test', charset='utf8',
                           autocommit=True)
    cur = conn.cursor()
    sql = "select * from test where CD="
    sql += n
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
job2 = job_server.submit(fet, ('015760',), (), ("pymysql",))
job3 = job_server.submit(fet, ('015760',), (), ("pymysql",))
job4 = job_server.submit(fet, ('051910',), (), ("pymysql",))

result1 = job1()
result2 = job2()
result3 = job3()
result4 = job4()

print("result : %s" % result1)
print("result : %s" % result2)
print("result : %s" % result3)
print("result : %s" % result4)

job_server.print_stats()

# 출처: http: // adbancedteam.tistory.com / 77?category = 943769[aDBancedTeam]