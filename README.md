# GoogleTranslateApi
Sử dụng Selenium, giả làm client để gọi api của google dịch
chạy cmd với lệnh python TranslateGoogleApi.py  --src_lang "<ngôn ngữ nguồn>" --tgt_lang "<ngôn ngữ đích>" --case 2 --file_name "<tên file.phần mở rộng>" --save_file_name "<tên file.phần mở rộng>"
<br/>
--src_lang: viết tắt của ngôn ngữ nguồn Ex: Việt Nam -> vi, English -> en
--tgt_lang: viết tắt của ngôn ngữ đích cần dịch sang
--file_name: file chứa các câu cần dịch ( chú ý các câu cần dịch phải tách nhau bởi dấu xuống dòng)
--save_file_name: file chứa dũ liệu lưu lại sau quá trình dịch (chú ý: cấu trúc trong file là <câu_dịch>Tab<câu_nguồn>

Ex: python TranslateGoogleApi.py  --src_lang "vi" --tgt_lang "lo" --case 2 --file_name "test.txt" --save_file_name "lo-vi.txt"
