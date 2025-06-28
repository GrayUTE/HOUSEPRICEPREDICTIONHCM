
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

options = uc.ChromeOptions() # Tạo một đối tượng ChromeOptions để cấu hình trình duyệt

# ================ Thiết lập các tùy chọn cho trình duyệt ================
# options.add_argument('--headless') # Chạy trình duyệt ở chế độ không hiển thị GUI
options.add_argument('--disable-extensions') # Vô hiệu hóa tất cả các extension trên trình duyệt
options.add_argument('--disable-gpu') # Tawsrt tăng tốc GPU
options.add_argument('--no-sandbox') # Tắt sandbox bảo mật của trình duyệt
options.add_argument('--disable-dev-shm-usage') # Vô hiệu hóa việc sử dụng bộ nhớ chia sẻ
options.add_argument('disable-blink-features=AutomationControlled') # ẩn dấu hiệu trình duyệt đang chạy bằng automation
options.add_argument('--ignore-certificate-errors') # Bỏ qua các lỗi chứng chỉ SSL
options.add_argument('--ignore-ssl-errors') # Bỏ qua các lỗi SSL
options.add_argument('--start-maximized') # Thiết lập kích thước cửa sổ trình duyệt

# ===================================================

# Lấy tất cả các đường dẫn đến bất động sản từ trang web

browser = uc.Chrome(options = options) # Khởi tạo trình duyệt chrome với Undetected chromedriver
def get_all_hrefs_from_page(url):
    browser.get(url) # Mở trang web
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'js__product-link-for-product-id'))
    )

    elements = browser.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id') # Tìm tất cả các phần tử có class 'js__product-link-for-product-id'
    hrefs = [element.get_attribute('href') for element in elements] #Lấy tất cả các thuộc tính href của các phần tử
    return hrefs # Trả về danh sách các hrefs

# ==========================================================

bdsHCM_url = "https://batdongsan.com.vn/nha-dat-ban-tp-hcm"
page = 1
all_hrefs = 0
written_hrefs = set()  # Sử dụng set để tránh ghi trùng lặp hrefs

with open('hrefs_batdongsan_hcm.txt', 'a', encoding='utf-8') as output_file:  
        while True:
            print(f"Đang cào dữ liệu trang số {page}...")
            url_with_page = f"{bdsHCM_url}/p{page}" if page > 1 else bdsHCM_url
            
            hrefs = get_all_hrefs_from_page(url_with_page)
            if not hrefs:
                print(f"Không tìm thấy hrefs trên trang {page}. Dừng cào dữ liệu.")

            # Ghi từng href ngay sau khi lấy được
            for href in hrefs:
                if href and href not in written_hrefs:  # Kiểm tra xem href đã được ghi chưa
                    written_hrefs.add(href)  # Thêm href vào set để tránh ghi tr
                    output_file.write(href + '\n')
                    all_hrefs += 1
                    print(f"Đã ghi href: {href}")
            output_file.flush()  # Ghi xuống file ngay lập tức
            
            # Kiểm tra còn nút next không
            next_page = browser.find_elements(By.CSS_SELECTOR, 'a.re__pagination-icon:not(.re__pagination-icon--no-effect)')
            if not next_page:
                print("Không tìm thấy trang tiếp theo. Dừng cào dữ liệu.")
                break

            page += 1
            time.sleep(3)

print(f"Tổng số hrefs đã cào được: {all_hrefs}")
browser.quit() # Đóng trình duyệt sau khi hoàn thành

print("Đã lưu tất cả các href vào file 'batdongsan_hcm.txt'.")