
# Cài đặt các thư viện cần thiết
# =================================================== 
from selenium import webdriver 
from selenium.webdriver.common.by import By # Cung cấp các constants để tìm kiếm các phần tử trong HTML
import undetected_chromedriver as uc # Sử dụng undetected_chromedriver để tránh bị phát hiện là bot
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import time

#==================================================
# Cấu hình tránh các web phát hiện là bot
# ================ Thiết lập các tùy chọn cho trình duyệt ================
def configure_browser():
    options = uc.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--start-maximized')
    
    return uc.Chrome(options=options)

def get_all_hrefs_from_page(url, browser):
        browser.get(url) # Mở trang web
        WebDriverWait(browser, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js__product-link-for-product-id'))
        )

        elements = browser.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id') # Tìm tất cả các phần tử có class 'js__product-link-for-product-id'
        hrefs = [element.get_attribute('href') for element in elements] #Lấy tất cả các thuộc tính href của các phần tử
        return hrefs # Trả về danh sách các hrefs

# ==========================================================

def crawl_all_hrefs(base_url, output_file_path):
    browser = configure_browser()
    page = 1
    all_hrefs = 0
    written_hrefs = set()

    try:
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            while True:
                print(f"Đang cào dữ liệu trang số {page}...")
                url_with_page = f"{base_url}/p{page}" if page > 1 else base_url
                hrefs = get_all_hrefs_from_page(url_with_page, browser)
                if not hrefs:
                    print(f"Không tìm thấy hrefs trên trang {page}. Dừng cào dữ liệu.")
                    break

                for href in hrefs:
                    if href and href not in written_hrefs:
                        written_hrefs.add(href)
                        output_file.write(href + '\n')
                        all_hrefs += 1
                        print(f"Đã ghi href: {href}")
                output_file.flush()

                next_page = browser.find_elements(By.CSS_SELECTOR, 'a.re__pagination-icon:not(.re__pagination-icon--no-effect)')
                if not next_page:
                    print("Không tìm thấy trang tiếp theo. Dừng cào dữ liệu.")
                    break

                page += 1
                time.sleep(3)
    finally:
        browser.quit()

    print(f"Tổng số hrefs đã cào được: {all_hrefs}")
    print(f"Đã lưu tất cả các href vào file '{output_file_path}'.")