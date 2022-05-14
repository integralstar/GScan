# GScan

gscan.py (Google Hacking Scanner)

keyword_query - 키워드 검색

googlehacking_query - 패턴 사용

example) python3 gscan.py -k doc -d testsite.com

---------------------------------

run.py -d domain (스케쥴링 프로그램)

Google Search API(무료 100건 조회 가능)에 가입해야 함 (구글 계정 11개가 필요)

도메인 1개 풀스캔 대략 7일 소요 = 패턴 7200개 / (100건 조회 * 10개 계정)

---------------------------------

구글 계정 차단을 막기 위한 조치

1) proxy server list를 조회하여 속도가 빠른 순으로 정렬하여 사용 : chrome driver 설치 필요 후 설치 경로 변경 필요

2) IP 변경을 위해 Tor network 사용

가장 간단한 방법은 tor browser를 통한 접속.

리눅스 같은 환경에서는 라이브러리 설치를 권고

https://www.torproject.org/download/

3) random User-Agent 사용
