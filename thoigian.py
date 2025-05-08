import schedule
import time
import congnghe

def job():
    print("⏰ Bắt đầu lấy tin lúc 6h sáng")
    data = congnghe.laytintuc()
    if data:
        congnghe.save_to_file(data)
    else:
        print("❌ Không có dữ liệu để lưu")

# Lịch chạy 6h sáng mỗi ngày
schedule.every().day.at("06:00").do(job)

print("📅 Đang chạy lịch...")

while True:
    schedule.run_pending()
    time.sleep(60)
