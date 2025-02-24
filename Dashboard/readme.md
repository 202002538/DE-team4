# 📊 대시보드 연결 과정 및 구현 내용

## 📌 프로젝트 개요
본 대시보드는 **AWS 기반 ETL 파이프라인**을 통해 수집된 데이터를 **Tableau에서 시각화**하는 프로젝트입니다. 데이터는 **Amazon S3**와 **Amazon Redshift Serverless**에서 불러와 실시간으로 분석됩니다.

---

## 🔗 데이터 소스 연결
### **S3 데이터 연결 (최근 48시간)**
- **실시간 데이터**는 S3에서 `live_{}.parquet` 파일을 직접 연결하여 표시됩니다.
- **데이터 갱신 주기**: 4시간마다 업데이트됩니다.

#### **Amazon S3 연결 방법**
AWS Management Console에서 **S3 버킷의 연결 정보를 확인**한 후, 아래 정보를 입력해야 합니다.

| 필드명 | 설명 | 입력 방법 |
|--------|------|----------|
| **Bucket Region** | S3 버킷이 위치한 AWS 리전 | AWS S3 Console에서 **버킷 상세 정보 → 리전(Region)** 확인 (예: `ap-northeast-2`) |
| **Bucket Name** | 데이터가 저장된 S3 버킷명 | AWS S3 Console에서 **버킷 이름(Bucket Name)** 확인 |
| **Access Key ID** | S3 접근을 위한 AWS IAM 사용자의 Access Key | AWS IAM에서 **Access Key 생성 후 확인** |
| **Secret Access Key** | Access Key와 함께 사용하는 비밀 키 | IAM에서 Access Key 생성 시 함께 제공 |


### **Redshift Serverless 데이터 연결 (최근 6개월)**
- 과거 6개월간의 데이터를 **Redshift Serverless**에서 변환 및 저장한 후 Tableau에 연결합니다.
- 대량 데이터 처리 및 분석을 위해 **Redshift에서 직접 쿼리**하여 데이터를 가져옵니다.

#### **Amazon Redshift Serverless 연결 방법**
AWS Management Console에서 **Redshift Serverless**의 연결 정보를 확인한 후, 아래 정보를 입력해야 합니다.

| 필드명 | 설명 | 입력 방법 |
|--------|------|----------|
| **Server** | Redshift Serverless 엔드포인트 | AWS Redshift Console에서 **Workgroup Endpoint** 확인 (예: `example-workgroup.123456789012.region.redshift-serverless.amazonaws.com`) |
| **Port** | Redshift Serverless의 포트 번호 | 기본 포트 **5439** 사용 |
| **Database** | 연결할 데이터베이스 이름 | AWS Redshift Console에서 **Database name** 확인 |
| **Authentication** | 인증 방법 | **Username & Password** 방식 선택 |
| **Username** | Redshift 로그인 사용자 이름 | AWS Redshift Console에서 **Master user name** 확인 |
| **Password** | 설정한 비밀번호 입력 | Redshift 생성 시 설정한 비밀번호 입력 |


---

## 📊 대시보드 구성
### **Tableau Dashboard**

#### **📍 Main Page (메인 페이지)**
- 최근 출시된 **4개 차종**에 대한 데이터 수집 및 분석 파이프라인 구축.
- **각 차종명을 클릭하면 디테일 페이지로 이동**하여 상세 분석 가능.
- 라인 차트(Line Chart)를 통해 최근 1년간 차종별 커뮤니티 조회수 총합을 시각화하여 **소비자 관심도 추이**를 확인 가능.

<img width="1510" alt="Image" src="https://github.com/user-attachments/assets/e284557c-0730-4836-9d6e-7d98205e0a4e" />


#### **🚗 Car Page (차량 상세 페이지)**
- 현대자동차 공식 PR센터에서 발표한 출시 기사를 분석하여, 기사에서 강조한 <b>주요 셀링 포인트(3가지)</b>를 선정.
- **소비자의 실제 반응과 비교**하여 기대와 실제 차이를 분석 가능.
- 각 셀링 포인트에 대한 소비자 댓글 및 피드백을 시각적으로 표현하여, **긍정/부정 반응을 구분**할 수 있도록 구성.

<img width="1510" alt="Image" src="https://github.com/user-attachments/assets/a87a6b80-1e96-41e6-99a2-414dd467b281" />


##### **Today’s Community Monitoring**
1. **Today's Hottest Topics**
   - 게시글을 키워드로 분석하여 **5가지 대분류, 16가지 소분류**로 구분
   - 가장 화제가 되는 **대분류**를 표시하며, 좋아요, 댓글 수, 조회수 등을 종합한 **화제도 지수**를 산정하여 소비자 관심도를 수치화
2. **Pie Chart**
   - 가장 화제가 된 **대분류**를 시각적으로 표현
3. **Bar Chart (Critical Focus Points)**
   - 각 **소분류의 관심도**를 막대 차트로 시각화하여 소비자들이 어떤 분야에 집중하는지 확인 가능
4. **게시글 목록 (Most Popular Article)**
   - 화제도가 높은 게시글을 목록으로 제공하며, 클릭 시 상세 내용을 확인할 수 있도록 구성
   - 소분류별 게시글을 필터링하여 특정 관심 주제별 조회 가능

##### **Last 6 Months Community Monitoring**
1. **Line Chart (Keyword Sentiment Distribution Over Time)**
   - 최근 6개월간의 **긍·부정 반응 변화**를 한눈에 볼 수 있도록, PR 센터에서 강조한 **3가지 주요 키워드별** 긍·부정 추이를 분석
2. **Bubble Chart**
   - 특정 키워드에 대한 **부정적 반응을 시각화**
   - **원의 크기**는 언급량, **색상**은 부정 감정 강도를 나타냄
3. **게시글 목록**
   - 최근 6개월 동안 **주요 셀링 포인트**로 선정된 3가지 키워드와 관련된 **화제도 높은 게시글 목록 제공**
   - 클릭하면 세부 내용을 확인하여 현재 커뮤니티에서 논의 중인 이슈 모니터링 가능


##### 📌 Tableau의 자동 새로고침 기능을 활용하여, 데이터가 갱신될 때 대시보드가 자동으로 업데이트됩니다.

---
