from time import sleep
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# 계정
_ID = '...'
_PASSWORD = '...'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
chrome_options = webdriver.ChromeOptions()
# 브라우저 꺼짐 방지코드
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")

print("#### 성남도시개발공사 사이트 접근 ####")

for i in range(3):
    print(".")

url = 'https://spo.isdc.co.kr/courseRegist.do'
driver.get(url)
driver.set_window_size(1000, 1000)
# driver.maximize_window()
# quit()

print("#### 로그인 여부 체크 ####")

# logSession 비어있으면
if not driver.find_element(By.ID, 'logSession').get_attribute('value'):
    print("[logout 상태]")
    print("...login 중...")
    driver.get("https://spo.isdc.co.kr/login.do")
    driver.find_element(By.ID, 'mbId').send_keys(_ID)
    driver.find_element(By.ID, 'mbPw').send_keys(_PASSWORD)

    driver.find_element(By.ID, 'loginBtn').click()
    # 로그인 Alert 닫기
    WebDriverWait(driver,3).until(ec.alert_is_present())
    alert = driver.switch_to.alert

    # 확인
    alert.accept()

driver.get(url)
print("[login 완료]")

for i in range(3):
    print(".")


while True:
    print("#### 수강신청 페이지 접근 ####")
    print("#### 강의내역 조회 ####")

    ## 조건설정

    # 평생스포츠센터
    center = Select(driver.find_element(By.ID, 'center'))
    center.select_by_value("05") 
    # 수영
    event = Select(driver.find_element(By.ID, 'event'))
    event.select_by_value("01") 
    # 조기수영
    swimClass = Select(driver.find_element(By.ID, 'class'))
    swimClass.select_by_value("010001")
    # 성인
    target = Select(driver.find_element(By.ID, 'target'))
    target.select_by_value("01") 

    # 조회
    driver.find_element(By.ID, 'submit').click() 

    sleep(2)

    # 접수버튼 위치 찾기
    table = driver.find_element(By.XPATH, '//*[@id="table_list_info"]/tbody')

    testTr = ""
    testTd = ""
    testClassName = ""
    testClassTime = ""
    testFlag = True

    driver.implicitly_wait(3)

    print("#### 강의 오픈여부 검사 ####")
    for testTr in table.find_elements(By.TAG_NAME, 'tr'):
        testTd = testTr.find_elements(By.TAG_NAME, 'td')
        testClassName = testTd[3].text
        testClassTime = testTd[4].text
        if ((testClassTime.find("06:00") != -1) 
            and (testClassName.find("상급반") != -1)):
            print("# 강의 검색 : " + testClassName + "[" + testClassTime + "]")
            if(testTd[8].get_attribute('innerText') == "신청"):
                print("# 오픈 강의 : " + testClassName + "[" + testClassTime + "]")
                testFlag = True
                break
            # else:
            #     print("# 미오픈 강의 : " + testClassName + "[" + testClassTime + "]")
            #     testFlag = False    

    # '신청' 이 아니면 새로고침
    if not testFlag:
        print("#### 강의 미오픈 ####")
        for i in range(3):
                print(".")
        # sleep(120)
        driver.refresh()
        driver.implicitly_wait(1)
        
    else: 
        print("#### 강의 오픈  ####")
        print("#### 매크로 실행 ####")
        ## 6-7시꺼부터 노리기
        for tr in table.find_elements(By.TAG_NAME, 'tr'):
            td = tr.find_elements(By.TAG_NAME, 'td')
            className = td[3].text
            classTime = td[4].text
            if ((classTime.find("06:00") != -1) # 6시 && 상급반 타임 탐색
                and (className.find("상급반") != -1)):
                print(td[3].text)
                # 버튼 글자가 '신청' 인지 조건 걸어야 함
                if(td[8].get_attribute('innerText') == "신청"): 
                    print("[Click 이벤트 발생] : " + td[8].get_attribute('innerText')) 
                    td[8].click()
                    try: 
                        WebDriverWait(driver,3).until(ec.alert_is_present())
                        alert = driver.switch_to.alert
                        # 확인
                        alert.dismiss()
                        print("[Alert 이벤트 발생] : " + td[3].text)

                    except:
                        print("[Alert 이벤트 미발생]")
            print("================================================")
        print("#### 조회 성공 ####")     

        for i in range(3):
                print(".")
        break

print("#### 프로그램 종료 ####")   

driver.implicitly_wait(5)
sleep(3)
