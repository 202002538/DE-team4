# 현대자동차 소프티어 부트캠프 5기 Data Engineering 4조

## 📌 1. 프로젝트 소개
- **[프로젝트 이름]**은 현대 자동차 공식 PR 센터에서 강조한 셀링 포인트가 실제 대중의 관심을 잘 끌고 있는지 모니터링하기 위해 개발된 데이터 프로덕트 입니다. 

- 본 프로젝트는 **크롤링, 데이터 처리, 분석, 시각화**를 자동화하여 실시간 인사이트를 제공합니다.
- 크롤링 사이트: dcinside, fmkorea, clien, bobaedream
- 크롤링 차종: palisade, tucson, avante, ioniq9



### 🎯 주요 기능
- **웹 데이터 크롤링**: 다양한 커뮤니티에서 게시글과 댓글을 수집
- **데이터 정제 및 분석**: 정제된 데이터셋을 이용한 트렌드 및 통계 분석
- **실시간 대시보드 제공**: Power BI / Tableau / Streamlit을 활용한 시각화

### 🎯 기술 스택
- 구현
  
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"><img src="https://img.shields.io/badge/Hadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black"><img src="https://img.shields.io/badge/Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"><img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=orange">


- 협업
  
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white"><img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=github&logoColor=white"><img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white">


---

## 👨‍💻 2. 팀원 소개
<div align="center">

| <img src="https://img.shields.io/badge/Project_Leader-FF5733" /> | <img src="https://img.shields.io/badge/Tech_Leader-%2300264B" /> | <img src="https://img.shields.io/badge/Documentation_Leader-%2310069F%20" /> |
| :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------------------: |
|      <img src="https://github.com/" width="120px;" alt=""/>      |      <img src="https://github.com/" width="120px;" alt=""/>      |            <img src="https://github.com/" width="120px;" alt=""/>            |
|           [한재웅](https://github.com/Hxxjaewoong)           |           [김태현](https://github.com/SpeOwO)           |                 [이채연](https://github.com/202002538)                 |
|                            팀원1 기능                            |                            팀원2 기능                            |                                  팀원3 기능                                  |

</div>

---

## 📊 3. 대시보드 소개

![Image](https://github.com/user-attachments/assets/19b665e1-8368-435f-aa4e-5ff1c88468d5)

### 📌 주요 지표
- **게시글 및 댓글 트렌드 분석**
- **화제도 분석**
- **주요 키워드 및 감성 분석**
- **사용자 참여도 및 반응 패턴**

### 🔗 접근 방법
- [📊 Tableau 대시보드 링크](dashboard-url)
- [📊 Streamlit 대시보드 링크](dashboard-url)

---

## 📂 4. 폴더 구조
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
│ ├── 📂 📝 README.md
│
├── 📂 Dashboard
├── 📂 📝 README.md
├── 📂 StepFuntion 
├── 📝 README.md
└── 📜 .gitignore
```

---


## 🏗️ 5. 아키텍처 구성

### 🔧 아키텍처 다이어그램
<img width="1073" alt="Image" src="https://github.com/user-attachments/assets/8724207e-803d-4d31-af13-ccbcfdebd615" />

### 🔧 Step Function flow
<img width="835" alt="Image" src="https://github.com/user-attachments/assets/8fb67526-5dde-468a-8172-6141070d2070" />


### 🔧 자세한 사항은...
- [아키텍처 다이어그램](https://github.com/softeer5th/DE-team4/tree/main/AWS)
- [Step Function](https://github.com/softeer5th/DE-team4/tree/main/StepFunction)

---

## 🚀 6. 협업 방식



