import schedule
import time
import vanhoa

def job():
    print("⏰ Bắt đầu lấy tin lúc 6h sáng")
    data = vanhoa.laytintuc()
    if data:
        vanhoa.save_to_file(data)
    else:
        print("❌ Không có dữ liệu để lưu")
# 7. Set lịch chạy vào lúc 6h sáng hằng ngày.
schedule.every().day.at("06:00").do(job)

print("📅 Đang chạy lịch...")

while True:
    schedule.run_pending()
    time.sleep(60)
