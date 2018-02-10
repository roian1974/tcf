# INPUT - Combined_News_DJIA.csv
# OUTPUT - TEXT Preprocessing
#           - 형태소 분리(왓슨의 경우는 senmentic role통해) 및 조사제거 -> 불용어 처리(filter):도메인과 관련없는 단어제거 ->
#           - 절차
#              train.iloc :
#               대문자를 소문자로 변경하는 plain text 화 시킨다.
#
#               단어별 빈도수를 작성한다.
#
#   BASIC MODEL TRAINING AND TESTING : 모델(로직스틱회귀분석모델)을 위한 학습 데이타 준비
#    -

