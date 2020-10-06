Tool chuyển datasample (wav, text) vào file excel
Cách sử dụng :
B1: Giải nén tệp tin Transcript.rar
B2: Mở terminal hoặc command line tại thư mục giải nén
B3: chạy chương trình bằng cách gõ :
python main.py [-h] -i IN.txt -o OUT.csv
hoặc
python main.py [-h] -in IN.txt -out OUT.csv
Với các tham số : IN.txt là tập tin chứa path và transcript, OUT.csv là tập tin excel cần xuất ra (Các mẫu có sẵn trong file nén)