# TryHackMe-Voyage

Recon

<img width="848" height="185" alt="image" src="https://github.com/user-attachments/assets/22b39482-5c83-4d8b-a59b-565ee24f4989" />

<img width="783" height="654" alt="image" src="https://github.com/user-attachments/assets/d40a29cc-83d2-47c6-9567-61af82729942" />

truy cập http://10.201.13.69/administrator/ được liệt kê từ gobuster

<img width="1230" height="714" alt="image" src="https://github.com/user-attachments/assets/7d2f8418-82e3-4c13-8b67-1d1d8fd5dbb9" />

Giống như wpscan, joomscan là một công cụ quét lỗ hổng bảo mật của Joomla CMS

<img width="569" height="735" alt="image" src="https://github.com/user-attachments/assets/71fb0230-fbd2-4af9-9d33-ab0bfb014b8d" />

Joomla 4.0.0 đến 4.2.7 dễ bị tấn công, improper access checkcho phép người dùng chưa xác thực truy cập vào một số endpoints dịch vụ web nhạy cảm bằng cách thêm ?public=truevào chuỗi truy vấn yêu cầu. Chi tiết : https://sysevil.github.io/posts/analysis-joomla-cve-2023-23752/

đối với trường hợp này tôi chỉ dùng 2 endpoints :

/api/index.php/v1/users?public=true: endpoint này liệt kê tất cả người dùng trên phiên bản Joomla

/api/index.php/v1/config/application?public=true: endpoint này tiết lộ các chi tiết cấu hình nhạy cảm, bao gồm thông tin xác thực cơ sở dữ liệu

có thể truy cập trực tiếp url hoặc dùng curl

<img width="1280" height="755" alt="image" src="https://github.com/user-attachments/assets/b1b26604-5178-4ff1-b0a6-c952fca17c6a" />

thông tin đăng nhập ở trên tuy nhiên nó không dùng để đăng nhập vào trang quản trị nên tôi thử đăng nhập vào ssh thì được 

<img width="791" height="586" alt="image" src="https://github.com/user-attachments/assets/7f9d777f-9382-4c51-9b31-bb677467a119" />

và tôi đang ở container docker , có thể sử dụng nmap bên trong này 

<img width="604" height="338" alt="image" src="https://github.com/user-attachments/assets/7ccd1868-bc1a-4cb5-96ef-009a7c50637f" />

<img width="897" height="678" alt="image" src="https://github.com/user-attachments/assets/db720161-1167-43b3-9b0b-a2f21f4a8a05" />

sau khi quét nmap thì xuất hiện port 5000 trên ip 192.168.100.12 hoàn toàn xa lạ không được phát hiện trong quá trình recon ban đầu, dịch vụ đang chạy Werkzeug/3.1.3, đây là thư viện máy chủ web được Flask sử dụng làm máy chủ mặc định

sau đó tôi sử dụng socat

<img width="922" height="267" alt="image" src="https://github.com/user-attachments/assets/e928c037-ccdd-42e5-addc-95499c135d07" />

socat tcp-listen:5000,fork,reuseaddr tcp:192.168.100.12:5000 &
→ Khởi chạy socat ở background, lắng nghe local:5000 và forward mọi kết nối tới 192.168.100.12:5000. fork cho phép nhiều kết nối.

ss -lntp | grep 5000
→ Kiểm tra xem có process nào lắng nghe trên cổng 5000 không; kết quả cho thấy socat đang lắng nghe (với PID).

curl -I localhost:5000
→ Gửi HEAD request tới local:5000; vì có socat forward, bạn nhận được header từ HTTP server chạy tại 192.168.100.12:5000 (vd. Werkzeug/Flask).

<img width="1275" height="756" alt="image" src="https://github.com/user-attachments/assets/5709680c-8766-418f-a25c-38967837d0f1" />

thật lạ sau khi tôi thấy 1 trang đăng nhập đơn giản chấp nhận bất kỳ tên người dùng và mật khẩu nào và chuyển hướng đến bảng thông tin hiển thị lại cho người dùng , tới bước này tôi đã nhận được sự hỗ trợ của bạn bè đặc biệt là chatgpt 😄

<img width="1078" height="590" alt="image" src="https://github.com/user-attachments/assets/16281fbf-c07e-44b6-8dfa-5bb8b7ad3ab7" />

có vẻ như đây không phải cookie dạng JWT hay PHP-serialized — đây là một object được pickle bởi Python (protocol 4) 

Dữ liệu chứa các khóa "user" và "revenue" với giá trị "admin" và "85000"

tôi đã thử tệp shell pickle.py

<img width="762" height="228" alt="image" src="https://github.com/user-attachments/assets/c8256bda-9402-4d07-87ed-3835196947c5" />

ở 1 terminal khác tôi chạy netcat lắng nghe trên cổng là 445 

<img width="676" height="314" alt="image" src="https://github.com/user-attachments/assets/da6aebad-04cd-4809-9d8f-9a4d0938c093" />

<img width="409" height="225" alt="image" src="https://github.com/user-attachments/assets/0b21274e-6f7e-42ff-8207-c6c35086b02b" />

như vậy là tôi đã có được lá cờ đầu tiên 

nhưng bây giờ tôi đang ở container khác 

linpeas.sh và deepce.sh là cdk-team/cdk một số công cụ được sử dụng nhiều nhất để liệt kê và thoát khỏi container.

đây là bài viết mô tả cuộc tấn công này https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/linux-capabilities.html#cap_sys_module:~:text=abusing%20this%20privilege.-,Example%20with%20environment%20(Docker%20breakout),-You%20can%20check


tạo một tệp reverse-shell.c


tạo một Makefile


chạy make
<img width="788" height="298" alt="image" src="https://github.com/user-attachments/assets/21806951-46b8-4d3e-a14c-2e91ae0323a8" />

mở 1 terminal mới chạy nc lắng nghe trên port 1234

<img width="995" height="746" alt="image" src="https://github.com/user-attachments/assets/0c9c0510-460c-4c73-95d3-f114b897724f" />

Lá cờ cuối cùng 
