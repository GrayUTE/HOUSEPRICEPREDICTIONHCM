# main.py

from crawler_bds.get_listing_hrefs import  configure_browser
from crawler_bds.detail_scraping import load_href_from_file, get_property_data_for_all_href
from database.connect_database import create_table, drop_table

def main():
    # Cấu hình
    base_url = "https://batdongsan.com.vn/nha-dat-ban-tp-hcm"
    href_file_path = "all_hrefs/all_hrefs_bdshcm.txt"

    # Bước 1: Thu thập hrefs (chỉ chạy nếu cần cập nhật danh sách href)
    # crawl_all_hrefs(base_url, href_file_path)

    # Bước 2: Tạo bảng trong cơ sở dữ liệu
    create_table()

    # Bước 3: Lấy dữ liệu chi tiết từ các href
    browser = configure_browser()
    try:
        all_hrefs = load_href_from_file(href_file_path)
        get_property_data_for_all_href(all_hrefs, browser)
        
    finally:
        browser.quit()
    print("Hoàn thành việc lấy dữ liệu chi tiết từ các bất động sản.")

if __name__ == "__main__":
    main()
    # drop_table()  # Xóa bảng nếu cần