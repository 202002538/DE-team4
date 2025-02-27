from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import json
import boto3
import os
import time
from multiprocessing import Manager, Process

# 게시글 리스트 가져오기
def get_list_from_url(keyword, end_date, result_href_list, keyword_dict):
    href_list = []
    search_keywords = keyword_dict[keyword]
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-gpu", "--single-process"], headless=True)
        page = browser.new_page()
        for key in search_keywords:
            if page.is_closed():
                page = browser.new_page()
            try:
                href_list.extend(get_inner_list(key, end_date, page))
            except Exception as e:
                log_error("get_list_from_url", key, e)
                continue
    result_href_list[keyword] = list(set(href_list))

def get_inner_list(key, end_date, page):
    href_list = []
    page_number = 1
    while True:
        if page_number > 15:
            break
        print(key, page_number)
        try:
            url = f"https://gall.dcinside.com/board/lists/?id=car_new1&page={page_number}&search_pos=&s_type=search_subject_memo&s_keyword={key}"
            page.goto(url, wait_until="load")

            # 페이지가 완전히 로드될 때까지 대기
            page.wait_for_selector("tbody.listwrap2")  # tbody 요소가 로드될 때까지 기다림
            
            tbody = page.locator("tbody.listwrap2")
            if (tbody.count()) == 0:  # tbody가 없으면 종료
                break
            trs = tbody.locator("tr.us-post").all()
            for tr in trs:
                td_time = tr.locator("td.gall_date").get_attribute("title")  # 추가
                td_time = td_time.strip()  # strip()은 동기 메서드이므로 문제가 되지 않음
                dt_post = datetime.strptime(td_time, "%Y-%m-%d %H:%M:%S")
                if dt_post < end_date:
                    print(td_time)
                    return href_list
                td_href = tr.locator("td.gall_num").inner_text()  # 추가
                td_href = td_href.strip()  # strip()은 동기 메서드이므로 문제가 되지 않음
                href_list.append(td_href)
        except Exception as e:
            log_error("get_inner_list", url, "목록 가져올 수 없음")
            return e
        page_number += 1
        time.sleep(0.3)  # 비동기식으로 대기

    return href_list

# HTML 가져오기
def get_htmls(keyword, hrefs, result, is_failed):
    js = {}
    failed_href_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-gpu", "--single-process"], headless=True)
        page = browser.new_page()
        
        for href in hrefs:
            try:
                if page.is_closed():
                    page = browser.new_page()
                print(f"크롤링 시작: {href}")
                inner_js = {}
                url = f'https://gall.dcinside.com/board/view/?id=car_new1&no={href}'
                
                page.goto(url, timeout=60000)  # 타임아웃 설정
                page.wait_for_selector("main.gallery_view", timeout=10000)
                comment = page.locator("div.comment_count em.font_red").inner_text()
                if comment != '0':
                    page.wait_for_selector("div.cmt_nickbox")
                main = page.locator("main.gallery_view")
                html = main.locator("article").nth(1).inner_html()
                
                inner_js["keyword"] = keyword
                inner_js["html"] = html
                js[url] = inner_js

                time.sleep(1)  # 부하 방지
            except Exception as e:
                if is_failed:
                    log_error("get_htmls", href, "페이지 가져올 수 없음")
                else:
                    failed_href_list.append(href)
                continue  # 다음 href로 넘어감
        
        browser.close()  # 브라우저 종료
    if failed_href_list and is_failed < 3:
        get_htmls(keyword, failed_href_list, result, is_failed+1)
    result.update(js)

# S3에 저장
def save_to_s3(data, bucket_name, folder_path, today, aws_region="ap-northeast-2"):
    object_key = f"{folder_path}/{today}.json"
    try:
        s3_client = boto3.client("s3", region_name=aws_region)
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_data,
            ContentType="application/json"
        )

        print(f"✅ 업로드 성공: s3://{bucket_name}/{object_key}")
        return True
    except Exception as e:
        print(f"❌ 업로드 실패: {e}")
        return False

def log_error(stage, url, error_message):
    LOGGING_LAMBDA_ARN = "arn:aws:lambda:ap-northeast-2:473551908409:function:crawling_log_lambda"
    lambda_client = boto3.client('lambda')
    log_payload = {
        "status": "error",
        "source": "clien_extract",
        "stage": stage,
        "url": url,
        "error": error_message
    }
    lambda_client.invoke(
        FunctionName=LOGGING_LAMBDA_ARN,
        InvocationType="Event",
        Payload=json.dumps(log_payload)
    )

def get_list(keywords, end_date, keyword_dict):
    with Manager() as manager:
        result_href_list = manager.dict()
        processes = []
        for keyword in keywords:
            process = Process(target=get_list_from_url, args=(keyword, end_date, result_href_list, keyword_dict))
            processes.append(process)
            time.sleep(0.25)
            process.start()
        for process in processes:
            process.join()
    
        result_href_list = dict(result_href_list)
    return result_href_list

def handler(event, context):
    keywords = event["keywords"]
    keyword_dict = os.getenv("KEYWORD_DICT",{'palisade': ["팰리", "펠리"],
                'avante': ["아반떼", "아방"],
                'tucson': ["투싼"],
                'ioniq9': ["오닉9"]
                })
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "hmg5th-4-bucket")
    S3_FOLDER_PATH = os.getenv("S3_FOLDER_PATH", "raw_html/dcinside")
    yesterday = datetime.today() - timedelta(days=1)
    end_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.today().strftime("%Y-%m-%d")
    try:
        result_href_list = get_list(keywords, end_date, keyword_dict)
    except:
        try: 
            result_href_list = get_list(keywords, end_date, keyword_dict)
        except:
            return {"status":"Failed to get url list", "statusCode": 429, "body": "failed to get url list"}

    with Manager() as manager:
        result = manager.dict()
        processes = []
        for key, value in result_href_list.items():
            process = Process(target=get_htmls, args=(key, value, result, 0))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()

        result_dict = dict(result)

    # 결과를 S3에 저장
    save_to_s3(result_dict, S3_BUCKET_NAME, S3_FOLDER_PATH, today)
    return {"statusCode": 200, "body": "Scraping and upload completed successfully."}

if __name__ == "__main__":
    handler({"keywords":["palisade", "avante", "tucson", "ioniq9"]},"h")