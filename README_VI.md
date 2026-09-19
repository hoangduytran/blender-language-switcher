# Nút đổi ngôn ngữ cho Blender

[English](README.md) | **Tiếng Việt**

Đây là một tiện ích nhỏ cài thêm vào Blender (Blender gọi loại này là
"add-on"). Nó đặt **một nút đổi ngôn ngữ ngay trên thanh trên cùng** của cửa sổ
Blender. Chỉ cần một cú bấm là bạn chuyển cả giao diện qua lại giữa tiếng Anh và
một ngôn ngữ khác, chẳng hạn tiếng Việt, mà không phải mỗi lần lại mở
*Preferences → Interface → Translation* để chỉnh.

Tiện ích này có ích cho:

- người dịch Blender, muốn xem bản dịch của mình hiện ra trên giao diện trông
  thế nào;
- người đang học Blender bằng tiếng Việt nhưng xem video hướng dẫn bằng tiếng
  Anh, cần so tên các menu cho khớp;
- bất kỳ ai muốn biết tên gốc tiếng Anh của một nút bấm hay một công cụ.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ File Edit Render Window Help │ Layout Modeling … │ [Tiếng Việt   ▾][✓] Scene │
└──────────────────────────────────────────────────────────────────────────────┘
                                                      └─ nút đổi ngôn ngữ ─┘
```

## Tiện ích làm được gì

- Một danh sách để chọn ngôn ngữ và một ô đánh dấu để bật/tắt, nằm trên thanh
  trên cùng, ngay bên trái ô **Scene**.
- **Đánh dấu vào ô:** Blender chuyển sang ngôn ngữ bạn chọn và dịch luôn mọi
  thứ: chữ trên giao diện, dòng chú thích hiện ra khi rê chuột lên nút, các
  thông báo, và tên đặt sẵn cho những vật mới tạo.
- **Bỏ dấu ở ô:** Blender tắt hết phần dịch và quay về ngôn ngữ mặc định, tức
  là giao diện trở lại tiếng Anh.
- Danh sách ngôn ngữ lấy từ chính bản Blender bạn đang dùng. Tiếng Anh luôn
  đứng đầu danh sách.
- Blender nhớ ngôn ngữ bạn đã chọn, nên lần sau bật lại vẫn là ngôn ngữ đó.

## Cần có gì

- Blender **bản 4.2 trở lên**. Tiện ích đã được thử với Blender 4.5.
- Bản Blender có hỗ trợ nhiều ngôn ngữ. Các bản tải từ trang chính thức
  [blender.org](https://www.blender.org) đều có sẵn. Nếu bản của bạn không có,
  nút đổi ngôn ngữ sẽ không hiện ra.

## Cách cài đặt

Tên các menu dưới đây ghi bằng tiếng Anh, vì đó là giao diện mặc định của
Blender.

1. Tải tệp `switch_language-1.0.1.zip` trong thư mục [`dist/`](dist/) về máy:
   bấm vào tên tệp, rồi bấm nút **Download raw file** (nút hình mũi tên chỉ
   xuống, ở phía bên phải).
2. Mở Blender, vào menu **Edit → Preferences**, rồi chọn **Get Extensions** ở
   cột bên trái.
3. Bấm vào nút mũi tên nhỏ **⌄** ở góc trên bên phải, rồi chọn
   **Install from Disk…**
4. Chọn tệp zip vừa tải về. Blender sẽ tự cài và tự bật tiện ích.

Còn một cách nhanh hơn: kéo tệp zip rồi thả thẳng vào cửa sổ Blender.

## Cách dùng

1. Nhìn về phía bên phải của thanh trên cùng, ngay trước ô **Scene**.
2. Chọn ngôn ngữ trong danh sách, ví dụ tiếng Việt.
3. Đánh dấu vào ô bên cạnh. Giao diện chuyển sang ngôn ngữ đó.
4. Bỏ dấu ở ô. Giao diện quay về tiếng Anh.

## Tự sửa tiện ích và tự làm tệp cài đặt

Phần này dành cho ai muốn sửa tiện ích theo ý mình. Nếu bạn chỉ cần dùng, có
thể bỏ qua phần này.

Tệp `mk_install_zip.py` là một chương trình nhỏ. Nó gom các tệp trong thư mục
`switch_language/` lại thành một tệp zip để cài vào Blender. Bạn dùng nó sau
khi đã sửa tiện ích, chẳng hạn để sửa một lỗi hay để đổi ngôn ngữ được chọn sẵn.

Bạn cần:

- máy có cài **Python bản 3.8 trở lên**. Python là phần mềm miễn phí, tải ở
  [python.org](https://www.python.org). Máy Mac và Linux thường đã có sẵn.
- một bản sao của toàn bộ thư mục dự án này trên máy.

### Bước 1. Tải thư mục dự án về máy

Nếu máy bạn có cài Git:

```sh
git clone https://github.com/hoangduytran/blender-language-switcher.git
cd blender-language-switcher
```

Nếu không có Git: trên trang GitHub của dự án, bấm nút xanh **Code**, chọn
**Download ZIP**, rồi giải nén tệp vừa tải về.

Sau đó mở cửa sổ gõ lệnh ngay trong thư mục đó:

- **Mac:** bấm chuột phải vào thư mục trong Finder, chọn
  **New Terminal at Folder** (Mở Terminal tại thư mục này).
- **Windows:** mở thư mục trong File Explorer, bấm vào thanh địa chỉ ở phía
  trên, gõ `cmd` rồi nhấn Enter.
- **Linux:** bấm chuột phải vào khoảng trống trong thư mục, chọn
  **Open in Terminal**.

### Bước 2. Sửa theo ý bạn

Các tệp cần sửa nằm trong thư mục `switch_language/`:

- `__init__.py`: vẽ nút đổi ngôn ngữ lên thanh trên cùng và lưu lựa chọn của
  bạn.
- `language_state.py`: quyết định dùng ngôn ngữ nào, và bật hoặc tắt các phần
  dịch.
- `blender_manifest.toml`: ghi tên, số phiên bản, và bản Blender thấp nhất
  dùng được tiện ích.

Nếu định chia sẻ bản của mình cho người khác, hãy tăng số phiên bản (dòng
`version`) trong `blender_manifest.toml`, ví dụ từ `1.0.1` lên `1.0.2`. Tên tệp
zip sẽ lấy theo số này, và nhờ số lớn hơn mà Blender biết đây là bản mới.

### Bước 3. Làm tệp zip

Gõ lệnh sau vào cửa sổ gõ lệnh, rồi nhấn Enter.

Trên Mac và Linux:

```sh
python3 mk_install_zip.py
```

Trên Windows:

```bat
py mk_install_zip.py
```

Tệp zip được lưu trong thư mục `dist/`, với tên
`switch_language-<số phiên bản>.zip`. Dòng chữ cuối cùng hiện ra cho biết tên
chính xác, ví dụ:

```
Created dist/switch_language-1.0.2.zip (3 files: blender_manifest.toml, __init__.py, language_state.py)
```

Chương trình tự tìm Blender trên máy bạn. Nếu tìm thấy, nó nhờ chính Blender
đóng gói tệp zip và kiểm tra xem tệp có dùng được không. Nó tìm theo thứ tự
sau:

1. chỗ bạn chỉ ra sau chữ `--blender` (xem bảng bên dưới);
2. thiết lập tên là `BLENDER` trên máy, nếu bạn đã tự đặt;
3. lệnh `blender`, nếu gõ `blender` trong cửa sổ gõ lệnh là mở được Blender;
4. trên Mac: các ứng dụng Blender trong thư mục **Applications**.

Nếu không tìm thấy Blender, chương trình vẫn làm được tệp zip bằng Python. Tệp
đó có nội dung giống hệt, chỉ là chưa được Blender kiểm tra lại.

Các cách chạy:

| Lệnh | Tác dụng |
|------|----------|
| `python3 mk_install_zip.py` | Dùng Blender nếu tìm thấy, không thấy thì dùng Python |
| `python3 mk_install_zip.py --blender ĐƯỜNG_DẪN` | Dùng Blender ở chỗ bạn chỉ ra, ví dụ `"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"` hoặc `/Applications/Blender.app/Contents/MacOS/Blender` |
| `python3 mk_install_zip.py --no-blender` | Không dùng Blender, chỉ dùng Python |
| `python3 mk_install_zip.py --help` | Hiện danh sách các cách chạy này |

Trên Windows, thay `python3` bằng `py`.

### Bước 4. Cài tệp zip của bạn

Cài tệp mới trong thư mục `dist/` giống như ở phần
[Cách cài đặt](#cách-cài-đặt). Nếu máy đã có bản cũ, Blender sẽ thay bằng bản
mới. Nếu thanh trên cùng chưa thay đổi, hãy tắt Blender rồi mở lại.

## Bên trong tiện ích làm gì

Phần này dành cho người biết lập trình.

Tiện ích gắn thêm một hàm vẽ vào thanh trên cùng (`TOPBAR_HT_upper_bar`) bằng
`prepend`, để phần của nó được vẽ trước phần có sẵn của Blender. Blender vẽ
thanh trên cùng làm hai nửa, trái và phải. Hàm này chỉ vẽ ở nửa bên phải
(`context.region.alignment == 'RIGHT'`), và vì được vẽ trước nên nút đổi ngôn
ngữ nằm ngay bên trái ô Scene / View Layer.

Danh sách ngôn ngữ và ô đánh dấu được lưu trong phần thiết lập của tiện ích.
Mỗi khi một trong hai thay đổi, hàm `language_state.apply_language_state()` sẽ
đặt lại `Preferences.view.language` và các tùy chọn `use_translate_*`.

## Các tệp trong dự án

| Tệp | Dùng để làm gì |
|-----|----------------|
| `switch_language/__init__.py` | Đăng ký tiện ích với Blender, lưu thiết lập, vẽ nút trên thanh trên cùng |
| `switch_language/language_state.py` | Chọn ngôn ngữ và bật/tắt các phần dịch |
| `switch_language/blender_manifest.toml` | Thông tin về tiện ích: tên, phiên bản, giấy phép |
| `dist/switch_language-1.0.1.zip` | Tệp zip để cài ngay vào Blender |
| `mk_install_zip.py` | Làm lại tệp zip trong `dist/` từ các tệp đã sửa |
| `README.md` | Hướng dẫn bằng tiếng Anh |

## Giấy phép

GPL-2.0 trở lên. Nói đơn giản: bạn được dùng, sửa và chia sẻ lại tiện ích này
miễn phí, với điều kiện bản bạn chia sẻ cũng phải giữ cùng giấy phép này. Toàn
văn giấy phép (bằng tiếng Anh) nằm trong tệp [LICENSE](LICENSE).
