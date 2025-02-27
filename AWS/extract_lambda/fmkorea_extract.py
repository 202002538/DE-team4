from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import json
import time
import boto3
import os
from multiprocessing import Manager, Process

# 게시글 리스트 가져오기
def get_list_from_url(keyword, end_date, result_href_list, keyword_dict):
    href_list = []
    search_keywords = keyword_dict[keyword]

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-gpu", "--single-process"], headless=True)
        page = browser.new_page()
        for key in search_keywords:
            href_list.extend(get_inner_list(key, end_date, page))

    result_href_list[keyword] = list(set(href_list))

def get_inner_list(key, end_date, page):
    href_list = []
    page_number = 1
    today = datetime.now()
    while True:
        url = f"https://www.fmkorea.com/search.php?mid=car&search_keyword={key}&search_target=title_content&page={page_number}"
        page.goto(url)

        # 페이지가 완전히 로드될 때까지 대기
        page.wait_for_selector("tbody")  # tbody 요소가 로드될 때까지 기다림
        
        tbody = page.locator("tbody")
        if tbody.count() == 0:  # tbody가 없으면 종료
            break
        page.wait_for_selector("td.time")
        rows_time = tbody.locator("td.time").all()
        rows_href = tbody.locator("a.hx").all()
        for row_time, row_href in zip(rows_time, rows_href):
            date = row_time.inner_text().strip()
            print(date)
            try:
                dt_post = datetime.strptime(date, "%Y.%m.%d")
            except:
                dt_post = datetime.strptime(date,"%H:%M")
                dt_post = datetime.combine(today, dt_post.time())
            if dt_post < end_date:
                return href_list
            href = row_href.get_attribute("href")
            if href and "document_srl=" in href:
                href = href.split("document_srl=")[1].split("&")[0]
                href_list.append(href)
        page_number += 1
        time.sleep(0.3)

    return href_list

def get_htmls(keyword, hrefs, result, is_failed):
    js = {}
    failed_href_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-gpu", "--single-process"], headless=True)
        page = browser.new_page()
        for href in hrefs:
            try:
                if not browser.is_connected():
                    browser = p.chromium.launch(args=["--disable-gpu", "--single-process"], headless=True)
                if page.is_closed():
                    page = browser.new_page()
                print(href)
                inner_js = {}
                url = f'https://www.fmkorea.com/{href}'
                page.goto(url)
                page.wait_for_selector("div.rd_nav_style2")

                # 해당 요소가 존재하는지 확인
                if page.locator("div.rd_nav_style2").count() > 0:
                    html = page.locator("div.rd_nav_style2").inner_html()
                else:
                    html = "Element not found"

                inner_js["keyword"] = keyword
                inner_js["html"] = html
                js[url] = inner_js
                time.sleep(0.5)
            except Exception as e:
                if is_failed:
                    log_error("get_htmls", href, e)
                    continue
                else:
                    failed_href_list.append(href)
                    print("error on", href)
                    continue
    if failed_href_list and is_failed < 3:
        get_htmls(keyword, failed_href_list, result, is_failed+1)
    result.update(js)

def save_to_s3(data, bucket_name, folder_path, today, aws_region="ap-northeast-2"):
    """
    데이터를 JSON 형식으로 변환하여 S3에 저장하는 함수.
    """
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
        "source": "fmkorea_extract",
        "stage": stage,
        "url": url,
        "error": error_message
    }
    lambda_client.invoke(
        FunctionName=LOGGING_LAMBDA_ARN,
        InvocationType="Event",
        Payload=json.dumps(log_payload)
    )

# 크롤링 실행
def handler(event, context):
    keywords = event["keywords"]
    keyword_dict = os.getenv("KEYWORD_DICT", {'palisade': ["팰리", "펠리"],
                'avante': ["아반떼", "아방"],
                'tucson': ["투싼"],
                'ioniq9': ["오닉9", "아9"]
                })
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "hmg5th-4-bucket")
    S3_FOLDER_PATH = os.getenv("S3_FOLDER_PATH", "raw_html/fmkorea")
    yesterday = datetime.today() - timedelta(days=1)
    end_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.today().strftime("%Y-%m-%d")

    with Manager() as manager:
        result_href_list = manager.dict()
        processes = []
        for keyword in keywords:
            process = Process(target=get_list_from_url, args=(keyword, end_date, result_href_list, keyword_dict))
            processes.append(process)
            process.start()
            time.sleep(0.3)
        for process in processes:
            process.join()
    
        result_href_list = dict(result_href_list)

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

    save_to_s3(result_dict, S3_BUCKET_NAME, S3_FOLDER_PATH, today)

    return {"statusCode": 200, "body": "Scraping and upload completed successfully."}

if __name__ == "__main__":
    handler({"keywords":["palisade", "avante", "tucson", "ioniq9"]},"h")