# -*- coding: utf-8 -*-
"""크몽_텍스트빈도.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1imRVJ1Eysz7KYBVWnVFlBNtxt10WhSA4

텍스타일 뉴스기사 빈도분석
"""

import os
import pandas as pd

# 파일이 저장된 디렉토리 경로
directory_path = '/content/drive/MyDrive/Colab Notebooks/textile/'

# 모든 파일의 데이터를 저장할 빈 데이터프레임 생성
all_data = pd.DataFrame()

# 디렉토리 내의 모든 Excel 파일을 반복하여 처리
for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)

        # Excel 파일을 데이터프레임으로 읽어오기
        data = pd.read_excel(file_path)

        # 현재 파일의 데이터를 기존 데이터프레임에 이어붙이기
        all_data = pd.concat([all_data, data], ignore_index=True)

all_data

!pip install wordcloud
!pip install konlpy

from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter

word_all = all_data[['title','contents']]

import re

def text_cleaning(text):
    if pd.isnull(text):
        return ""  # NaN이면 빈 문자열로 처리
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')    # ㅣ : 한글 ㅣ (이)
    result = hangul.sub('',text)
    return result

word_all['title'] = word_all['title'].apply(lambda x: text_cleaning(x))
word_all['contents'] = word_all['contents'].apply(lambda x: text_cleaning(x))

# konlpy의 형태소 분석기 모듈을 이용하여 단어를 추출하기

nouns_tagger = Okt()   # 명사 추출을 위한 형태소 분석기

# 각 피처마다 말뭉치를 생성
# df : 나무위키에서 수집한 텍스트 데이터 중 한글만 저장하고 있는 데이터프레임 객체
title_corpus = "".join(word_all['title'].tolist())
contents_corpus = "".join(word_all['contents'].tolist())

title_corpus
contents_corpus

concatenated_list = (title_corpus + ' '  + contents_corpus)

concatenated_list

nouns = nouns_tagger.nouns(concatenated_list)
nouns[:5]

count = Counter(nouns)

# x : 단어
# count[x] : 단어빈도수
remove_char_counter = Counter({x: count[x] for x in count if len(x) > 1 })  # 컴프리헨션 방식

!wget https://raw.githubusercontent.com/byungjooyoo/Dataset/main/korean_stopwords.txt
import re
stop_words=[]
with open("korean_stopwords.txt", 'r') as f:
    while True:
        line = f.readline().strip()
        stop_words.append(line)
        if not line: break
print(stop_words)

korean_stopwords = "korean_stopwords.txt"
with open(korean_stopwords, encoding='utf8') as f :
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

remove_char_counter = \
    Counter({x:remove_char_counter[x] for x in remove_char_counter if x not in stopwords})

remove_char_counter

tags = remove_char_counter.most_common(52)
tags

# 제거할 인덱스 리스트 (2와 18)
indices_to_remove = [12,33]

# 리스트 컴프리헨션을 사용하여 제거할 인덱스 제외
tags2 = [item for idx, item in enumerate(tags) if idx not in indices_to_remove]

tags2

!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 나눔 폰트 경로 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=font_path, size=10).get_name()

# 폰트 설정
plt.rc('font', family=font_name)

# WordCloud를 생성한다.
wc = WordCloud(font_path=font_path,background_color="white", max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tags))

plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.savefig('워드클라우드.jpg', dpi=3000, bbox_inches='tight')
plt.show()

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Colab에서 폰트 설정
#!apt-get -y install fonts-nanum
fontpath = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font = fm.FontProperties(fname=fontpath, size=10)

labels, values = zip(*tags2)

# 막대그래프로 나타내기 (30개만 표시)
plt.figure(figsize=(12, 8))
plt.bar(labels[:30], values[:30], color='skyblue')
plt.title('텍스타일')
plt.xlabel('Tag')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right', fontproperties=font)  # X 축 레이블 회전 및 정렬

plt.savefig('단어빈도수.jpg', dpi=1500, bbox_inches='tight')

plt.show()

textile = pd.DataFrame(tags2, columns=['labels', 'values'])

# CSV 파일로 저장 (파일 이름은 원하는 대로 변경 가능)
textile.to_csv('textile.csv', index=False, encoding='utf-8-sig')

"""지속가능성 뉴스기사 빈도분석"""

import os
import pandas as pd

# 파일이 저장된 디렉토리 경로
directory_path = '/content/drive/MyDrive/Colab Notebooks/sustainability/'

# 모든 파일의 데이터를 저장할 빈 데이터프레임 생성
all_data = pd.DataFrame()

# 디렉토리 내의 모든 Excel 파일을 반복하여 처리
for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)

        # Excel 파일을 데이터프레임으로 읽어오기
        data = pd.read_excel(file_path)

        # 현재 파일의 데이터를 기존 데이터프레임에 이어붙이기
        all_data = pd.concat([all_data, data], ignore_index=True)

all_data

from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter

word_all = all_data[['title','contents']]

import re

def text_cleaning(text):
    if pd.isnull(text):
        return ""  # NaN이면 빈 문자열로 처리
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')    # ㅣ : 한글 ㅣ (이)
    result = hangul.sub('',text)
    return result

word_all['title'] = word_all['title'].apply(lambda x: text_cleaning(x))
word_all['contents'] = word_all['contents'].apply(lambda x: text_cleaning(x))

# konlpy의 형태소 분석기 모듈을 이용하여 단어를 추출하기

nouns_tagger = Okt()   # 명사 추출을 위한 형태소 분석기

# 각 피처마다 말뭉치를 생성
# df : 나무위키에서 수집한 텍스트 데이터 중 한글만 저장하고 있는 데이터프레임 객체
title_corpus = "".join(word_all['title'].tolist())
contents_corpus = "".join(word_all['contents'].tolist())

title_corpus
contents_corpus

concatenated_list = (title_corpus + ' '  + contents_corpus)

concatenated_list

nouns = nouns_tagger.nouns(concatenated_list)
nouns[:5]

count = Counter(nouns)

# x : 단어
# count[x] : 단어빈도수
remove_char_counter = Counter({x: count[x] for x in count if len(x) > 1 })  # 컴프리헨션 방식

!wget https://raw.githubusercontent.com/byungjooyoo/Dataset/main/korean_stopwords.txt
import re
stop_words=[]
with open("korean_stopwords.txt", 'r') as f:
    while True:
        line = f.readline().strip()
        stop_words.append(line)
        if not line: break
print(stop_words)

korean_stopwords = "korean_stopwords.txt"
with open(korean_stopwords, encoding='utf8') as f :
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

remove_char_counter = \
    Counter({x:remove_char_counter[x] for x in remove_char_counter if x not in stopwords})

remove_char_counter

tags = remove_char_counter.most_common(55)
tags

# 제거할 인덱스 리스트 (2와 18)
indices_to_remove = [8,12,18,35,37]

# 리스트 컴프리헨션을 사용하여 제거할 인덱스 제외
tags2 = [item for idx, item in enumerate(tags) if idx not in indices_to_remove]

tags2

!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 나눔 폰트 경로 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = fm.FontProperties(fname=font_path, size=10).get_name()

# 폰트 설정
plt.rc('font', family=font_name)

# WordCloud를 생성한다.
wc = WordCloud(font_path=font_path,background_color="white", max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tags2))

plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.savefig('워드클라우드.jpg', dpi=3000, bbox_inches='tight')
plt.show()

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Colab에서 폰트 설정
#!apt-get -y install fonts-nanum
fontpath = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font = fm.FontProperties(fname=fontpath, size=10)

labels, values = zip(*tags2)

# 막대그래프로 나타내기 (30개만 표시)
plt.figure(figsize=(12, 8))
plt.bar(labels[:30], values[:30], color='skyblue')
plt.title('지속가능성')
plt.xlabel('Tag')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right', fontproperties=font)  # X 축 레이블 회전 및 정렬

plt.savefig('단어빈도수.jpg', dpi=1500, bbox_inches='tight')

plt.show()

sustainability = pd.DataFrame(tags2, columns=['labels', 'values'])

# CSV 파일로 저장 (파일 이름은 원하는 대로 변경 가능)
sustainability.to_csv('sustainability.csv', index=False, encoding='utf-8-sig')