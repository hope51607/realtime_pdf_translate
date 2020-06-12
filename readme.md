# Realtime Paper Translate
### 即時論文翻譯


## Dependency
- Windows
- python3
- win32clipboard
- selenium
- pynput

## How To Use
1. 
    install dependencies
    ```sh
    pip install win32clipboard selenium pynput
    ```

2. 
    run script
    ```sh
    python realtime_paper_translate.py
    ```

3. 
    copy paper and enjoy

## Demo
![Demo](demo.gif)

## 說穿了就是自動幫你做下列步驟
1. 用 selenium 打開 google 翻譯
2. 按下 ctrl+c 時自動把 windows 剪貼簿裡的換行刪掉
3. 把結果丟到 google 翻譯


> 期末報告要報 paper，對英文苦手來說真的是生不如死，
> 論文 pdf 複製的文字下來會一堆段行，
> 丟翻譯就會翻得很怪，
> 手動去掉斷行實在太麻煩了，
> 就寫了這個來逃避現實中 QQ
