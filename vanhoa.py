import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def laytintuc(max_articles=50, max_pages=10):
    # Bước 1: Chọn trang tin tức: https://nhandan.vn/
    # Bước 2: Click chọn mục tin tức với danh mục văn hóa: https://nhandan.vn/vanhoa/
    # Bước 3: Không có nút tìm kiếm nên bỏ qua

    base_url = "https://nhandan.vn/vanhoa/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }

    all_links = set()

    # Bước 5: Lấy dữ liệu từ nhiều trang, lặp từ 1 đến max_pages
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}" if page > 1 else base_url
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Không vào được trang {url}, mã trạng thái: {response.status_code}")
            break

        print(f"Đang lấy dữ liệu từ trang {page}...")
        soup = BeautifulSoup(response.content, "html.parser")

        danh_sach_tin = soup.find_all('h3', class_='story__heading')
        if not danh_sach_tin:
            print("Không tìm thấy bài viết nào ở trang này!")
            break

        links = []
        for tin in danh_sach_tin:
            a_tag = tin.find('a', href=True)
            if a_tag:
                link = a_tag['href']
                if not link.startswith('http'):
                    link = "https://nhandan.vn" + link if link.startswith('/') else link
                links.append(link)

        if not links:
            print("Không tìm thấy link nào ở trang này!")
            break

        all_links.update(links)
        print(f"Trang {page}: Tìm được {len(links)} link bài viết. Tổng cộng: {len(all_links)}")

        if len(all_links) >= max_articles:
            break

        time.sleep(1)

    # Giới hạn số lượng bài viết
    all_links = list(all_links)[:max_articles]
    print(f"Tổng cộng lấy {len(all_links)} bài viết.")

    # Bước 4: Lấy tiêu đề, mô tả, hình ảnh, nội dung bài viết
    data = []
    for link in all_links:
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            page_soup = BeautifulSoup(response.content, "html.parser")

            title_tag = page_soup.find("h1", class_="article__title cms-title")
            title = title_tag.text.strip() if title_tag else ""

            summary_tag = page_soup.find("div", class_="article__sapo cms-desc")
            summary = summary_tag.text.strip() if summary_tag else ""

            body = page_soup.find("div", class_="article__body cms-body")
            content = body.get_text(separator="\n").strip() if body else ""

            img_url = ""
            if body:
                first_img = body.find('img', class_='cms-photo')
                if first_img and 'src' in first_img.attrs:
                    img_url = first_img['src']

            data.append([title, summary, content, img_url])
            print(f"Đã lấy bài: {title} - Ảnh: {img_url}")

            time.sleep(1)

        except Exception as e:
            print(f"Lỗi khi lấy bài {link}: {str(e)}")
            continue

    # Bước 6: Lưu dữ liệu vào Excel
    if data:
        df = pd.DataFrame(data, columns=["Tiêu đề", "Tóm tắt", "Nội dung", "Hình ảnh"])
        time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"tin_tuc_{time_now}.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Đã lưu vào file {file_name}")
    else:
        print("Không có dữ liệu để lưu.")

if __name__ == "__main__":
    print("Bắt đầu chạy scraper...")
    laytintuc()
