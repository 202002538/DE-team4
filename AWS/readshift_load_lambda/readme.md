# 📌 README: Redshift 데이터 적재 Lambda

이 문서는 **S3에서 업로드된 Parquet 파일을 Redshift로 적재하는 Lambda 함수**에 대한 설명을 포함합니다.  
Lambda는 **S3 이벤트를 감지하여 실행되며, Parquet 데이터를 Staging 테이블을 거쳐 대상 테이블로 삽입**하는 역할을 수행합니다.

---

## 🛠 1. 개요
이 Lambda 함수는 **매일 20시(KST, 한국시간)** 이후 실행되며,  
**어제 자정부터 오늘 자정까지의 데이터를 필터링하여 Redshift에 적재**합니다.

### 📌 기능 요약
1. **S3 이벤트 트리거** → Parquet 파일이 업로드되면 Lambda 실행  
2. **Redshift 연결** → Staging 테이블(`temp_staging_table`)에 Parquet 데이터 적재  
3. **시간 필터링** → `datetime` 컬럼을 기준으로 **어제 자정~오늘 자정**의 데이터만 삽입  
4. **대상 테이블(`my_table`)에 추가 삽입**  
5. **Staging 테이블 초기화** (옵션)

---

## 📂 2. 환경 변수
Lambda 실행을 위해 **아래 환경 변수를 설정해야 합니다.**

| 환경 변수명          | 설명 |
|---------------------|------|
| `REDSHIFT_DATABASE` | Redshift 데이터베이스 이름 |
| `REDSHIFT_USER`     | Redshift 사용자 계정 |
| `REDSHIFT_PASSWORD` | Redshift 비밀번호 |
| `REDSHIFT_HOST`     | Redshift 클러스터 호스트 |
| `REDSHIFT_PORT`     | Redshift 포트 (기본값: 5439) |

---

## 🚀 3. 실행 흐름
1. **Lambda가 S3 이벤트를 수신** (Parquet 파일 업로드 감지)  
2. **현재 시간을 확인**하여 **20시(KST) 이전이면 실행 중단**  
3. **Redshift에 연결** 후 `temp_staging_table`에 Parquet 데이터 적재  
4. **어제 00:00 ~ 오늘 00:00 데이터만 필터링하여 `my_table`에 삽입**  
5. **(옵션) Staging 테이블 정리** (`TRUNCATE TABLE temp_staging_table;`)

---

## 🗄 4. Redshift 적재 SQL 예시
Lambda는 **Redshift에 Parquet 데이터를 적재**하기 위해 다음 SQL을 실행합니다.

### 📌 1️⃣ Staging 테이블로 데이터 로드
```sql
COPY temp_staging_table
FROM 's3://hmg5th-4-bucket/merge_data/contents/2025-02-22.parquet'
IAM_ROLE 'arn:aws:iam::your-account-id:role/your-redshift-role'
FORMAT AS PARQUET;
```

### 📌 2️⃣ 어제~오늘 자정 데이터만 대상 테이블에 삽입
```sql
INSERT INTO my_table
SELECT *
FROM temp_staging_table
WHERE datetime >= '2025-02-21 00:00:00'
  AND datetime < '2025-02-22 00:00:00';
```

## 🛑 5. 오류 처리
- Redshift 적재 중 오류 발생 시 **오류 메시지를 출력**하며, Lambda 실행이 종료됩니다.
- **20시(KST) 이전에는 실행되지 않음**

---

## 🎯 6. 주의사항
- **IAM Role 설정 필수**: `COPY` 명령어를 실행하려면 **Redshift에 S3 읽기 권한이 있는 IAM Role**을 사용해야 합니다.
- **Staging 테이블 필요**: `temp_staging_table`이 미리 생성되어 있어야 합니다.
- **시간 변환 주의**: Lambda는 **UTC 기준으로 실행되므로, 한국시간(KST)** 변환이 필요합니다.

---

✅ **이 Lambda는 S3에서 업로드된 Parquet 파일을 필터링하여 Redshift에 적재하는 역할을 수행합니다.**  
⚡ `Staging 테이블 → 대상 테이블` 구조로 적재하여 **데이터 품질 유지 및 성능 최적화**를 고려하였습니다. 🚀
