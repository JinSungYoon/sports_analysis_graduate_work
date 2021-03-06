import csv
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt

# matplotlib의 font_manager에서 설정을 변경해주는 방법을 통해 한글을 출력하는 방법
# http://gomguard.tistory.com/172

# 한글 폰트 안 깨지게하기위한 import
import matplotlib.font_manager as fm

# 가져올 폰트 지정
font_location='E:/글꼴/H2GTRE.TTF'
# 폰트 이름 지정 
font_name=fm.FontProperties(fname=font_location).get_name()
mpl.rc('font',family=font_name)

# 다른 파일에 있는 파일 불러오기 위한 import
import sys
# 해당 파일을 불러오기 위해서 paht경로 지정하기
sys.path.insert(0,'E:\대학교\졸업\졸업작품\웹크롤링\Webcrwaling and scraping using python')

import kovo_game_data_Beautifulsoup as kovo

# Pandas로 데이터 읽어오기
# utf-8로 인코딩 된 파일 읽어오기
#table=pd.read_csv('서울시 대중교통 수단별 이용 현황.csv',delimiter=',',engine='python',encoding="utf-8")
# EUC-KR로 인코딩 된 파일 읽어오기
#test=pd.read_csv('서울교통공사 2016년 일별 역별 시간대별 승하차인원(1_8호선).csv',engine='python',encoding='EUC-KR')

# 배구 시즌 데이터 불러오기
Season_result=pd.read_csv('E:/대학교/졸업/졸업작품/웹크롤링/Webcrwaling and scraping using python/Season_result.csv',engine='python',encoding='EUC-KR')

#배구 시즌 데이터 인덱스 Date로 재설정하기
Season_result=Season_result.set_index("Date")

# Python에서 SQL문처럼 사용하는 방법 사이트 https://codeburst.io/how-to-rewrite-your-sql-queries-in-pandas-and-more-149d341fc53e

# 한 시즌에서 한국전력의 경기만 불러오기 테이블명.query(해당열조건 |(or) &(and) 해당열조건)
#print(Season_result.query("Home=='한국전력'|Away=='한국전력'"))

# ==================================== 시즌 결과 데이터 7년치 ===========================================================
"""
# 시즌 7년 데이터 불러오기
# 10년치 데이터를 긁어오려고 하였으나 2011년도부터 승점 제도가 도입되었고, 그에따른 플레이오프 진출 규정도 승점제도로 변경되어 7년전 데이터부터 긁어왔다.
MSeason=kovo.MSeason
FSeason=kovo.FSeason

# 플레이오프에 진출여부에 대한 column을 하나 생성한다.
# 플레이오프에 진출하기위한 조건은 남자,여자부 3위 이내 팀은 자동 진출이고 남자부의 경우에만 3위와 4위의 승점이 3점 이내일 경우 플레이오프에 진출한다.

MPlay_off = [ [] for i in range(len(MSeason))]
FPlay_off = [ [] for i in range(len(FSeason))]

for year in range(len(MSeason)):
    for rank in range(len(MSeason[year])):
        if rank<3:
            MPlay_off[year].append(1)
        else:
            # 2010-2011시즌부터 남자부는 3위와 4위가 승점이 3점 이내로 났을경우 준플레이오프에 진출하게 된다.
            if (rank==3 and MSeason[year].iloc[2]["승점"]-MSeason[year].iloc[3]["승점"]<=3):
                MPlay_off[year].append(1)
            else:
                MPlay_off[year].append(0)

for year in range(len(FSeason)):
    for rank in range(len(FSeason[year])):
        if rank<3:
            FPlay_off[year].append(1)
        else:
            FPlay_off[year].append(0)

print(Mplay_off)

for loop in range(len(MPlay_off)):            
    MSeason[loop]["플레이오프_진출"]=MPlay_off[loop]
    FSeason[loop]["플레이오프_진출"]=FPlay_off[loop]

MAll_data = []
FAll_data = []

for year in range(len(MSeason)):
    for team in range(len(MSeason[year])):
        MAll_data.append(MSeason[year].iloc[team])

for year in range(len(FSeason)):
    for team in range(len(FSeason[year])):
        FAll_data.append(FSeason[year].iloc[team])

Mavg = [ [] for i in range(5) ]
Favg = [ [] for i in range(5) ]
index = 0
for i in range(len(MSeason)):
    Mavg[index].append(float(MSeason[i].iloc[2:3]["승점"]))
    Favg[index].append(float(FSeason[i].iloc[2:3]["승점"]))
    Mavg[index+1].append(float(MSeason[i].iloc[2:3]["승"]))
    Favg[index+1].append(float(FSeason[i].iloc[2:3]["승"]))
    Mavg[index+2].append(float(MSeason[i].iloc[2:3]["패"]))
    Favg[index+2].append(float(FSeason[i].iloc[2:3]["패"]))
    Mavg[index+3].append(float(MSeason[i].iloc[2:3]["세트득실률"]))
    Favg[index+3].append(float(FSeason[i].iloc[2:3]["세트득실률"]))
    Mavg[index+4].append(float(MSeason[i].iloc[2:3]["점수득실률"]))
    Favg[index+4].append(float(FSeason[i].iloc[2:3]["점수득실률"]))

    
def avg(line):
    sum=0
    for loop in range(len(line)):
        sum+=line[loop]
    return sum/len(line)


print("남자부 3위 최대 승점 : %2.2f / 승 : %2.2f / 패 : %2.2f / 세트득실률 : %2.2f / 점수득실률 : %2.2f"%(max(Mavg[0]),max(Mavg[1]),max(Mavg[2]),max(Mavg[3]),max(Mavg[4])))
print("남자부 3위 평균 승점 : %2.2f / 승 : %2.2f / 패 : %2.2f / 세트득실률 : %2.2f / 점수득실률 : %2.2f"%(avg(Mavg[0]),avg(Mavg[1]),avg(Mavg[2]),avg(Mavg[3]),avg(Mavg[4])))
print("남자부 3위 최소 승점 : %2.2f / 승 : %2.2f / 패 : %2.2f / 세트득실률 : %2.2f / 점수득실률 : %2.2f"%(min(Mavg[0]),min(Mavg[1]),min(Mavg[2]),min(Mavg[3]),min(Mavg[4])))

print('\n')

print("여자부 3위 최대 승점 : %2.2f / 승 : %2.2f / 패 : %2.2f / 세트득실률 : %2.2f / 점수득실률 : %2.2f"%(max(Favg[0]),max(Favg[1]),max(Favg[2]),max(Favg[3]),max(Favg[4])))
print("여자부 3위 평균 승점 : %2.2f / 승 : %2.2f / 패 : %2.2f / 세트득실률 : %2.2f / 점수득실률 : %2.2f"%(avg(Favg[0]),avg(Favg[1]),avg(Favg[2]),avg(Favg[3]),avg(Favg[4])))
print("여자부 3위 최소 승점 : %2.2f / 승 : %2.2f / 패 : %2.2f / 세트득실률 : %2.2f / 점수득실률 : %2.2f"%(min(Favg[0]),min(Favg[1]),min(Favg[2]),min(Favg[3]),min(Favg[4])))

"""
# ================================ 의사결정나무 연습 =========================================
"""
# http://yamalab.tistory.com/31 <reference>

from sklearn import tree
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

iris = datasets.load_iris()

X = iris.data[:,[2,3]]
Y = iris.target

#print(X)
#print(Y)

# 자동으로 데이터셋을 분리해주는 함수
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3,random_state=0)

# 데이터 표준화 작업
sc = StandardScaler()
sc.fit(X_train)

# 표준화된 데이터셋
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

iris_tree = tree.DecisionTreeClassifier(criterion='entropy',max_depth=3,random_state=0)
iris_tree.fit(X_train,Y_train)

# 정확도를 알기 위한 임포트
from sklearn.metrics import accuracy_score

Y_pred_tr = iris_tree.predict(X_test)

print("Accuracy : %.2f"%accuracy_score(Y_test,Y_pred_tr))

#from sklearn.tree import export_graphviz
#import pydotplus
#from IPython.display import Image
#
##from sklearn.tree import export_graphviz
##import pydotplus
##from IPython.display import Image
#
#dot_data = export_graphviz(iris_tree, out_file=None, feature_names=['petal length','petal width'],
#                           class_names=iris.target_names, filled=True, rounded=True, special_character=True)
#graph = pydotplus.graph_from_dot_data(dot_data)
#Image(graph.create_png())
"""

#===================== 경기에서 각 항목별 성공비율이 경기의 승리와 연관이 있는지 성공비율을 비교(경기 세부데이터)===============================

"""
#===================== 오늘 또 하나의 좋은 삽질을 했다 ㅎㅎㅎㅎㅎ==================================================================================

# 경기에서 각 항목별 성공비율이 경기의 승리와 연관이 있는지 알아보자.

Hframe=kovo.Hframe
Aframe=kovo.Aframe

HScore=Hframe["득점"].sum()
AScore=Aframe["득점"].sum()
HA=Hframe["공격종합"]["성공"].sum()/Hframe["공격종합"]["시도"].sum()
AA=Aframe["공격종합"]["성공"].sum()/Aframe["공격종합"]["시도"].sum()
HO=Hframe["오픈"]["성공"].sum()/Hframe["오픈"]["시도"].sum()
AO=Aframe["오픈"]["성공"].sum()/Aframe["오픈"]["시도"].sum()
HT=Hframe["시간차"]["성공"].sum()/Hframe["시간차"]["시도"].sum()
AT=Aframe["시간차"]["성공"].sum()/Aframe["시간차"]["시도"].sum()
HRear=Hframe["후위"]["성공"].sum()/Hframe["후위"]["시도"].sum()
ARear=Aframe["후위"]["성공"].sum()/Aframe["후위"]["시도"].sum()
HQ=Hframe["속공"]["성공"].sum()/Hframe["속공"]["시도"].sum()
AQ=Aframe["속공"]["성공"].sum()/Aframe["속공"]["시도"].sum()
HQO=Hframe["퀵오픈"]["성공"].sum()/Hframe["퀵오픈"]["시도"].sum()
AQO=Aframe["퀵오픈"]["성공"].sum()/Aframe["퀵오픈"]["시도"].sum()
HServe=Hframe["서브"]["성공"].sum()/Hframe["서브"]["시도"].sum()
AServe=Aframe["서브"]["성공"].sum()/Aframe["서브"]["시도"].sum()
HD=Hframe["디그"]["성공"].sum()/Hframe["디그"]["시도"].sum()
AD=Aframe["디그"]["성공"].sum()/Aframe["디그"]["시도"].sum()
HSet=Hframe["세트"]["성공"].sum()/Hframe["세트"]["시도"].sum()
ASet=Aframe["세트"]["성공"].sum()/Aframe["세트"]["시도"].sum()
HReceive=Hframe["리시브"]["정확"].sum()/Hframe["리시브"]["시도"].sum()
AReceive=Aframe["리시브"]["정확"].sum()/Aframe["리시브"]["시도"].sum()
HBlock=Hframe["블로킹"]["성공"].sum()/Hframe["블로킹"]["시도"].sum()
ABlock=Aframe["블로킹"]["성공"].sum()/Aframe["블로킹"]["시도"].sum()
HE=Hframe["범실"].sum()
AE=Aframe["범실"].sum()

#print("현대캐파탈의 각 항목별 성공률\n 득점 : %2.2f / 공격종합 : %2.2f / 오픈 : %2.2f / 시간차 :%2.2f /\n 후위 : %2.2f / 속공 : %2.2f / 퀵오픈 : %2.2f / 서브 : %2.2f /\n 디그 : %2.2f / 세트 : %2.2f / 리시브 : %2.2f / 블로킹 : %2.2f / 범실 %d"%(HScore,HA,HO,HT,HRear,HQ,HQO,HServe,HD,HSet,HReceive,HBlock,HE))
#print("대한항공의 각 항목별 성공률\n 득점 : %2.2f / 공격종합 : %2.2f / 오픈 : %2.2f / 시간차 :%2.2f /\n 후위 : %2.2f / 속공 : %2.2f / 퀵오픈 : %2.2f / 서브 : %2.2f /\n 디그 : %2.2f / 세트 : %2.2f / 리시브 : %2.2f / 블로킹 : %2.2f / 범실 %d"%(AScore,AA,AO,AT,ARear,AQ,AQO,AServe,AD,ASet,AReceive,ABlock,AE))

# 경기 관련 정보 그래프 그리기
# https://matplotlib.org/examples/pylab_examples/barchart_demo.html 참조

# 내가 표현하고 싶은 데이터
Sky=[HA,HO,HT,HRear,HQ,HQO,HServe,HD,HSet,HReceive,HBlock]
Jumbos=[AA,AO,AT,ARear,AQ,AQO,AServe,AD,ASet,AReceive,ABlock]

fig,ax = plt.subplots()     # 그래프를 여러개 표현할때 사용하는것 같다.

height = np.arange(len(Sky))    # y축 높이
bar_width=0.35  # 그래프의 너비

opacity = 0.4

# x축에 들어갈 이름
xlabel = ["공격종합","오픈","시간차","후위공격","속공","퀵오픈","서브","디그","세트","리시브","블로킹"]

# 데이터 bar형태로 표현
Sky_graph=plt.bar(height,Sky,bar_width,
                  alpha=opacity,        # 그래프 불투명도
                  color='r',            # 그래프 색깔
                  label='현대캐피탈')
# 여기서 그래프를 분리해서 보고 싶다면 y축에 그래프의 너비만큼을 더해줘야 한다.
Jumbos_graph=plt.bar(height+bar_width,Jumbos,bar_width,
                     alpha=opacity,     # 그래프 불투명도
                     color='b',         # 그래프 색깔
                     label='대한항공')
# x,y축 그래프 이름 설정
plt.xlabel('각 항목')
plt.ylabel('성공률')
plt.title('두 팀의 항목별 성공률 비교')

# x축 항목 이름 지정
plt.xticks(height,xlabel)
plt.legend()

plt.tight_layout()
plt.show()
"""
#==============================================실시간 중계 데이터 분석===============================================================
"""
# 실시간 중계데이터에서 부문별 성공률 정리한 데이터 가져오기

On_air_rate=kovo.Rate_record
On_air_success=kovo.Success_record

# 각 세트의 항목별 성공률 그래프화
for set_num in range(4):
    # 각 팀의 세트 데이터 가져오기
    Sky_1st = On_air_rate.iloc[set_num]
    Jumbos_1st = On_air_rate.iloc[set_num+1]
        
    fig,ax = plt.subplots()
    
    height = np.arange(len(Sky_1st))    # 그래프의 y축 높이
    
    bar_width = 0.4                     # 그래프의 너비
    
    opacity = 0.4                       #그래프의 불투명도
    
    Home_graph=plt.bar(height,Sky_1st,bar_width,
                       alpha=opacity,
                       color='#000000',
                       label="현대캐피탈"
                       )
    
    Away_graph=plt.bar(height+bar_width,Jumbos_1st,bar_width,
                       alpha=opacity,
                       color='#0000FF',
                       label="대한항공"
                       )
    
    # x,y축 그래프 이름 설정
    plt.xlabel=('각 항목')
    plt.ylabel=('성공률')
    plt.title('%d세트 두 팀의 항목별 성공률 비교'%(set_num+1))
    
    # x축 항목 이름 지정
    plt.xticks(height,kovo.Scoring_sort)
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# 각 세트의 성공횟수 그래프 생성
for set_num in range(4):
    # 각 팀의 세트 데이터 가져오기
    Sky_1st = On_air_success.iloc[set_num]
    Jumbos_1st = On_air_success.iloc[set_num+1]
        
    fig,ax = plt.subplots()
    
    height = np.arange(len(Sky_1st))
    
    bar_width = 0.4
    
    opacity = 0.4
    
    # Home팀의 경기 그래프
    Home_graph=plt.bar(height,Sky_1st,bar_width,
                       alpha=opacity,
                       color='r',
                       label="현대캐피탈"
                       )
    
    # Away팀의 경기 그래프
    Away_graph=plt.bar(height+bar_width,Jumbos_1st,bar_width,
                       alpha=opacity,
                       color='g',
                       label="대한항공"
                       )
    
    # x,y축,그래프 이름 설정
    plt.xlabel=('각 항목')
    plt.ylabel=('성공횟수')
    plt.title('%d세트 두 팀의 항목별 성공횟수 비교'%(set_num+1))
    
    # x축 항목 이름 지정
    plt.xticks(height,kovo.Scoring_sort)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
"""
#=====================================연습 데이터========================================================
"""
fruit=pd.DataFrame({
        '사과':np.random.randint(100,1000,size=10),
        '배':np.random.randint(100,1000,size=10),
        '참외':np.random.randint(100,1000,size=10),
        '옥수수':np.random.randint(100,1000,size=10),
        '고구마':np.random.randint(100,1000,size=10),
        '수박':np.random.randint(100,1000,size=10),
        '딸기':np.random.randint(100,1000,size=10),
        '토마토':np.random.randint(100,1000,size=10),
        },
        columns=['딸기','토마토','수박','참외','사과','배','옥수수','고구마'],
        index=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct']
        )
print(fruit)
fruit.index.name="Month"
# 열 데이터 추가
#fruit["sum"]=fruit.sum(axis=1)
print(len(fruit.columns))
print(len(fruit.index))
# 행 데이터 추가
fruit.loc["Nov"]=np.random.randint(100,1000,size=8)
fruit.loc["Dec"]=np.random.randint(100,1000,size=8)
print(fruit)
# 엑셀파일로 내보내기
fruit.to_csv("fruit.csv",mode='w',encoding='EUC-KR')
"""

#store=pd.read_csv('fruit.csv',engine='python')
# Month를 인덱스롤 재설정
#store=store.set_index("Month")
#print(store)
#store.sum(axis=1).plot(kind="bar")

"""
# 엑셀파일을 읽어옵니다.
f=open('서울시 대중교통 수단별 이용 현황.csv','r',encoding='utf-8')
rdr=csv.reader(f)

# Data에 엑셀 내용 넣기
Data=[]
for line in rdr:
    Data.append(line)
# Pandas로 Dataframe에 넣기
#Seoul=pd.DataFrame(Data[1:len(Data)+1],columns=Data[0],index=np.arange(1,len(Data)))
#Seoul=pd.DataFrame(Data[3:len(Data)+1],columns=Data[0][3:13],index=Data[:][2:])
#for loop in range(2,len(Data)):
#    print(Data[loop][2:])
#print(Seoul.info())
#print(Seoul)
# iloc는 [행,열]을 적으면 해당 데이터를 긁어온다.
#move=Seoul.iloc[:,3:13].sum(axis=0)
move=[]

# 달 정보 넣기
month=Data[0][3:13]

# map(자료형,data)는 해당 자료를 입력 자료형 형태로 변환해주는 함수이다.
for index in range(1,len(Data)-1):
    move.append(list(map(int,Data[index][3:13])))

# Dataframe에서 강제로 문자열을 숫자로 바꾸는 함수
def coerce_df_columns_to_numeric(df, column_list):
    df[column_list] = df[column_list].apply(pd.to_numeric, errors='coerce')
coerce_df_columns_to_numeric(Seoul,['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'])

#월별 지하철 이용객 그래프로 표시
#Seoul.iloc[:,3:13].sum(axis=0).plot(kind="bar")
#Seoul["1월"].plot(kind="bar")
"""
