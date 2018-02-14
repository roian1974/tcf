import sys, os, yaml, time,glob, codecs, json, csv
import pandas as pd
import time
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.info import include
from src.com.fwk.business.util.KeywordExtractor.customized_konlpy.ckonlpy.tag import Twitter
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def preAnalysis(big2001cdto) :
    try:
        rtn = True

        # 정상차주나 부도차주 파일이 있는 디렉토리 가져오기
        env = big2001cdto.ddto['envinfo']
        dir_name = env['location']['output_bankruptcy']
        normal_dir_name = env['location']['output_normal']

        # 전체 디렉토리정보를 들고온다
        tmp_list = [g for g in glob.glob(dir_name + "/*.json")]
        full_path_list = sorted(tmp_list, reverse=False)  # 디렉토리내 파일목록 조회

        keyword_file = env['file_name']['keyword_list']
        model_file = env['file_name']['keyword_model']

        print('---3333--', dir_name, full_path_list, tmp_list)

        big2001cdto.ddto['keyword_file'] = keyword_file
        big2001cdto.ddto['model_file'] = model_file
        big2001cdto.ddto['dir_name'] = dir_name
        big2001cdto.ddto['normal_dir_name'] = normal_dir_name

    except Exception as err:
        comlogging.logger.error('▲preAnalysis()-ERR:'+ str(err))
        include.setErr('EBIG005', 'preAnalysis 분석에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲preAnalysis()-성공:')
    finally:
        if rtn == True :
            return big2001cdto
        else :
            return False

def makeModel(big2001cdto) :
    try:
        rtn = True

        keyword_file = big2001cdto.ddto['keyword_file']
        model_file = big2001cdto.ddto['model_file']
        dir_name = big2001cdto.ddto['dir_name']
        normal_dir_name = big2001cdto.ddto['normal_dir_name']

        full_path_csv_dir = "{0}tsv\\".format(dir_name)
        if not os.path.exists(full_path_csv_dir):
            raise Exception("source directory not found")

        # if not os.path.exists("{0}excel".format(dir_name)):
        if not os.path.exists("{0}excel".format(dir_name)):
            os.mkdir("{0}excel".format(dir_name))

        file_names = [g.split('\\')[-1] for g in glob.glob(full_path_csv_dir + "*.csv")]
        # del file_names[1:]
        twitter = Twitter()

        for file_name in file_names:
            want = []
            for chunck in pd.read_csv(filepath_or_buffer=full_path_csv_dir + file_name, header=None, delimiter="\t"
                    , engine="python", index_col=None, encoding="utf-8", chunksize=50000, dtype="str"):
                want.append(chunck)

            df = pd.concat(want, ignore_index=True)

            company_name = df[5].str.strip()[0].replace('"', '')
            content_titles = df[8].str.strip()
            contens = df[9].str.strip()
            twitter.add_dictionary(company_name, 'Noun')

            content_list = []
            for i in range(0, content_titles.count()):
                content_list.append(company_name + " " + content_titles.values[i] + contens.values[i])

            # contens = pd.concat([content_titles,contens], ignore_index=True)
            results = []
            for content in content_list:
                lines = content.split("\n")
                for line in lines:
                    # malist = twitter.pos(line, norm=True, stem=True)
                    malist = twitter.pos(line)
                    r = []
                    for word in malist:
                        if not word[1] in ['Punctuation', 'Josa']:
                            r.append(word[0])

                    rl = (" ".join(r)).strip()

                    if rl:
                        results.append(rl)

            print("{0} done!!!!!".format(file_name))

            print("----keywordfile,", keyword_file)
            if 0 == file_names.index(file_name):
                with open(keyword_file, 'w', encoding='utf-8') as fp:
                    fp.write("\n".join(results))
            else:
                with open(keyword_file, 'a', encoding='utf-8') as fp:
                    fp.write("\n".join(results))

        data = LineSentence(keyword_file)
        model = Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)

        model.save(model_file)

    except Exception as err:
        comlogging.logger.error('▲makeModel()-ERR:'+ str(err))
        include.setErr('EBIG005', 'makeModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲makeModel()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False



def predictModel(big2001cdto) :
    try:
        rtn = True

        keyword_file = big2001cdto.ddto['keyword_file']
        model_file = big2001cdto.ddto['model_file']
        dir_name = big2001cdto.ddto['dir_name']
        normal_dir_name = big2001cdto.ddto['normal_dir_name']

        s_rr = big2001cdto.indata['model_similarity_word']
        word = big2001cdto.indata['model_most_similar_word']

        # 모델 로딩
        model = Word2Vec.load(model_file)

        print(model.most_similar(positive=word, topn=50))
        print(model.similarity(s_rr[0], s_rr[1]))

        big2001cdto.outdata['model_similarity'] = model.similarity(s_rr[0], s_rr[1])
        big2001cdto.outdata['model_most_similar'] = model.most_similar(positive=word, topn=50)

    except Exception as err:
        comlogging.logger.error('▲predictModel()-ERR:'+ str(err))
        include.setErr('EBIG005', 'predictModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲predictModel()-성공:')
    finally:
        if rtn == True :
            return big2001cdto
        else :
            return False


