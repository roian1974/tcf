from bottle import route, run, template
from src.com.fwk.business.util.dbms import comdbutil

# HOST = '169.56.68.67'
HOST ='localhost'
PORT = 8080


# CREATE TABLE `o2`.`bucket` (
#   `id` INT NOT NULL,
#   `wish` VARCHAR(45) NULL,
#   `status` VARCHAR(45) NULL,
#   PRIMARY KEY (`id`));

@route('/bucket')
def bucket_list():
    conn = comdbutil.dbinit('localhost', 'root', '1234qwer', 'o2')

    # sql = "SELECT id, wish, status FROM bucket WHERE status LIKE '0' OR '1'"
    sql = "SELECT id, wish, status FROM bucket"

    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()

    return template('wish_tbl', rows=result)

run(host=HOST, port=PORT, debug=True)