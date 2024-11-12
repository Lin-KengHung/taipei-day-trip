import chardet

# 檢測檔案編碼
def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result

file_path = "taipei_day_trip.sql"
encoding_info = detect_file_encoding(file_path)
print(f"File Encoding: {encoding_info}")
