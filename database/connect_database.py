import psycopg2

from crawler_bds.detail_scraping import *

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            database = "house_price_prediction",
            user = "postgres",
            password = "11042005",
            port = "5432"
            )
        cur = conn.cursor()
        print("Kết nối đến cơ sở dữ liệu thành công!")
        return conn, cur
    except Exception as e:
        print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
        return None, None
    
# Biến toàn cục để lưu kết nối
conn, cur = connect_to_database()

# --- Tạo bảng ---
def create_table():
    if conn is not None and cur is not None:
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS raw_property_data (
                id SERIAL PRIMARY KEY,
                title TEXT,
                link TEXT,
                address TEXT,
                price_per_m2 TEXT,
                area TEXT,
                num_bedrooms TEXT,
                num_bathrooms TEXT,
                legal TEXT,
                furniture TEXT,
                balcony_direction TEXT,
                house_direction TEXT,
                posted_date TEXT,
                expiry_date TEXT,
                fluctuation TEXT
            );
            """
            cur.execute(create_table_query)
            conn.commit()
            print("Bảng raw_property_data đã được tạo.")
        except Exception as e:
            print(f"Lỗi khi tạo bảng: {e}")

def drop_table():
    if conn is not None and cur is not None:
        try:
            drop_table_query = "DROP TABLE IF EXISTS raw_property_data;"
            cur.execute(drop_table_query)
            conn.commit()
            print("Bảng raw_property_data đã được xóa.")
        except Exception as e:
            print(f"Lỗi khi xóa bảng: {e}")


# --- Mapping dữ liệu ---
def map_data_to_table(data):
    if conn is not None and cur is not None:
        try:
            insert_query = """
            INSERT INTO raw_property_data (
                title, link, address, price_per_m2, area, num_bedrooms,
                num_bathrooms, legal, furniture, balcony_direction,
                house_direction, posted_date, expiry_date, fluctuation
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (
                data.get('Tiêu đề'),
                data.get('Đường dẫn'),
                data.get('Địa chỉ'),
                data.get('Giá/m²'),
                data.get('Diện tích'),
                data.get('Số phòng ngủ'),
                data.get('Số phòng tắm'),
                data.get('Pháp lý'),
                data.get('Nội thất'),
                data.get('Hướng ban công'),
                data.get('Hướng nhà'),
                data.get('Ngày đăng'),
                data.get('Ngày hết hạn'),
                data.get('Biến động/năm')
            )
            cur.execute(insert_query, values)
            conn.commit()
            print("Dữ liệu đã được chèn vào bảng raw_property_data.")
            print("===============================================")
        except Exception as e:
            print(f"Lỗi khi chèn dữ liệu: {e}")

