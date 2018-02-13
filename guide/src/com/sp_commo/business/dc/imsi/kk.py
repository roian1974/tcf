import chardet


euc_data = '아름다운 한글'.encode('utf-8')
print( euc_data )
print (chardet.detect (euc_data))
print( euc_data.decode('utf-8'))
