import win32clipboard as wc
import win32con
import pywintypes
from msedge.selenium_tools import Edge, EdgeOptions
from pynput.keyboard import Key, Listener
import threading

print('You can press ESC to quit the process')

clipboard_lock = threading.Lock()
opts = EdgeOptions()
opts.use_chromium = True
opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
driver = Edge(options=opts)
driver.get("https://translate.google.com/")

try:
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[1]/div/div[3]/div/div').click()
except Exception as e:
    print(e)
    pass


def stripClipboard():
    # lock 住 Critical Sections 減少 OpenClipboard access deny 的情況
    with clipboard_lock:

        # 開剪貼簿 可能會有 access deny exception
        try:
            wc.OpenClipboard()
        except pywintypes.error as we:
            print("pywintypes.error")
            print(we)
            return

        try:
            global driver
            # 拿複製內容
            txt = wc.GetClipboardData(win32con.CF_UNICODETEXT)
            txt = str(txt).strip()
            # 按行分割
            txt = txt.splitlines()
            # 換成空格
            txt = ' '.join(txt)
            # 把空格都變一個
            txt = ' '.join(txt.split())
            # 把 ` escape 跳脫成 \`
            txt = txt.replace(r'`', r'\`')
            # 清空剪貼簿
            wc.EmptyClipboard()
            # 把轉換文的問自丟回剪貼簿
            wc.SetClipboardData(win32con.CF_UNICODETEXT, txt)
            # 餵 google 翻譯
            driver.find_element_by_tag_name('textarea').clear()
            driver.find_element_by_tag_name('textarea').send_keys(txt)
        except TypeError:
            print("Type Error: Maybe your clip is not text")
        finally:
            # 關剪貼簿
            wc.CloseClipboard()


def on_press(key):
    # print('{0} pressed'.format(key))
    return


def on_release(key):
    # print('{0} release'.format(key))

    # 按 ctrl c
    if str(key) == r"'\x03'":
        print('copy to clipboard')
        stripClipboard()

    # Stop listener
    if key == Key.esc:
        global driver
        driver.close()
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
