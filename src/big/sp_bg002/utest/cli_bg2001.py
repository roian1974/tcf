from src.big.sp_bg002.transfer.big2001cdto import BIG2001CDTO
from src.com.fwk.business.tcf import tcf_sp_bg001

"""
word2vec  관련 내용정리
2018년 2월 14일
"""
servicename='sp_bg002'
hostprog='BIG2001'
userid='user01'
tpfq=200
cdto = BIG2001CDTO(servicename,hostprog,userid,tpfq)

# ----- make model
# cdto.indata['env_filename'] = "C:\jDev\MyWorks\PycharmProjects\Roian\src\com\\fwk\\business\\util\KeywordExtractor\env.yml"
# cdto.indata['config_filename'] ="C:\jDev\MyWorks\PycharmProjects\Roian\src\com\\fwk\\business\\util\KeywordExtractor\config\configuration.yml"
# cdto.indata['domain_function'] = "makeModel"
#
# argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
# s_out = tcf_sp_bg001.main(argv)
#
# cdto = s_out['outdata'][0]
# print( cdto.outdata['out'] )

# ----- predict model
cdto.indata['env_filename'] = "C:\jDev\MyWorks\PycharmProjects\Roian\src\\big\sp_bg002\\utest\word2vec\env.yml"
cdto.indata['config_filename'] ="C:\jDev\MyWorks\PycharmProjects\Roian\src\\big\sp_bg002\\utest\word2vec\config\configuration.yml"
cdto.indata['model_similarity_word'] = ['부도','자금난']
cdto.indata['model_most_similar_word'] = ['발주']
cdto.indata['domain_function'] = "predictModel"

argv=['tcf_sp_bg001.py', servicename, hostprog, cdto ]
s_out = tcf_sp_bg001.main(argv)

cdto = s_out['outdata'][0]
print( cdto.indata['model_similarity_word'], "-model_similarity:" ,cdto.outdata['model_similarity'] )
print( cdto.indata['model_most_similar_word'],'-model_most_similar:', cdto.outdata['model_most_similar'] )
