import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

# آدرس وب‌سایت مورد نظر
url = "https://arjang.ac.ir/instructors"

# ارسال درخواست به سایت و دریافت محتوای صفحه
response = requests.get(url)
html_content = response.content

# استفاده از BeautifulSoup برای پردازش محتوای HTML صفحه
soup = BeautifulSoup(html_content, "html.parser")

# یافتن عناصر حاوی اطلاعات اساتید
instructors_list = soup.find_all("div", class_="post-instructor")

# ایجاد یک شیء از کلاس FPDF
pdf = FPDF()
pdf.add_page()

# افزودن نام اساتید به فایل PDF
for instructor in instructors_list:
    # یافتن لینک مربوط به هر استاد
    link = instructor.find("a")
    # دریافت متن موجود در داخل تگ <a>
    name = link.text.strip()
    # افزودن نام استاد به فایل PDF
    pdf.cell(200, 10, txt=name, ln=True, align='L')

# ذخیره فایل PDF
pdf_output_path = "instructors_list.pdf"
pdf.output(pdf_output_path)

print("لیست اساتید با موفقیت در فایل PDF ذخیره شد: ", pdf_output_path)
