import os
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.dbms import comdbutil
from src.com.sp_comrc.business.pc.mod import com9001

from src.com.fwk.business.tcf import tcf_sp_comrc


def subprocessor_ty1(com1100CDTO) :
    rtn = True
    try:
        print('info'+"subprocessor() start ")

        r2ow = com1100CDTO[0]
        queue = com1100CDTO[1]
        # print('----------com1100CDTO[0]----',com1100CDTO[0])
        argv = ['tcf_sp_comrc', 'sp_comrc', 'COM9001', com1100CDTO[0] ]
        tcf_sp_comrc.main(argv)

    except Exception as err:
        comlogging.logger.error( 'subprocessor-'+ str(err))
        include.setErr('subprocessor', 'subprocessor' + str(err))
    else:
        print('info'+ 'subprocessor-성공')
    finally:

        queue.put(str(os.getpid()) + ' job end')

        if include.isError() == False :
            return True
        else :
            return False

def subprocessor_ty2(r2ow,queue) :
    rtn = True
    try:
        print('info'+"################################################### Subprocessor() start ")

        argv = ['tcf_sp_comrc', 'sp_comrc', 'COM9001', r2ow ]
        tcf_sp_comrc.main(argv)

    except Exception as err:
        comlogging.logger.error( 'subprocessor-'+ str(err))
        include.setErr('ESUB001', 'subprocessor' + str(err))
    else:
        print('info'+ 'subprocessor-성공')
    finally:


        print('info'+"################################################## Subprocessor() end ")
        queue.put(str(os.getpid()) + ' job end')
        if include.isError() == False :
            return True
        else :
            return False

def subprocessor_ty3(r2ow,queue) :
    rtn = True
    try:
        print('>>>>>>>>>>>>>>',r2ow)
        print('llllllllll',queue)
        print('info'+"################################################### Subprocessor() start ")

        argv = ['tcf_sp_commo', 'sp_comrc', 'COM9001', r2ow ]
        tcf_sp_comrc.main(argv)

    except Exception as err:
        comlogging.logger.error( 'subprocessor-'+ str(err))
        include.setErr('ESUB001', 'subprocessor' + str(err))
    else:
        print('info'+ 'subprocessor-성공')
    finally:


        print('info'+"################################################## Subprocessor() end ")
        queue.put(str(os.getpid()) + ' job end')
        if include.isError() == False :
            return True
        else :
            return False

def subthread_ty2(r2ow,queue) :
    rtn = True
    try:
        print('info'+"################################################### Subprocessor() start ")

        argv = ['tcf_sp_commo', 'sp_comrc', 'COM9001', r2ow ]
        tcf_sp_comrc.main(argv)

    except Exception as err:
        comlogging.logger.error( 'subprocessor-'+ str(err))
        include.setErr('ESUB001', 'subprocessor' + str(err))
    else:
        print('info'+ 'subprocessor-성공')
    finally:

        queue.put(str(os.getpid()) + ' job end')
        print('info'+"################################################## Subprocessor() end ")
        if include.isError() == False :
            return True
        else :
            return False





def subprocessor_function (r2ow,queue) :

    try :
        rcnt = False
        txflag = True

        tpsutil.tpenv()

        rtn = tpsutil.tpbegin()
        if rtn == False:
            queue.put(str(os.getpid()) + ' job end')
            print('tpbegin fail-', os.getpid())
            raise Exception('tpbegin error')

        rtn = tpsutil.tpsinit_processor()
        if rtn == False:
            queue.put(str(os.getpid()) + ' job end')
            print('tpsinit_processor fail-', os.getpid())
            raise Exception('tpsinit_processor error')

        for r3ow in r2ow:
            rcnt += 1
            print("--nlu call--", rcnt, "-------------------------------", r3ow[0], os.getpid())

            dic_response_s = com9001.nlu_sentiment(r3ow)
            if dic_response_s == False :
                continue

            dic_response_e = com9001.nlu_entity(r3ow)
            if dic_response_e == False :
                continue

            print("--save data--", rcnt, "-------------------------------", r3ow[0], os.getpid())
            if com9001.result_processing_document(dic_response_s) == False :
                txflag = False
                break

            if  com9001.result_processing_entity(dic_response_e) == False :
                txflag = False
                print("#================================================",txflag)
                break

            tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
            if comdbutil.upsert("update_document_01", [], tup) == False:
                txflag = False
                break

    except Exception as err:
        print('▲subprocessor_function()-ERR:', str(err),os.getpid())
        txflag = False
        rtn = False
    else:
        print('▲subprocessor_function()-성공:',os.getpid())
        rtn = True
    finally:

        if txflag == True :
            tpsutil.tpcommit()
            print("tpcommit success -child")
        else:
            tpsutil.tprollback()
            print("tprollback success -child")

        queue.put(str(os.getpid()) + ' job end')

        return rtn





# cutting_rows 단위로 작업의 타스크를 나누어 리스트에 저장한다.
def divide_task(rows,cutting_rows) :

    flag = False
    n1rows = []
    n2rows = []

    for row in rows:
        doc_id = row[0]
        doc_content = row[1]
        if len(n2rows) <= cutting_rows :
            n2rows.append(row)
        if len(n2rows) == cutting_rows :
            n1rows.append(n2rows)
            n2rows = []

    n1rows.append(n2rows)

    return n1rows

#-----------------------------------------------------------------------------------------------------------------------

