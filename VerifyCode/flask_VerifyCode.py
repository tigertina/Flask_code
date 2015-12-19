# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
"""
__author__="tina"
__mtime__ = '2015/12/19  15:32'
"""
import random
import Image, ImageDraw, ImageFont
import StringIO

from flask import Flask

class RandomChar():
  """用于随机生成汉字对应的Unicode字符"""
  @staticmethod
  def Unicode():
    val = random.randint(0x4E00, 0x9FBB)
    return unichr(val)

  @staticmethod
  def GB2312():
    head = random.randint(0xB0, 0xCF)
    body = random.randint(0xA, 0xF)
    tail = random.randint(0, 0xF)
    val = ( head << 8 ) | (body << 4) | tail
    str = "%x" % val
    #
    return str.decode('hex').decode('gb2312','ignore')

class ImageChar():
  def __init__(self, fontColor = (0, 0, 0),
                     size = (100, 40),
                     fontPath = 'STZHONGS.TTF',
                     bgColor = (255, 255, 255, 255),
                     fontSize = 20):
    self.size = size
    self.fontPath = fontPath
    self.bgColor = bgColor
    self.fontSize = fontSize
    self.fontColor = fontColor
    self.font = ImageFont.truetype(self.fontPath, self.fontSize)
    self.image = Image.new('RGBA', size, bgColor)

  def rotate(self):
	img1 = self.image.rotate(random.randint(-5, 5), expand=0)#默认为0，表示剪裁掉伸到画板外面的部分
    img = Image.new('RGBA',img1.size,(255,)*4)
    self.image = Image.composite(img1,img,img1)

  def drawText(self, pos, txt, fill):
    draw = ImageDraw.Draw(self.image)
    draw.text(pos, txt, font=self.font, fill=fill)
    del draw

  def randRGB(self):
    return (random.randint(0, 255),
           random.randint(0, 255),
           random.randint(0, 255))

  def randPoint(self):
    (width, height) = self.size
    return (random.randint(0, width), random.randint(0, height))

  def randLine(self, num):
    draw = ImageDraw.Draw(self.image)
    for i in range(0, num):
      draw.line([self.randPoint(), self.randPoint()], self.randRGB())
    del draw

  def randChinese(self, num):
    gap = 0
    start = 0
    strRes = ''
    for i in range(0, num):
      char = RandomChar().GB2312()
      strRes += char
      x = start + self.fontSize * i + random.randint(0, gap) + gap * i
      self.drawText((x, random.randint(-5, 5)), char, (0,0,0))
      self.rotate()
    print strRes
    self.randLine(8)
    return strRes,self.image

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello World!'

@app.route('/VerifyCode/')
def get_code():
    #把strs发给前端,或者在后台使用session保存
    ic = ImageChar(fontColor=(100,211, 90))
    strs,code_img = ic.randChinese(4)
    buf = StringIO.StringIO()
    code_img.save(buf,'JPEG',quality=70)
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

if __name__ == "__main__":
    app.run(host="localhost",port=5000,debug=True)