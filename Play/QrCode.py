#! usr/bin/Python
# coding = utf -8
# 爬虫
#生成一个二维码
import qrcode

data = '我是momo'

img_file = r'E:\Lianxi'

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image()
img.save(img_file)
img.show(img_file)