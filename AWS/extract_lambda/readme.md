# 🚀 Extract Lambda Functions

이 문서는 **DCInside, BobaeDream, Clien, FMKorea** 사이트에서 크롤링한 HTML 데이터를 수집하는 **Extract Lambda Functions**에 대한 설명을 포함합니다.  
각 Lambda는 **Step Function에서 전달받은 키워드 목록을 기반으로 크롤링을 수행하고, HTML 데이터를 S3에 저장**하는 역할을 수행합니다.

---

## **🛠️ 1. 프로젝트 개요**
📀 **Step Function Workflow**
1. **Step Function에서 키워드 목록을 전달받음**  
2. **Extract Lambda 실행 → 해당 키워드로 크롤링 수행**  
3. **HTML 데이터를 JSON 형식으로 변환 후 S3 저장**  
4. **성공 또는 실패 로그를 기록 후 Step Function에 결과 전달**  

---

## **📂 2. Lambda 함수 개요**
### ✅ **DCInside Extract Lambda**
- **Lambda 이름:** `dcinside_extract`  

### ✅ **Clien Extract Lambda**
- **Lambda 이름:** `clien_extract`   

### ✅ **BobaeDream Extract Lambda**
- **Lambda 이름:** `bobae_extract`  

### ✅ **FMkorea Extract Lambda**
- **Lambda 이름:** `fmkorea_extract`  

---

## **📀 3. 입출력 데이터 형식**

- **입력 데이터:** Step Function에서 전달받은 키워드 목록. 예: ['palisade', 'tucson', 'ioniq9', 'avante']
- **출력 데이터:** `raw_html/{site}/yyyy-mm-dd.json` (크롤링한 HTML 데이터)  

Extract Lambda는 HTML 페이지를 JSON 파일로 저장하며, JSON 파일의 데이터 구조는 다음과 같습니다.

```json
{
  "게시글URL_1": {
    "keyword": "검색 키워드",
    "html": "<html>...</html>"
  },
  "게시글URL_2": {
    "keyword": "검색 키워드",
    "html": "<html>...</html>"
  }
}
```
--- 

## **4. Lambda Workflow**

1. **사이트별 검색 기능 활용**  
   각 사이트에서 제공하는 검색 기능을 이용하여 주어진 키워드를 검색하고, 설정된 기간 내에 작성된 게시글의 URL과 페이지 넘버를 수집합니다.

2. **수집된 URL 방문 및 크롤링**  
   수집된 URL을 순차적으로 방문하여, 필요한 정보를 포함한 HTML `Body` 태그를 추출하고 이를 JSON 형태로 저장합니다.

3. **멀티프로세싱 구현**  
   1, 2번 과정을 4개의 `multiprocessing Manager`를 통해 4개의 함수가 비동기적으로 실행되도록 하여, 간접적인 멀티프로세싱을 구현했습니다. 이를 통해 크롤링 작업의 효율성을 극대화했습니다.

4. **오류 처리 및 재시도**  
   오류가 발생할 경우 재시도하는 메커니즘을 구축하였으며, 지속적으로 오류가 발생할 경우 `log_error` 함수를 통해 Step Function에 오류를 전달하여 프로세스를 재시작할 수 있도록 했습니다.

---

## **5. Lambda 구현 특이사항**

- **동적 크롤링을 위한 Playwright 사용**  
  동적 웹사이트의 크롤링을 위해 Playwright라는 End-to-End(E2E) 프레임워크를 활용하여 자동화된 크롤링을 구현했습니다.

- **AWS Lambda 환경의 제약**  
  AWS Lambda는 컨테이너 환경에서 실행되며, 멀티프로세싱을 직접적으로 지원하지 않기 때문에 네트워크 I/O Bound 작업인 크롤링 중에 대기 시간이 길어지면 자원 낭비가 발생할 수 있습니다.

- **멀티프로세싱 대안**  
  Lambda는 `multiprocessing.Queue`를 지원하지 않지만, 이를 해결하기 위한 3가지 대안을 고려하여 선택했습니다
  
  1. **Pipe**  
     - AWS Lambda에서 공식적으로 지원하는 방법으로, 데이터를 프로세스 간에 전달하는 방식입니다.
     - 그러나 데이터 사이즈가 커지면 버퍼링이 발생하는 문제점이 있습니다.
  
  2. **Async 구현**  
     - `async` 키워드와 Playwright의 비동기 패키지를 사용하여 코루틴을 통해 비동기 처리를 구현했습니다.
     - 이 방법은 속도 면에서 가장 우수하고 Lambda 환경에 적합하지만, 코드 가독성이 떨어지고 `Browser Context`가 소멸되는 문제가 발생하여 안정성이 낮았습니다.
  
  3. **Multiprocessing Manager + Process 사용**  
     - `Manager`를 사용하여 공유 `dict`와 `list`를 통해 간접적으로 비동기 처리를 구현했습니다.
     - 이 방법이 가장 안정적이며 코드 가독성이 좋고, 다양한 사이트에 재사용하기에 적합했습니다.

### **결론**  
Lambda 환경에서 멀티프로세싱을 효과적으로 처리하기 위해 **Multiprocessing Manager + Process** 방법을 채택하여 처리율을 높이고, Lambda의 실행 시간을 단축하는 데 성공했습니다.
