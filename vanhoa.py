import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
5
# 1 chọn trang Website tin tức https://nhandan.vn/ 
# 2 Click chọn một mục tin tức với danh mục văn hóa
# 3 Bấm tìm kiếm(nếu trang web tin tức không có Button tìm kiếm thì có thể bỏ qua).


def laytintuc(max_articles=50):
    base_url = "https://nhandan.vn/vanhoa/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }

    all_links = set() 
    page = 1
    has_next_page = True
# 5. Lấy tất cả dữ liệu của các trang.
    # Lặp qua các trang (nếu có)
    while len(all_links) < max_articles and has_next_page:
        url = f"{base_url}?page={page}" if page > 1 else base_url
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Không vào được trang {url}, mã trạng thái: {response.status_code}")
            break

        print(f"Đang lấy dữ liệu từ trang {page}...")
        soup = BeautifulSoup(response.content, "html.parser")

        # Tìm danh sách bài viết
        danh_sach_tin = soup.find_all('h3', class_='story__heading')
        if not danh_sach_tin:
            print("Không tìm thấy bài viết nào ở trang này!")
            break

        # Lấy các link bài viết
        links = []
        for tin in danh_sach_tin:
            a_tag = tin.find('a', href=True)
            if a_tag and 'href' in a_tag.attrs:
                link = a_tag['href']
                if not link.startswith('http'):
                    link = "https://nhandan.vn" + link if link.startswith('/') else link
                links.append(link)

        if not links:
            print("Không tìm thấy link nào ở trang này!")
            break

        all_links.update(links)
        print(f"Trang {page}: Tìm được {len(links)} link bài viết. Tổng cộng: {len(all_links)}")

        # Kiểm tra phân trang
        next_page = soup.find('a', class_='pagination-next')  # Tìm thẻ "Trang tiếp theo"
        if next_page and 'href' in next_page.attrs:
            page += 1
        else:
            print("Không có phân trang, chỉ có 1 trang.")
            has_next_page = False

        if len(all_links) >= max_articles:
            all_links = set(list(all_links)[:max_articles])
            break

        time.sleep(1)  # Chờ 1 giây giữa các trang để tránh bị chặn

    print(f"Tổng cộng tìm được {len(all_links)} link bài viết: {all_links}")
    
    
# 4. Lấy tất cả dữ liệu(Tiêu đề, Mô tả, Hình ảnh, Nội dung bài viết) hiển thị ở bài viết
    # Trích xuất dữ liệu từ từng bài viết
    data = []
    for link in all_links:
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            page_soup = BeautifulSoup(response.content, "html.parser")

            # Lấy tiêu đề
            title_tag = page_soup.find("h1", class_="article__title cms-title")
            title = title_tag.text.strip() if title_tag else ""

            # Lấy tóm tắt
            summary_tag = page_soup.find("div", class_="article__sapo cms-desc")
            summary = summary_tag.text.strip() if summary_tag else ""

            # Lấy nội dung
            body = page_soup.find("div", class_="article__body cms-body")
            content = body.get_text(separator="\n").strip() if body else ""

            # Lấy URL hình ảnh
            img_url = ""
            if body:
                first_img = body.find('img', class_='cms-photo')
                if first_img and 'src' in first_img.attrs:
                    img_url = first_img['src']

            data.append([title, summary, content, img_url])
            print(f"Đã lấy bài: {title} - Ảnh: {img_url}")

            time.sleep(1)  # Chờ 1 giây giữa các bài

        except Exception as e:
            print(f"Lỗi khi lấy bài {link}: {str(e)}")
            continue

# 6. Lưu dữ liệu đã lấy được vào file excel 
    if data:
        df = pd.DataFrame(data, columns=["Tiêu đề", "Tóm tắt", "Nội dung", "Hình ảnh"])
        time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"tin_tuc_{time_now}.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Đã lưu vào file {file_name} lúc {datetime.now().strftime('%H:%M %d/%m/%Y')}")
    else:
        print("Không có dữ liệu để lưu")

if __name__ == "__main__":
    print("Bắt đầu chạy scraper...")
    laytintuc()