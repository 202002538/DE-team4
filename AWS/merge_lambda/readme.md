# 📝 Merge Lambda (`merge_lambda`)

## 📌 개요
`merge_lambda`는 **Step Function 내에서 실행되며, 여러 커뮤니티 사이트(DCInside, BobaeDream, Clien, FMKorea)의 본문 및 댓글 데이터를 병합하여 S3에 저장**하는 역할을 합니다.  
각 `parse` Lambda가 생성한 Parquet 파일을 불러와 합친 후, **Parquet 포맷으로 S3에 업로드**합니다.

---

## 📂 입력 데이터
Lambda는 S3에서 **각 커뮤니티별 본문 및 댓글 데이터를 가져와 병합**합니다.  
파일은 아래 경로에서 가져옵니다:

📥 **입력 데이터 경로**
- 본문 데이터: `raw_data/{site}/yyyy-mm-dd-content.csv`
- 댓글 데이터: `raw_data/{site}/yyyy-mm-dd-comment.csv`
  
✅ `site`는 다음 중 하나:
  - `dcinside`
  - `bobae`
  - `clien`
  - `fmkorea`

---

## 📤 출력 데이터
병합된 데이터는 아래 경로에 **Parquet 파일** 형식으로 저장됩니다.

📀 **출력 데이터 경로**
- 본문 데이터: `merge_data/contents/yyyy-mm-dd.parquet`
- 댓글 데이터: `merge_data/comments/yyyy-mm-dd.parquet`

---

## 📊 저장 데이터 형식
### 📌 본문 데이터 (`merge_data/contents/yyyy-mm-dd.parquet`)
| 컬럼명          | 타입      | 설명 |
|---------------|---------|----------------------------------|
| site         | string  | 사이트명 (예: `"dcinside"`) |
| datetime     | datetime | 게시글 작성 시간 |
| model       | string  | 검색 키워드 |
| title       | string  | 게시글 제목 |
| content     | string  | 게시글 내용 |
| url         | string  | 게시글 URL |
| author      | string  | 작성자 (사용 안함) |
| likes       | int     | 추천 수 |
| hates       | int     | 비추천 수 |
| comments_count | int     | 댓글 개수 |
| views       | int     | 조회수 |

### 📌 댓글 데이터 (`merge_data/comments/yyyy-mm-dd.parquet`)
| 컬럼명  | 타입   | 설명 |
|--------|--------|------|
| url    | string | 게시글 URL |
| title  | string | 게시글 제목 |
| comment | string | 댓글 내용 |

---

## 🔄 실행 흐름
1. **Step Function에서 `merge_lambda` 실행**
2. **S3에서 `raw_data/{site}/yyyy-mm-dd-content.csv` 및 `raw_data/{site}/yyyy-mm-dd-comment.csv` 가져오기**
3. **Pandas를 사용해 데이터 병합**
4. **병합된 데이터를 `merge_data/contents/yyyy-mm-dd.parquet`, `merge_data/comments/yyyy-mm-dd.parquet`에 저장**
5. **Slack으로 성공/실패 로그 전송**
6. **Step Function에 병합 결과 반환**

---

## 🛑 오류 처리
Lambda 실행 중 오류 발생 시, **`crawling_log_lambda`** 를 호출하여 Slack으로 오류 메시지를 전송합니다.

### 1️⃣ **S3에서 파일을 찾을 수 없는 경우**
- `list_s3_files()` 단계에서 **S3에 해당 파일이 존재하지 않을 경우**, 로그를 남기고 빈 리스트 반환.

예제 오류 메시지:
```md
🚨 **오류 발생!**
- **위치:** `merge_lambda`
- **단계:** `upload_parquet_to_s3`
- **오류 메시지:**  
```


### 2️⃣ **병합할 데이터가 없는 경우**
- 본문 및 댓글 데이터를 병합한 결과가 **비어 있는 경우**, Step Function의 정상 진행을 방해하지 않도록 `log_error()`를 실행.
- 단, **병합된 본문 및 댓글 데이터가 모두 없는 경우** `NoDataToMergeException`을 발생시키고 Step Function에서 오류로 처리됨.

예제 오류 메시지:
```md
🚨 **병합 오류 발생!**
- **위치:** `merge_lambda`
- **단계:** `lambda_handler`
- **오류 메시지:**  
```
