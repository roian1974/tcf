
def tprollback() :
    try :
        print('1111111111111')
        raise Exception('tprollback--')
        print('2222222222222')
        print('333333333333333')
    except Exception as err:
        print('▲tprollback()-ERR:', str(err))
        return False
    else:
        print('▲tprollback()-성공:')
    finally:
        return True

tprollback()