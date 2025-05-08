import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def laytintuc():
    url = "https://www.24h.com.vn/tin-tuc-cong-nghe-c453.html"
    response = requests.get(url)

    if response.status_code == 200:
        print("Đã vào được trang chính!")
        soup = BeautifulSoup(response.content, "html.parser")

        danh_sach_tin = soup.find_all('div', class_='cate-24h-car-news-rand__info')
        links = []

        for tin in danh_sach_tin:
            a_tag = tin.find('a')
            if a_tag and 'href' in a_tag.attrs:
                links.append(a_tag['href'])

        print(f"Tìm được {len(links)} link bài viết: {links}")

        if not links:
            print("Không tìm thấy bài viết nào! Kiểm tra selector hoặc trang web.")
            return

        data = []

        for link in links:
            try:
                full_url = link if link.startswith('http') else "https://www.24h.com.vn" + link.lstrip('/')
                page = requests.get(full_url)
                page_soup = BeautifulSoup(page.content, "html.parser")

                title_tag = page_soup.find("h1", class_="clrTit bld tuht_show")
                title = title_tag.text.strip() if title_tag else ""

                summary_tag = page_soup.find("h2", class_="cate-24h-foot-arti-deta-sum ctTp tuht_show")
                summary = summary_tag.text.strip() if summary_tag else ""

                body = page_soup.find("article", class_="cate-24h-foot-arti-deta-info inpage-parent")
                content = body.decode_contents() if body else ""

                # Cập nhật: Lấy ảnh đầu tiên bất kỳ trong trang bài viết
                img_url = ''
                first_img = page_soup.find('img')
                if first_img and 'src' in first_img.attrs:
                    img_url = first_img['src']

                data.append([title, summary, content, img_url])
                print(f"Đã lấy bài: {title} - Ảnh: {img_url}")

            except Exception as e:
                print(f"Lỗi khi lấy bài {full_url}: {str(e)}")
                continue

        if data:
            df = pd.DataFrame(data, columns=["Tiêu đề", "Tóm tắt", "Nội dung", "Hình ảnh"])
            time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"tin_tuc_{time_now}.xlsx"
            df.to_excel(file_name, index=False)
            print(f"Đã lưu vào file {file_name}")
        else:
            print("Không có dữ liệu để lưu")
    else:
        print("Không vào được trang chính")

if __name__ == "__main__":
    print("Bắt đầu chạy scraper...")
    laytintuc()
