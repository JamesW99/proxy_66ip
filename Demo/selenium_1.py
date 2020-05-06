import tesserocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('w3c', False)



browser = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(browser, 20)

url= "https://passport.bilibili.com/login"
browser.get(url)

#输入账号密码
username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#login-username')))
username.send_keys("15010778788")

pw = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#login-passwd')))
sleep(2)
pw.send_keys('JWys150319')

login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,' div.btn-box > a.btn.btn-login')))
sleep(1)

#登陆完成
login.click()



#验证码部分
#拿slice
slice_image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_bg')))
slice_image.screenshot(r'/Users/james/Downloads/captcha1.png')


#拿full_bg
js = 'var change = document.getElementsByClassName("geetest_canvas_fullbg");change[0].style = "display:block"'
browser.execute_script(js)
sleep(2)
fullimg = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_canvas_fullbg')))
fullimg.screenshot(r'/Users/james/Downloads/captcha2.png')         #拿到两张图


def is_pixel_equal(self, image1,image2,x,y ):
    '''
    判断两个像素是否相同
    :param image1:图片1
    :param image2:图片2
    :param x : 位 置 x
    :param y : 位 置 y
    :return:像素是否相同
    '''
    #取两个图片的像素点
    pixel1 = image1.load()[x,y]
    pixel2 = image2.load()[x,y]
    threshold=60
    if abs(pixel1[0]- pixel2[0]) < threshold and abs(pixel1[1]- pixel2[1]) < threshold and abs(
        pixel1[2] - pixel2[2])<threshold:
        return True
    else:
        return False

def get_gap(self, image1, image2):
    '''
    获取缺口偏移量
    :param image1:不带缺口图片
    :param image2:带缺口图片
    :return:
    '''
    left =60
    for i in range(left, image1.size[0]):
        for j in range(image1.size[1]):
            if not self.is_pixel_equal(image1,image2,i , j ):
                left = i
                return left
    return left