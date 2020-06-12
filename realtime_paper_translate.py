import win32clipboard as wc
import win32con
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from pynput.keyboard import Key, Listener

driver = webdriver.Edge()
driver.get("https://translate.google.com/")

try:
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[3]/div/div').click()
    driver.find_element_by_xpath('//*[@id="gb"]/div[2]/div[4]/div/div/div/div[2]/div/a[1]').click()
except ElementNotInteractableException as e:
    pass

def stripClipboard():
    global driver
    # 開剪貼簿，拿複製內容
    wc.OpenClipboard()
    txt = wc.GetClipboardData(win32con.CF_UNICODETEXT)
    txt = str(txt).strip()
    # 按行分割
    txt = txt.splitlines()
    # 換成空格
    txt = ' '.join(txt)
    # 把空格都變一個
    txt = ' '.join(txt.split())
    # 清空剪貼簿
    wc.EmptyClipboard()
    # 把轉換文的問自丟回剪貼簿
    wc.SetClipboardData(win32con.CF_UNICODETEXT, txt)
    wc.CloseClipboard()
    # 餵 google 翻譯
    driver.execute_script("document.getElementById('source').value = String.raw`{}`;".format(txt))

def on_press(key):
    # print('{0} pressed'.format(key))
    return

def on_release(key):
    # print('{0} release'.format(key))
    
    # 按 ctrl c
    if str(key) == r"'\x03'":
        print('ctrl+c')
        stripClipboard()        

    # Stop listener
    if key == Key.esc:
        global driver
        driver.close()
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()