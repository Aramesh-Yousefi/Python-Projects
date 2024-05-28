import sqlite3
import requests
from bs4 import BeautifulSoup

# اتصال به پایگاه داده SQLite
conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

# ایجاد جدول در پایگاه داده
cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    status TEXT,
                    code TEXT,
                    instructor TEXT,
                    type TEXT,
                    location TEXT,
                    duration TEXT,
                    fee TEXT,
                    weekdays TEXT,
                    start_date TEXT,
                    start_time TEXT,
                    link TEXT,
                    register TEXT,
                    coupon_code TEXT
                )''')

# ذخیره تغییرات در پایگاه داده
conn.commit()

url = 'https://arjang.ac.ir/calendar/full'

# دریافت محتوای صفحه وب
response = requests.get(url)

# بررسی درستی دریافت اطلاعات
if response.status_code == 200:
    # تحلیل HTML صفحه وب با استفاده از BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # یافتن همه ردیف‌های دارای کلاس 'fc-day-grid-event'
    events = soup.find_all(class_='fc-day-grid-event')
    
    # اضافه کردن اطلاعات هر دوره به جدول
    for event in events:
        status = event.find(class_='course-status').text.strip()
        code = event.find(class_='course-code').text.strip()
        instructor = event.find(class_='course-instructor').text.strip()
        type_ = event.find(class_='course-type').text.strip()
        location = event.find(class_='course-location').text.strip()
        duration = event.find(class_='course-duration').text.strip()
        fee = event.find(class_='course-fee').text.strip()
        weekdays = event.find(class_='course-weekdays').text.strip()
        start_date = event.find(class_='course-startdate').text.strip()
        start_time = event.find(class_='course-starttime').text.strip()
        link = event.find(class_='course-link').text.strip()
        register = event.find(class_='course-register').text.strip()
        coupon_code = event.find(class_='course-coupon-code').text.strip()
        
        # اضافه کردن اطلاعات به جدول
        cursor.execute('''INSERT INTO courses (status, code, instructor, type, location, duration, fee, weekdays, start_date, start_time, link, register, coupon_code)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (status, code, instructor, type_, location, duration, fee, weekdays, start_date, start_time, link, register, coupon_code))
        
        # ذخیره تغییرات در پایگاه داده
        conn.commit()
else:
    print('دریافت اطلاعات ناموفق بود. کد وضعیت:', response.status_code)

# بستن اتصال به پایگاه داده
conn.close()
