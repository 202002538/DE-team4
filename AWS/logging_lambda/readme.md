# 🚀 Crawling Log Lambda (crawling_log_lambda)

이 Lambda 함수는 **크롤링 과정에서 발생하는 오류를 Slack으로 알림**하는 역할을 수행합니다.  
Step Function에서 오류 발생 시 호출되며, **Slack Webhook을 통해 오류 메시지를 전송**합니다.

---
## **📂 1. 입력 데이터 형식**
Lambda는 Step Function에서 JSON 형식의 오류 로그를 전달받습니다.

| 필드명      | 타입     | 설명                         |
|------------|---------|-----------------------------|
| `timestamp` | string | 오류 발생 시간 (`YYYY-MM-DD HH:MM`) |
| `source`   | string  | 오류 발생 위치 (예: `bobae_extract`) |
| `stage`    | string  | 오류 단계 (예: `extract_content`) |
| `keyword`  | string  | 관련 키워드 (예: `palisade`) |
| `url`      | string  | 오류가 발생한 URL |
| `error`    | string  | 오류 메시지 상세 내용 |

### **📌 입력 데이터 예시**
```json
{
  "timestamp": "2025-02-22 14:30",
  "source": "bobae_extract",
  "stage": "extract_content",
  "keyword": "palisade",
  "url": "https://www.bobaedream.co.kr/view/12345",
  "error": "본문이 존재하지만 파싱 실패"
}
```
---
## **📌 2. 알림 메시지 예시**
Slack으로 전송되는 메시지는 다음과 같은 형식입니다.

<img width="590" alt="Image" src="https://github.com/user-attachments/assets/1d0d156e-5717-4c3e-bced-d00855a2d796" />

---
## **🔧 3. 실행 흐름**
#### 1️⃣ Step Function에서 오류 발생 시 crawling_log_lambda 호출
#### 2️⃣ Lambda가 오류 데이터를 받아 Slack 메시지 생성
#### 3️⃣ Slack Webhook을 통해 메시지 전송
#### 4️⃣ 전송 성공/실패 여부 반환


