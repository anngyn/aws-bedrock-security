# Agentic SecOps Workshop — Hugo & GitHub Pages

Website: **https://anngyn.github.io/aws-bedrock-security/**

Site dùng Hugo **0.170.1** và theme [Relearn **9.5.2**](https://github.com/McShelby/hugo-theme-relearn/tree/9.5.2), có menu theo chương, tìm kiếm và chế độ sáng/tối. Đây là bản mirror cộng đồng của workshop AWS, có liên kết về nguồn ở mỗi trang.

Mục **Evidence gallery** chọn 21 ảnh tham khảo theo 6 module, gồm 6 ảnh bổ sung từ tài liệu công khai và 15 ảnh trong workshop. Các ảnh mô tả kết quả mẫu để đối chiếu khi làm lab. `evidence-catalog.json` lưu chú thích, thông tin đối chiếu và SHA-256; ảnh bổ sung nằm trong `static/evidence/`. Ảnh này không chứng minh một phiên lab cá nhân đã được thực thi.

## Chạy local

Cài Hugo 0.170.1 và Python 3.9 trở lên, rồi chạy trong thư mục repo:

```sh
python3 scripts/prepare_content.py
hugo server --baseURL http://localhost:1313/aws-bedrock-security/ --appendPort=false
```

Mở http://localhost:1313/aws-bedrock-security/.

Để build và kiểm tra:

```sh
python3 scripts/prepare_content.py
hugo --gc --minify
python3 scripts/verify_site.py
```

`content/` giữ nguyên nguồn AWS; script xác minh SHA-256 rồi chuyển cấu trúc chương, đường dẫn ảnh và liên kết sang `.hugo-content/`. Thư mục này được tạo lại khi build. `static/` được xuất dưới `/aws-bedrock-security/static/`. Các khối code được giữ nguyên.

## Triển khai

Trong **Settings → Pages**, chọn **GitHub Actions**. Workflow [pages.yaml](.github/workflows/pages.yaml) tự build, kiểm tra liên kết và triển khai sau mỗi lần push lên `main`. Cấu hình `baseURL` trong `hugo.toml` phải khớp địa chỉ Pages nếu đổi tên repo.

Theme được lưu trong `themes/hugo-theme-relearn/`, kèm license và tệp `THEME_SOURCE.json` ghi phiên bản/nguồn. Các GitHub Actions được cố định bằng commit SHA. Không cần dịch vụ trả phí hoặc tài khoản AWS để đọc website.

## Bản lưu offline

Mở `workshop.html` bằng Edge hoặc trình duyệt khác. File tự chứa nội dung và ảnh; không cần đăng nhập để đọc. Có mục lục, tìm nội dung theo chương và danh sách resource ở cuối trang.

- 26 trang tiếng Anh, gồm phần chuẩn bị, Module 0–6, các bài bonus và tổng kết.
- 165 ảnh/GIF riêng biệt và tệp `cfn-self-paced.yaml` đã lưu.
- 241 mục liên kết resource theo trang xuất hiện. Liên kết tới website ngoài vẫn cần Internet.
- Giữ nguyên văn bản/code nguồn; mỗi chương có mục “Exact original Markdown source”. Giao diện HTML được dựng lại để đọc offline. Sơ đồ Mermaid được giữ dưới dạng code nguồn.

## Nguồn và giới hạn xác minh

Nguồn công khai chính thức của AWS:
https://catalog.us-east-1.prod.workshops.aws/workshops/1ff65006-cc4a-48fd-99c9-3ef1e3d7a5ef/en-US

Build: `c4660d38-851e-45db-9894-729d4fa65763`.

Nội dung tổng quan và cấu trúc module khớp với workshop trong phiên sự kiện đã đăng nhập. Giao diện sự kiện không cung cấp build ID trong phần đã đọc, nên chưa xác minh được hai phiên bản trùng build hoàn toàn. Bản lưu không gồm thông tin tài khoản/credentials riêng của sự kiện.

Link gốc tới `cfn-self-paced.yaml` trả HTTP 403. Tệp đã được tải thành công từ đường dẫn của chính build công khai ở trên; HTML giữ link gốc trong danh sách resource và cung cấp bản tải local.

## Tệp đối chiếu

- `content/`: 26 tệp Markdown nguồn, giữ nguyên byte đã tải.
- `static/`: ảnh/GIF và template gốc.
- `manifest.json`, `metadata.json`, `published.json`: mô tả bản xuất bản của AWS.
- `resources.json`: liên kết gốc và trang xuất hiện.
- `source-downloads.json`, `asset-downloads.json`: URL, kích thước và SHA-256.
- `verification.json`: số lượng và tình trạng tải.

Việc kiểm tra file đã xác nhận nội dung nguồn của đủ 26 trang, 16 code block và các file tài nguyên bằng SHA-256; tất cả ảnh trong HTML được nhúng trực tiếp, không phụ thuộc đường dẫn file khác.
