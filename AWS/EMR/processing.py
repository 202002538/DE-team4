from pyspark.sql import SparkSession, functions as F, types as T
from datetime import datetime, timedelta
import re

# ---------------------------------------------------------------------------
# 1. 딕셔너리 데이터 (키워드→스몰카테고리, 스몰카테고리→라지카테고리, 감성 분석 단어)
# ---------------------------------------------------------------------------
# 예시 데이터 (실제 데이터에 맞게 확장)
keyword_small_category = {
    'keyword': [
        '외관', '전면', '휠', '손잡이', '와이드', '사이즈', '미터', '그릴', '루프', '램프', '도어', '배기구', '크기', '측면', '본넷', '범퍼', '휀더', '사이드미러', '필러', 
        '스포일러', '사이드스커트', '몰딩', '헤드라이트', '후미등', '안개등', '크롬', 'LED', '주간주행등', '방향지시등', '라이트바', '휠베이스', '타이어', '림', '선루프', 
        '파노라마', '루프랙', '보닛', '리어', '프런트', '에어 인테이크', '휀더라인', '테일게이트', '유리', '윈도우', '조명', '디스플레이', '계기판', '터치스크린', 
        '센터페시아', '버튼', '조작부', '앰비언트', '무드등', '독서등', '풋라이트', '시트', '가죽', '전동', '통풍', '열선', '리클라이닝', '버킷', '헤드레스트', '소재', 
        '우드', '알칸타라', '메탈', '카본', '스웨이드', '콘솔', '송풍구', '터치 버튼', '인포테인먼트', '대시보드', '센터 콘솔', '디자인', '흰색', '검은색', '화이트', 
        '블랙', '럭셔리', '모던', '컬러', '메탈릭', '무광', '유광', '투톤', '블루', '레드', '실버', '골드', '브라운', '카키', '베이지', '퍼플', '클래식', '퓨처리스틱', 
        '스포츠', '프리미엄', '하이테크', '심플', '엣지', '레트로', '우드그레인', '가죽마감', '다이아몬드', '스티칭', '하이글로시', '새틴', '광택', '펄', '투명코트', '스모키', 
        '고급스러움', '스포티', '모던함', '배색', '텍스처', '가속', '속도', '제로백', '시속', '속력', '터보차저', '배기량', 'RPM', '변속', '출력', '핸들링', '스티어링', 
        '조향', '코너링', '민첩성', '코너링 안정성', '롤링 억제', '서스펜션', '균형', '반응 속도', '핸들', '승차감', '소음', '운동', '하체', '강성', '드라이빙', '브레이크', 
        '노면 반응', '서스펜션 반응', '댐핑', '진동', '엔진', '토크', '구동', '기어', '변속기', '6단', '5단', '8단', '7단', '배기 시스템', '모터', 'ADAS', '아다스', 'ICCU', 
        '차선 유지', '차간 거리 유지', '긴급 브레이크', '급제동', '스마트센스', 'ABS', 'ESC', 'TCS', 'EBD', '보조', '경고', '센서', '감지', '비상 제공', '스마트 크루즈', 
        '자동 차선', '전방 추돌', '효율', '연비', '연료', '가솔린', '휘발유', '디젤', '경유', '하브', '충전', '전비', '에너지', '절약', '보험료', '수리', '부품', '소모품', 
        '정비', '소모성', '점검', '구매', '값', '가성비', '감가', '중고차 가치', '보조금', '보증기간', '장기', '보증', '만원', '비용', '세금', '주차', '출고가', '중고', 
        '리세일', '밸류', '레그룸', '헤드룸', '탑승', '좌석', '1열', '2열', '3열', '운전석', '조수석', '배열', '팔걸이', '뒷좌석', '앞좌석', '착좌', '등받이', '각도', 
        '트렁크', '수납', '용량', '시트 폴딩', '암레스트', '컵홀더', '슬라이딩', '차박', '무게', '다용도', '활용도', '조절', '확장성', '차량 구조', '프레임', '하부', 
        '강도', '차체', '내구성', '에어백', '임팩트', '보호', '충돌', '충격', '안정', '긴급 보호', '흡수', '카메라', '블라인드', '야간', '사고'
    ],
    'small_category': [
        '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', 
        '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '외관', '내관', '내관', '내관', '내관', 
        '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '내관', '스타일', '스타일', '스타일', 
        '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', 
        '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '스타일', '속도', '속도', '속도', 
        '속도', '속도', '속도', '속도', '속도', '속도', '핸들링', '핸들링', '핸들링', '핸들링', '핸들링', '핸들링', '핸들링', '핸들링', '핸들링', '주행감', '주행감', 
        '주행감', '주행감', '주행감', '주행감', '주행감', '주행감', '주행감', '주행감', '동력', '동력', '동력', '동력', '동력', '동력', '동력', '동력', '동력', '동력', 
        '주행 보조', '주행 보조', '주행 보조', '주행 보조', '주행 보조', '주행 보조', '주행 보조', '주행 보조', '주행 보조', '주행 보조', '주행 보조', '연비', '연비', 
        '연비', '연비', '연비', '연비', '연비', '연비', '연비', '연비', '연비', '유지비', '유지비', '유지비', '유지비', '유지비', '유지비', '유지비', '유지비', '가격', 
        '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '가격', '실내', '실내', '실내', '실내', 
        '실내', '실내', '실내', '실내', '실내', '실내', '실내', '실내', '실내', '실내', '실내', '적재', '적재', '적재', '적재', '적재', '활용도', '활용도', '활용도', 
        '활용도', '활용도', '활용도', '활용도', '활용도', '활용도', '구조', '구조', '구조', '구조', '구조', '구조', '안정성', '안정성', '안정성', '안정성', '안정성', '안정성', 
        '감지', '감지', '감지', '감지'
    ]
}

small_category_large_category = {
    'small_category': ['외관', '내관', '스타일', '속도', '핸들링', '주행감', '동력', '주행 보조', '연비', '유지비', '가격', '실내', '적재', '활용도', '구조', '안정성', '감지'],
    'large_category': ['디자인', '디자인', '디자인', '퍼포먼스', '퍼포먼스', '퍼포먼스', '퍼포먼스', '퍼포먼스', '경제성', '경제성', '경제성', '공간', '공간', '공간', '안전', '안전', '안전']
}


# SparkSession 생성 (이미 생성되어 있다면 생략)
spark = SparkSession.builder.appName("Transform").getOrCreate()

# ----- 1. 기본 설정 -----
# 오늘 날짜 (어제 날짜)
today = datetime.now().strftime("%Y-%m-%d")
#today = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

bucket = "hmg5th-4-bucket"
contents_path = f"s3a://{bucket}/merge_data/contents/{today}.parquet"
comments_path = f"s3a://{bucket}/merge_data/comments/{today}.parquet"

# S3에서 CSV 파일 읽기 (옵션은 실제 환경에 맞게 조정)
df_contents = spark.read.option("header", True).parquet(contents_path)
df_comments = spark.read.option("header", True).parquet(comments_path)

# ----- 2. 전처리: 컬럼 삭제, 결측치 제거, 텍스트 정제 -----
# 불필요한 컬럼 제거 및 null 제거
df_contents = df_contents.drop("author", "hates") \
    .filter(F.col("title").isNotNull() & F.col("content").isNotNull())

df_comments = df_comments.filter(F.col("comment").isNotNull())

df_contents = df_contents.withColumn(
    "datetime", 
    (F.unix_timestamp("datetime", "yyyy-MM-dd HH:mm:ss") * 1000000000)  # 초를 나노초로 변환
).withColumn(
    "likes", F.col("likes").cast("int")
).withColumn(
    "views", F.col("views").cast("int")
).withColumn(
    "comments_count", F.col("comments_count").cast("int")
)


# ----- 3. 화제도(popularity) 계산 -----
# 기준 데이터 (작은 테이블이므로 브로드캐스트 사용)
data_stats = {
    "clien": {"avg_likes": 1.2, "avg_views": 4500, "avg_comments_count": 13},
    "fmkorea": {"avg_likes": 7, "avg_views": 180, "avg_comments_count": 8},
    "bobae": {"avg_likes": 2, "avg_views": 450, "avg_comments_count": 6},
    "dcinside": {"avg_likes": 1, "avg_views": 65, "avg_comments_count": 4}
}
broadcast_stats = spark.sparkContext.broadcast(data_stats)

# UDF로 popularity 계산 (site가 data_stats에 없으면 0 반환)
def calc_popularity(site, likes, views, comments_count):
    stats = broadcast_stats.value.get(site)
    if stats:
        return (float(likes) / stats["avg_likes"]) * 0.4 + \
               (float(views) / stats["avg_views"]) * 0.2 + \
               (float(comments_count) / stats["avg_comments_count"]) * 0.4
    return 0.0

popularity_udf = F.udf(calc_popularity, T.DoubleType())

df_contents = df_contents.withColumn("popularity", 
    popularity_udf(F.col("site"), F.col("likes"), F.col("views"), F.col("comments_count"))
)

# ----- 4. 댓글 병합 및 텍스트 생성 -----
# URL 별 댓글 합치기 (공백으로 연결)
df_comments_grouped = df_comments.groupBy("url") \
    .agg(F.concat_ws(" ", F.collect_list("comment")).alias("comment_agg"))

# df_contents와 조인 (왼쪽 조인, 댓글 없는 경우 빈 문자열 채움)
df_merged = df_contents.join(df_comments_grouped, on="url", how="left") \
    .withColumn("comment_agg", F.coalesce(F.col("comment_agg"), F.lit("")))

# 전체 텍스트 생성: title + content + comment_agg
df_merged = df_merged.withColumn("text", 
    F.concat_ws(" ", F.col("title"), F.col("content"), F.col("comment_agg"))
)

# 필요 없는 컬럼 제거 (content, comment_agg, comments_count, likes)
df_merged = df_merged.select("url", "site", "datetime", "model", "title", "views", "popularity", "text")

# ----- 5. 키워드 및 감성 분석 데이터 로드 -----
# 키워드-소분류, 소분류-대분류 데이터 (dictonary to df)
df_keyword_small = spark.createDataFrame(
    zip(keyword_small_category["keyword"], keyword_small_category["small_category"]),
    schema=["keyword", "small_category"]
)

df_small_large = spark.createDataFrame(
    zip(small_category_large_category["small_category"], small_category_large_category["large_category"]),
    schema=["small_category", "large_category"]
)

# 키워드 리스트 추출 및 브로드캐스트
keywords = [row["keyword"] for row in df_keyword_small.select("keyword").distinct().collect()]
broadcast_keywords = spark.sparkContext.broadcast(keywords)

# UDF: 텍스트에서 키워드 매칭 (리스트 반환, 매칭 없으면 None)
def find_keywords(text):
    if text:
        matched = [kw for kw in broadcast_keywords.value if kw in text]
        return matched if matched else None
    return None

find_keywords_udf = F.udf(find_keywords, T.ArrayType(T.StringType()))

df_merged = df_merged.withColumn("matched_keywords", find_keywords_udf(F.col("text"))) \
    .filter(F.col("matched_keywords").isNotNull())

# ----- 6. 키워드 DataFrame 생성 -----
# 각 행마다 매칭된 키워드를 개별 행으로 전개 (explode)
df_keywords = df_merged.select("model", "url", "title", "popularity", "text", "matched_keywords") \
    .withColumn("keyword", F.explode("matched_keywords")) \
    .drop("matched_keywords", "text")

# 작은 데이터셋은 broadcast join 활용
# 소분류 정보 join (키: keyword)
df_keywords = df_keywords.join(
    F.broadcast(df_keyword_small.select("keyword", "small_category")),
    on="keyword",
    how="left"
)

# 대분류 정보 join (키: small_category)
df_keywords = df_keywords.join(
    F.broadcast(df_small_large.select("small_category", "large_category")),
    on="small_category",
    how="left"
)
# 최종 컬럼 순서 조정
df_keywords = df_keywords.select("model", "url", "title", "keyword", "small_category", "large_category", "popularity")

# ----- 7. 감성 분석 -----
# 감성 단어 리스트 (정규표현식 패턴으로 결합)
sentiment_json = {
  "positive": [
    "좋다", "기쁘다", "사랑하다", "행복", "즐겁다", "훌륭", "최고", "아름", "멋지다", "감사", "좋아하다", 
    "신났다", "환상적", "기대", "긍정", "고맙다", "보람", "안심", "만족", "잘하다", "대박", "짱", "존좋", 
    "완전", "꿀잼", "대단해", "짱짱", "굿", "이상적", "감동", "정말", "대박", "잘한",
    "귀엽다", "다행", "원하는", "자랑", "유쾌", "편한", "잘 되었다", "확신", "편안", "소중", "좋았어", "완벽", 
    "완전", "이쁨", "예쁨", "예쁘다", "멋진", "괜찮", "인정", "잘함", "잘해서", "잘하니까", "트렌디", "스포티", 
    "좋은", "좋고", "좋아서", "좋았고", "좋을까", "좋으면", "좋더라", "좋네요", "좋겠다", "좋았던",
    "즐거", "즐겁", "멋지고", "멋져서", "멋졌어", "멋졌네요", "멋있"
    "멋질까", "멋진가", "편하고", "편해서", "편했어", "편했네", "편할까", "편해", "소중" "예쁜", "예쁘고", 
    "예뻐서", "예뻤어", "예쁘네요", "예쁠까", "예뻤던", "이쁜", "이쁘고", "이쁘네"
  ],
  "negative": [
    "나쁘", "슬프", "짜증", "화나다", "실망", "불만", "불쾌", "귀찮", "불편", "못하", "실수하다", "지루하다", 
    "아프다", "문제", "실패", "부정적", "미워하다", "엉망", "걱정", "불안", "혐오", "고통", "지치다", "억울", 
    "괴롭다", "잘못", "괴로워", "어렵다", "개새끼", "XX", "씹", "좆", "개판", "좆밥", "개같다", "씨발", "좆같다", "염병", 
    "씹새끼", "까불다", "좆나", "지랄", "쓰레기", "미친", "X끼", "개X", "빨리", "좆될", 
    "시X", "병X", "구라", "사기", "정신병", "뻘짓", "븅신", "머저리", "뒤지다", "병X새끼", "개졸라",
    "좆망", "좆밥들", "좆같은", "시발", "사기꾼", "후회",
    "젠장", "하아", "헛소리", "엿먹어라", "병신", "망한", "망했", "잘못", "망할", "망할지도",
    "나쁜", "나빠서", "나빴", "나쁠까", "짜증", "화난", "화나고", "화나서", "화났", "화날까",
    "못하", "못한", "별로", "못해서", "못했어", "못할까", "못할지도", "지루", "부정", "혐오", "고통" 
    "지친", "지치고", "지쳐서", "지쳤어", "지칠까", "지쳤다",
    "괴로운", "괴롭고", "괴로워서", "괴로웠어", "괴롭네", "괴로울까",
    "잘못", "망하다", "망하고", "망해서", "망했어", "망할까", "망할지도"
  ]
}
# 두 리스트를 정규식 패턴으로 결합 (대소문자 구분 여부는 필요에 따라 조정)
positive_pattern = "|".join(sentiment_json["positive"])
negative_pattern = "|".join(sentiment_json["negative"])

# UDF: 텍스트 내에서 정규식 패턴에 해당하는 단어 개수 세기
def count_occurrences(text, pattern):
    if text:
        return len(re.findall(pattern, text))
    return 0

count_occurrences_udf = F.udf(count_occurrences, T.IntegerType())

df_merged = df_merged.withColumn("positive", count_occurrences_udf(F.col("text"), F.lit(positive_pattern))) \
                     .withColumn("negative", count_occurrences_udf(F.col("text"), F.lit(negative_pattern)))

# df_sentiment: model, url, positive, negative
df_sentiment = df_merged.select("model", "url", "positive", "negative")
# text 컬럼은 이후 삭제 (이미 사용한 경우)
df_merged = df_merged.select("site", "datetime", "model", "title", "url", "popularity", "views", "positive", "negative")

df_keywords.cache()
# ----- 8. 데이터 집계 -----
# (1) 소분류별 집계: model, large_category, small_category별 popularity 합계 - live_popularity.parquet
df_small_category = df_keywords.groupBy("model", "large_category", "small_category") \
    .agg(F.sum("popularity").alias("popularity_sum")) \
    .orderBy("model", "large_category")

# (2) 게시글-소분류: df_merged (model, url, title, popularity)와 키워드 테이블의 small_category (중복 제거 후 조인) live_title.parquet
df_key_url = df_keywords.select("url", "keyword", "small_category", "large_category").dropDuplicates(["url", "small_category"])
df_post_small_category = df_merged.select("model", "url", "title", "popularity") \
    .join(df_key_url.select("url", "small_category"), on="url", how="left") \
    .orderBy("url", F.col("popularity").desc())

# (3) 대분류 감성 집계: df_keywords와 df_sentiment를 조인 후, model, large_category별 positive, negative 합계 live_sentiment.parquet
df_category_sentiment = df_keywords.join(df_sentiment, on=["model", "url"], how="left") \
    .groupBy("model", "large_category", "small_category") \
    .agg(F.sum("positive").alias("positive_sum"),
         F.sum("negative").alias("negative_sum"))

# (4) 키워드 언급 집계: model, keyword별 popularity 합계
df_keyword_mentions = df_keywords.groupBy("model", "keyword") \
    .agg(F.sum("popularity").alias("popularity_sum"))

# (5) popularity 15 이상 게시물 검출
filtered_df = df_contents.select("title", "url", "popularity").filter(F.col("popularity") >= 15)
# 필터링된 결과가 존재하는지 확인
if filtered_df.count() > 0:  # 데이터가 있는 경우에만 저장
    alarm_path = "s3a://hmg5th-4-bucket/transformed_data/alarm/"
    # CSV 파일로 저장 (헤더 포함)
    filtered_df.write.mode("overwrite").option("header", "true").csv(alarm_path)

# (5)
df_keyword = df_keywords.select("url", "keyword", "small_category", "large_category")

# save
output_base = f"s3a://hmg5th-4-bucket/transformed_data/{today}/"

df_merged.write.mode("overwrite").parquet(output_base + "post.parquet")
df_keyword.write.mode("overwrite").parquet(output_base + "keyword.parquet")
df_small_category.write.mode("overwrite").parquet(output_base + "live_popularity.parquet")
df_post_small_category.write.mode("overwrite").parquet(output_base + "live_category.parquet")
df_category_sentiment.write.mode("overwrite").parquet(output_base + "live_sentiment.parquet")
