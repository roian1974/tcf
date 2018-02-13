import tailer
import os
import shutil

# fullpath = '/home/aaa/bbb/ccc.txt'
def split_filename(fullpath) :
	return os.path.basename(fullpath)  # 'ccc.txt'

def split_dirname(fullpath):
	return print(os.path.dirname(fullpath)  # '/home/aaa/bbb'

#def split_2p2(fullpath) :
#	return os.path.split(fullpath)  # ('/home/aaa/bbb', 'ccc.txt')

#def split_ext(fullpath) :
#	return os.path.splitext(fullpath) # ('/home/aaa/bbb/ccc', '.txt')

#def exist_file(fullpath) :
#	return os.path.exists(fullpath)

#def cp_file(o_file , t_file) :
#	shutil.copy('a.txt', 'a-copied.txt')

#def move_file(o_file, t_file) :
#	shutil.move(o_file, t_file)

# def delete_file(file) :
# 	os.remove(file)
#
# def copy_dir(o_dir, t_dir) :
# 	shutil.copytree(o_dir,t_dir)
#
# def move_dir(o_dir, t_dir) :
# 	shutil.move(o_dir, t_dir)
#
# def delete_dir(dir) :
# 	shutil.rmtree(dir)
#
# def search_dir(dir) :
# 	for filename in os.listdir(dir):
# 		fullpath = os.path.join(dir, filename)
# 		if (os.path.islink(fullpath)):
# 			print('link: %s' % fullpath)
# 		elif (os.path.isfile(fullpath)):
# 			print('file: %s' % fullpath)
# 		elif (os.path.isdir(fullpath)):
# 			print('dir: %s' % fullpath)
#
# def search_subdir(dir) :
# 	for (path, dirs, files) in os.walk(dir):
# 		for f in files:
# 			fullpath = os.path.join(path, f)
# 			print(fullpath)

# # def file_tailer(filename,linecount) :
# # 	lines = tailer.tail(open(filename), linecount)
# # 	return lines
# #
# def file_write(filename, text) :
#     f = open(filename, 'w')
#     f.write(text + '\n')
#     f.close()
#
# def file_write_02(filename,text) :
#     with open(filename, 'w') as f:
#         f.write(text + '\n')
#
# def file_append(filename,text) :
#     with open('hello.txt', 'a') as f:
#         f.write(text + '\n')
#
# def file_readline(filename) :
#     with open(filename, 'r') as f:
#         for line in f.readlines():
#             print(line)
#
# def file_readtotal(filename) :
#     with open(filename, 'r') as f:
#         content = f.read()
#         print(content)
#
# def tail_file(filename, line) :
#     lines = tailer.tail(open('very_large_file.txt'), line)
#     print(lines)

#--------------------------------------------------

# def printRecord(j_response):
#     sentiment_targets_text1 = j_response['sentiment']['targets'][0]['text'] # samsung
#     sentiment_targets_score1 = j_response['sentiment']['targets'][0]['score']  # 0.27
#     sentiment_targets_label1 = j_response['sentiment']['targets'][0]['label']  # positive
#
#     sentiment_targets_text2 = j_response['sentiment']['targets'][1]['text'] # sk
#     sentiment_targets_score2 = j_response['sentiment']['targets'][1]['score']  # 0.3
#     sentiment_targets_label2 = j_response['sentiment']['targets'][1]['label']  # positive
#
#     sentiment_document_score = j_response['sentiment']['document']['score']
#     sentiment_document_label = j_response['sentiment']['document']['label']
#
#     print("===========================================================================================")
#     print("%-10.10s %-10.10s %-10.10s %-10.10s %-8.8s %-8.8s %-8.8s" % ("문서ID", "기사스코어", "레이블", "모델ID", "사용여부", "등록일자", "수정일자"))
#     print("===========================================================================================")
#     print("%-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s" % ("00001", sentiment_document_score, sentiment_document_label, "2017-12-31", "N", "20180105","20180105" ))
#
#     print("===========================================================================================")
#     print("%-10.10s %-10.10s %-10.10s %-10.10s %-8.8s %-8.8s %-8.8s" % ("문서ID", "기업명", "기사스코어", "레이블", "사용여부", "등록일자", "수정일자"))
#     print("===========================================================================================")
#
#     for dicitem in j_response['sentiment']['targets']:
#         print("%-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s" % ("00001", dicitem['text'], dicitem['score'], dicitem['label'], "Y", "20180105","20180105" ))


# def imsiResponse():
#     j_response = {
#         "usage": {
#             "text_units": 1, "text_characters": 1188, "features": 1
#         },
#         "sentiment": {
#             "targets": [  { "text": "samsung", "score": 0.279964, "label": "positive" } ,
#                            { "text": "sk",       "score": 0.312345,  "label": "positive" }   ],
#             "document": { "score": 0.127034, "label": "positive"  }
#         },
#         "retrieved_url": "https://www.wsj.com/news/markets",
#         "language": "en"
#     }
#
#     jsentiment  = j_response['sentiment']
#     jtargets    = j_response['sentiment']['targets']
#
#     printRecord(j_response)
#
#     return j_response

print()
