# 현대자동차 소프티어 부트캠프 5기 Data Engineering 4조

## 📌 프로젝트 소개
- 본 프로젝트는 현대 자동차 공식 PR 센터에서 강조한 Selling Point가 실제 대중의 관심을 잘 끌고 있는지 모니터링하기 위해 개발된 Data Product 입니다. 

- 본 프로젝트는 **크롤링, 데이터 처리, 분석, 시각화**를 자동화하여 실시간 인사이트를 제공합니다.
- 크롤링 사이트: dcinside, fmkorea, clien, bobaedream
- 크롤링 차종: palisade, tucson, avante, ioniq9



### 🎯 주요 기능
- **웹 데이터 크롤링**: 다양한 커뮤니티에서 게시글과 댓글을 수집
- **데이터 정제 및 분석**: 정제된 데이터셋을 이용한 트렌드 및 통계 분석
- **실시간 대시보드 제공**: Tableau를 활용한 시각화

### 🎯 기술 스택
- 구현
  
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"><img src="https://img.shields.io/badge/Hadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black"><img src="https://img.shields.io/badge/Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"><img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=orange"><img src="https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white">


- 협업
  
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white"><img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=github&logoColor=white"><img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white">


---

## 👨‍💻 팀원 소개
<div align="center">

| DE | DE | DE |
| :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------------------: |
|      <img src="https://avatars.githubusercontent.com/u/89863441?v=4" width="120px;" alt=""/>      |      <img src="https://avatars.githubusercontent.com/u/136967331?v=4" width="120px;" alt=""/>      |            <img src="https://avatars.githubusercontent.com/u/90441461?v=4" width="120px;" alt=""/>            |
|           [한재웅](https://github.com/Hxxjaewoong)           |           [김태현](https://github.com/SpeOwO)           |                 [이채연](https://github.com/202002538)                 |
|    **Dashboard 시각화** <br> **EMR Cluster 구축**    |     **웹 크롤링 자동화** <br> **Spark Job 최적화**    | **파이프라인 안정성 확보** <br> **AWS Architecture** |

</div>


---

## 📊 대시보드 소개

![Image](https://github.com/user-attachments/assets/19b665e1-8368-435f-aa4e-5ff1c88468d5)

### 📌 주요 지표
- **게시글 및 댓글 트렌드 분석**
- **화제도 분석**
- **주요 키워드 및 감성 분석**
- **사용자 참여도 및 반응 패턴**


### 📌 인사이트 예시 - 팰리세이드
➡️ HMG PR팀에서 제시한 팰리세이드의 [3가지 공식 셀링 포인트](https://press.hmckmc.co.kr/news/press/newsDet.do?cotnNewsSn=202501130002): 외관 디자인, 실내 공간성, 주행감
  
 - **막대차트**: 디자인에서는 외관이, 공간에서는 실내 키워드가 의도대로 잘 주목받음
 - **파이차트 & 막대차트**: 가장 많이 화제된 퍼포먼스 분야에서 셀링포인트인 주행감보다 핸들링이 주목받음
 - **Most Popular Article(왼쪽)**: 핸들링을 체크하여 관련된 최근 글들을 읽고 왜 관심이 쏠렸는지 확인
 - **Sentiment Distribution**: 11월 중순 주행감에 대한 부정 반응이 긍정보다 급격히 증가함
 - **버블차트**: 외관이 가장 많이 언급되었으며, 색이 진한 것으로 보아 부정적인 반응이 많다
 - **Most Popular Article(오른쪽)**: 셀링포인트 3개와 관련된 반년간 화제도 순 글 정렬

### 🚨 Alarm
- 화제도를 기준으로 특정 수치(Threshold)를 초과하면 Slack으로 게시글 알림을 자동으로 전송하는 기능 구현
![Image](https://github.com/user-attachments/assets/6afcdbde-6628-4283-acfb-0787f890ec06)


### Dashboard 상세 설명
- [📊 Tableau 대시보드](https://github.com/softeer5th/DE-team4-Hoice/tree/main/Dashboard)


---

## 📂 폴더 구조
```md
├── 📂 AWS # 전체 아키텍처 인스턴스들
│ ├── 📂 EMR
│ ├── 📂 extract_lambda
│ ├── 📂 parse_lambda
│ ├── 📂 merge_lambda
│ ├── 📂 redshift_load_lamda
│ ├── 📂 logging_lambda
│ ├── 📂 slack_alarm_lambda
│ ├── 📂 event_bridge
│ └── 📂 📝 README.md
│
├── 📂 Dashboard
├── 📂 StepFuntion 
├── 📝 README.md
└── 📜 .gitignore
```

---


## 🏗️ 아키텍처 구성

### 🔧 아키텍처 다이어그램
<img width="1073" alt="Image" src="https://github.com/user-attachments/assets/8724207e-803d-4d31-af13-ccbcfdebd615" />

### 🔧 Step Function flow
<img width="835" alt="Image" src="https://github.com/user-attachments/assets/8fb67526-5dde-468a-8172-6141070d2070" />


### 🔧 자세한 사항은...
- [아키텍처 다이어그램](https://github.com/softeer5th/DE-team4/tree/main/AWS)
- [Step Function](https://github.com/softeer5th/DE-team4/tree/main/StepFunction)

---




