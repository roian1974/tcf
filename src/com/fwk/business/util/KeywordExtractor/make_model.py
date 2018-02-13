#TODO 검색 결과 파일 한개 파일에 모으기
#TODO 1. 디렉토리 파일명 리스트 담기
#TODO 2. 회사별로 파일 읽기
#TODO 3. 회사별로 파일에 쓰기
#TODO 4. randum access 방식으로 마지막에 추가하기

#TODO 5. DBMS에 넣기

import sys
import os
import yaml
import time
import glob
import codecs
import json
import csv
import pandas as pd

# from konlpy.tag import Twitter
from src.com.fwk.business.util.KeywordExtractor.customized_konlpy.ckonlpy.tag import Twitter
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

current_directory = os.getcwd() #실행 파일이 위치한 디렉토리
current_file = os.path.realpath(__file__) #실행 파일명
env = None

g_dir_name=''
g_keyword_file=''
g_model_file=''

def load_environment():
    """
    환경을 설정 파일 로드한다.
    :return:
    """
    environment = yaml.load(codecs.open("C:\jDev\MyWorks\PycharmProjects\Roian\src\com\\fwk\\business\\util\KeywordExtractor\env.yml", "r", "utf-8"))['running_env']

    return yaml.load(codecs.open("C:\jDev\MyWorks\PycharmProjects\Roian\src\com\\fwk\\business\\util\KeywordExtractor\config\configuration.yml", "r", "utf-8"))[environment]


def search_full_path(dir_name):
    """
    지정된 경로의 json파일 목록을 반환하낟.
    :param dir_name:
    :return:
    """
    tmp_list = [g for g in glob.glob(dir_name + "/*.json")]
    return sorted(tmp_list, reverse=False)





def make_model():
    """
    die
    기업별로 합쳐진 json 파일을 읽어 엑셀 파일로 변환한다.
    :param file_names:
    :return:
    """
    # full_path_csv_dir = "{0}tsv/".format(dir_name)
    global  g_dir_name
    full_path_csv_dir = "{0}tsv\\".format(g_dir_name)
    if not os.path.exists(full_path_csv_dir):
        raise Exception("source directory not found")

    # if not os.path.exists("{0}excel".format(dir_name)):
    if not os.path.exists("{0}excel".format(g_dir_name)):
        os.mkdir("{0}excel".format(g_dir_name))

    file_names = [g.split('\\')[-1] for g in glob.glob(full_path_csv_dir + "*.csv")]
    # del file_names[1:]
    twitter = Twitter()

    try:
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
            for i in range(0,content_titles.count()):
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

            global g_keyword_file
            print("----keywordfile,", g_keyword_file)
            if 0 == file_names.index(file_name):
                with open(g_keyword_file, 'w', encoding='utf-8') as fp:
                    fp.write("\n".join(results))
            else:
                with open(g_keyword_file, 'a', encoding='utf-8') as fp:
                    fp.write("\n".join(results))

        data = LineSentence(g_keyword_file)
        model = Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)

        global g_model_file
        model.save(g_model_file)

        # 모델 로딩
        try:
            model = Word2Vec.load(g_model_file)
        except:
            print("해당하는 모델파일이 없습니다.")

        # 키워드 추출
        try:
            print(model.most_similar(positive=['발주'], topn=50))
            print(model.similarity('부도', '자금난'))
        except:
            print("해당하는 키워드가 없습니다.")

    except:
        raise Exception("")

def main() :
    env = load_environment() #환경변수 로딩
    # dir_name = env['location']['output_normal'] # 정상차주 디렉토리 얻어오기
    global  g_dir_name
    g_dir_name = dir_name = env['location']['output_bankruptcy']  # 부도차주 디렉토리 얻어오기
    print(g_dir_name,'---3333--',dir_name)

    full_path_list = search_full_path(dir_name) #디렉토리내 파일목록 조회
    global  g_keyword_file

    g_keyword_file = keyword_file = env['file_name']['keyword_list']
    global g_model_file
    g_model_file = model_file = env['file_name']['keyword_model']

    print(full_path_list,keyword_file,model_file)

    #모델 생성
    make_model()

if __name__ == "__main__":
    env = load_environment() #환경변수 로딩
    # dir_name = env['location']['output_normal'] # 정상차주 디렉토리 얻어오기
    dir_name = env['location']['output_bankruptcy']  # 부도차주 디렉토리 얻어오기
    full_path_list = search_full_path(dir_name) #디렉토리내 파일목록 조회
    keyword_file = env['file_name']['keyword_list']
    model_file = env['file_name']['keyword_model']


    #모델 생성
    make_model()