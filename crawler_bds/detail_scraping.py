# Mô tả: Cào dữ liệu chi tiết bất động sản từ trang batdongsan.com.vn
# =====================================================================

# Cấu hình các thư viện cần thiết
from selenium.webdriver.common.by import By # Cung cấp các constants để tìm kiếm các phần tử trong HTML
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from database.connect_database import map_data_to_table
import time
import numpy as np

# Hàm lấy tất cả các href đưa về list từ file
# =====================================================================

def load_href_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        all_hrefs = [line.strip() for line in f if line.strip()]
    return all_hrefs

# Hàm lấy dữ liệu chi tiết bất động sản từ một href
# =====================================================================

def get_property_data_for_one_href(href, browser, max_retries=2):
    information = {
        # Tiêu đề
        'Tiêu đề': np.nan,
        # --- Link đến các bất động sản ---
        'Đường dẫn': href,
        
        # --- Thông tin cơ bản ---
        'Địa chỉ': np.nan,
        'Giá/m²': np.nan,  
        'Diện tích': np.nan,
        
        # --- Cấu trúc bất động sản ---
        'Số phòng ngủ': np.nan,
        'Số phòng tắm': np.nan,
        'Pháp lý': np.nan,
        'Nội thất': np.nan,
        
        # --- Thông tin về vị trí ---
        'Hướng ban công': np.nan,
        'Hướng nhà': np.nan,

        # --- Thời gian ---
        'Ngày đăng': np.nan,
        'Ngày hết hạn': np.nan,
       
        # --- Giá trị tham khảo ---
        'Biến động/năm': np.nan,
    }
    
    def try_find_element(find_function, retries=max_retries):
        attempt = 0
        while attempt <= retries:
            try:
                return find_function()
            except:
                if attempt < retries:
                    time.sleep(5)  # Chờ 5 giây trước khi thử lại
                    attempt += 1
                else:
                    return None

    # --- Lấy thông tin tiêu đề ---
    title_element = try_find_element(lambda: browser.find_element(By.CLASS_NAME, 're__pr-title'))
    if title_element:
        information['Tiêu đề'] = title_element.text.strip()
    
    # --- Thông tin cơ bản ---
    
    # Lấy địa chỉ
    address_element = try_find_element(lambda: browser.find_element(By.CLASS_NAME, 're__pr-short-description'))
    if address_element:
        information['Địa chỉ'] = address_element.text.strip()
    
    # Lấy giá/m²
    price_per_m2_element = try_find_element(lambda: browser.find_element(By.CSS_SELECTOR, 'div.re__pr-short-info-item.js__pr-short-info-item span.ext'))
    if price_per_m2_element:
        information['Giá/m²'] = price_per_m2_element.text.strip()
    
    # Lấy diện tích
    area_element = try_find_element(lambda: browser.find_element(By.XPATH, '//div[span[text() = "Diện tích"]]/span[@class = "value"]'))
    if area_element:
        information['Diện tích'] = area_element.text.strip()
    
    # --- Cấu trúc bất động sản ---
    
    # --- Số phòng ngủ ---
    room_element = try_find_element(lambda: browser.find_element(By.XPATH, '//div[span[text() = "Phòng ngủ"]]/span[@class = "value"]'))
    if room_element:
        information['Số phòng ngủ'] = room_element.text.strip()

    # --- Số phòng tắm ---
    bathroom_element = try_find_element(lambda: browser.find_element(
        By.XPATH,
        '//div[@class = "re__pr-specs-content-item"][span[text() = "Số phòng tắm, vệ sinh"]]/span[@class = "re__pr-specs-content-item-value"]'
    ))
    if bathroom_element:
        information['Số phòng tắm'] = bathroom_element.text.strip()
    
    # --- Pháp lý ---
    legal_element = try_find_element(lambda: browser.find_element(
        By.XPATH,
        '//div[contains(@class, "re__pr-specs-content-item")][span[contains(text(), "Pháp lý")]]/span[@class="re__pr-specs-content-item-value"]'
    ))
    if legal_element:
        information['Pháp lý'] = legal_element.text.strip()
    
    # --- Nội thất ---
    furniture_element = try_find_element(lambda: browser.find_element(
        By.XPATH,
        '//div[contains(@class, "re__pr-specs-content-item")][span[contains(text(), "Nội thất")]]/span[@class="re__pr-specs-content-item-value"]'
    ))
    if furniture_element:
        information['Nội thất'] = furniture_element.text.strip()

    # --- Thông tin về vị trí ---
    
    # --- Hướng ban công ---
    balcony_element = try_find_element(lambda: browser.find_element(
        By.XPATH,
        '//div[contains(@class, "re__pr-specs-content-item")][span[contains(text(), "Hướng ban công")]]/span[@class="re__pr-specs-content-item-value"]'
    ))
    if balcony_element:
        information['Hướng ban công'] = balcony_element.text.strip()
    
    # --- Hướng nhà ---
    house_element = try_find_element(lambda: browser.find_element(
        By.XPATH,
        '//div[contains(@class, "re__pr-specs-content-item")][span[contains(text(), "Hướng nhà")]]/span[@class="re__pr-specs-content-item-value"]'
    ))
    if house_element:
        information['Hướng nhà'] = house_element.text.strip()
    
    # --- Thời gian ---
    
    # --- Ngày đăng ---
    date_element = try_find_element(lambda: browser.find_element(
        By.XPATH,
        '//div[contains(@class, "re__pr-short-info-item")][span[contains(text(), "Ngày đăng")]]/span[@class="value"]'
    ))
    if date_element:
        information['Ngày đăng'] = date_element.text.strip()
    
    # --- Ngày hết hạn ---
    expiry_element = try_find_element(lambda: browser.find_element(
        By.XPATH,
        '//div[contains(@class, "re__pr-short-info-item")][span[contains(text(), "Ngày hết hạn")]]/span[@class="value"]'
    ))
    if expiry_element:
        information['Ngày hết hạn'] = expiry_element.text.strip()
    
    # --- Giá trị tham khảo ---
    fluctuation_percent = try_find_element(lambda: browser.find_element(By.CLASS_NAME, 'cta-number'))
    fluctuation_text = try_find_element(lambda: browser.find_element(By.CLASS_NAME, 'cta-text'))
    if fluctuation_percent and fluctuation_text:
        information['Biến động/năm'] = f"{fluctuation_percent.text.strip()} - {fluctuation_text.text.strip()}"
    
    return information

def get_property_data_for_all_href(hrefs, browser, max_retries=2):
    all_property_data = []
    for href in hrefs[6300:]:
        for attempt in range(max_retries + 1):
            try:
                print(f"Đang truy cập href thứ {hrefs.index(href) + 1}")
                print(f"Thử truy cập {href} lần {attempt + 1}")
                browser.get(href)
                WebDriverWait(browser, 6).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 're__pr-title'))
                )
                # browser.implicitly_wait(5)
                all_property_data.append(get_property_data_for_one_href(href, browser))
                print(f"Đã lấy được các trường dữ liệu từ {href}")
                map_data_to_table(all_property_data[0])
                all_property_data = []
                break
            except TimeoutException as e:
                if attempt < max_retries:
                    print(f"Timeout khi truy cập {href}: {e}. Thử lại sau 5 giây...")
                    time.sleep(5)
                else:
                    print(f"Không thể truy cập {href} sau {max_retries + 1} lần thử. Bỏ qua.")
                    break
        time.sleep(5)  # Chờ giữa các lần truy cập để tránh bị chặn