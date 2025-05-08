# Web Scraper cho Tin Tức Văn Hóa nhandan.vn

Dự án này là một công cụ cào dữ liệu web đơn giản, được viết bằng Python, để lấy các bài viết tin tức từ mục văn hóa của trang [nhandan.vn](https://nhandan.vn/vanhoa/). Công cụ sẽ trích xuất tiêu đề, tóm tắt, nội dung và URL hình ảnh, sau đó lưu vào file Excel với định dạng tự động.

## Mục Lục
- [Mô Tả Dự Án](#mô-tả-dự-án)
- [Tính Năng](#tính-năng)
- [Tải Dự Án Về Máy](#tải-dự-án-về-máy)
- [Liên Hệ](#liên-hệ)

## Mô Tả Dự Án
Dự án này giúp bạn lấy tin tức từ trang nhandan.vn (phần văn hóa) và lưu vào file Excel. File Excel sẽ có các cột như "Tiêu đề", "Tóm tắt", "Nội dung", "Hình ảnh".

## Tính Năng
- Cào dữ liệu tin tức từ https://nhandan.vn/vanhoa/.
- Hỗ trợ phân trang (nếu có) để thu thập bài viết từ nhiều trang.
- Trích xuất tiêu đề, tóm tắt, nội dung và URL hình ảnh từ mỗi bài viết.
- Giới hạn số lượng bài viết tối đa có thể cấu hình (mặc định: 50 bài).
- Lưu dữ liệu vào file Excel .
- Bao gồm xử lý lỗi cho các yêu cầu thất bại và vấn đề phân tích cú pháp.
- Thêm độ trễ giữa các yêu cầu để tránh bị chặn bởi trang web.

## Tải Dự Án Về Máy
Để bắt đầu, bạn cần
   - Cài đặt Git từ trang chính thức: "https://github.com/quocviet7624/baitaplonttnhandan_lqv.git"
   - Download Zip
   - Sau khi cài xong
   - Vào Thư Mục Dự Án
   - Cài Đặt Các Thành Phần Cần Thiết
   1 . Cài Đặt Thư Viện Python
   Cài các thư viện cần thiết: requests, beautifulsoup4, pandas, và openpyxl bằng lệnh:
   pip install requests beautifulsoup4 pandas openpyxl

   2 . Chạy Chương Trình
   python vanhoa.py

   3 . Theo Dõi Tiến Trình
    Chương trình sẽ in log:
    Số lượng link bài viết tìm được.
    Tiêu đề và URL hình ảnh của từng bài.
    Tên file Excel được tạo.
    Quá trình cào có thể mất vài phút tùy số lượng bài.
    Kiểm Tra Kết Quả
    File Excel (ví dụ: tin_tuc_20250508_173000.xlsx) sẽ được tạo trong thư mục dự án.
    Mở file để xem các cột: "Tiêu đề", "Tóm tắt", "Nội dung", "Hình ảnh". 
## Liên hệ
 Tác giả : Lê Quốc Việt
 Email: lequocviet76st@gmail.com
