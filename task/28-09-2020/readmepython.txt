Cài đặt unrar : sudo apt-get install rar unrar
Unrar : unrar x Name.rar

Cài đặt python 3.6:

B1: sudo apt-get update
B2: sudo add-apt-repository ppa:deadsnakes/ppa
B3: sudo apt-get update
B4: sudo apt-get install python3.6

Cấu hình mặc định python3.6 cho hệ thống:
B1: which python3 --> xem thư mục python3 , mặc định là /usr/bin/python3
which python --> xem thư mục cài đặt python , mặc định là /usr/bin/python

B2: sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
--> mặc định python3 là python3.6
B3: sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
B4 : sudo update-alternatives --config python3
sudo update-alternatives --config python
(There is only one alternative in link group python (providing /usr/bin/python): /usr/bin/python3.6
Nothing to configure) bỏ qua
B5: Kiểm tra : python --version
python3 --verion

Fix pip erro
sudo apt-get install python3-pip
python -m pip install --upgrade pip
pip install --upgrade pip