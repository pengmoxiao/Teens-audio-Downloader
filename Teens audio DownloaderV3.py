import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image, ImageTk
def on_button_click():
    grade=gradevar.get()
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/112.0.0.0 Safari/537.36'}
    res=requests.get(url=f"https://m.i21st.cn/paper/index_21je{grade}_1.html",headers=header)
    if res.status_code==200:
        soup = BeautifulSoup(res.content, 'html.parser')
        href="https://m.i21st.cn"+str(soup.find_all("a")[26].get("href"))
    else :
        label.config(text="连接服务器错误，状态码："+str(res.status_code))
        root.update_idletasks()
        return 
    result = messagebox.askokcancel("确认下载", "即将下载："+soup.find_all("a")[26].get_text())
    
        
    if result:

        download(href,header,soup,res,soup.find_all("a")[26].get_text())
def on_input_button_click():
    grade=gradevar.get()
    input_text = input_entry.get()
    
    try:
        input_text=int (input_text)
    except:
        label.config(text="期数要为整数！！！")
        return
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/112.0.0.0 Safari/537.36'}
    res=requests.get(url=f"https://m.i21st.cn/paper/index_21je{grade}_1.html",headers=header)
    tmp=["","一","二","三"]
    if res.status_code==200:
        soup = BeautifulSoup(res.content, 'html.parser')
        try:
            href="https://m.i21st.cn"+soup.find('a', class_='wrapno txt-18', string=lambda text: text and f"初{tmp[int(grade)]} "+"第"+str(input_text)+"期"==text).get("href")
        except:
            label.config(text="未找到指定期数的报纸！！")
            root.update_idletasks()
            return
    else :
        label.config(text="连接服务器错误，状态码："+str(res.status_code))
        root.update_idletasks()
        return 
    result = messagebox.askokcancel("确认下载", "即将下载："+soup.find('a', class_='wrapno txt-18', string=lambda text: text and f"初{tmp[int(grade)]} "+"第"+str(input_text)+"期"==text).get_text())
    
    if result:

        download(href,header,soup,res,soup.find('a', class_='wrapno txt-18', string=lambda text: text and f"初{tmp[int(grade)]} "+"第"+str(input_text)+"期"==text).get_text())
    



def download(href,header,soup,res,fpath):
    try:
        os.mkdir(fpath)
    except:
        pass
    if (1231==1231):
        audiohtmlres=requests.get(url=href,headers=header)
        if audiohtmlres.status_code==200:
            audiohtmlsoup=BeautifulSoup(audiohtmlres.content,"html.parser")
            audio_name=[]
            audio_urls=[]
            for audiohtmlurl in audiohtmlsoup.find_all("a",class_="wrapno txt-16"):
                print ("html url:",audiohtmlurl.get("href"),"audio name:",audiohtmlurl.get_text())
                audio_urls.append(audiohtmlurl.get("href"))
                audio_name.append(audiohtmlurl.get_text())
            #print (audio_urls,audio_name)
            for i in range(len(audio_urls)):
                audiores=requests.get(url=audio_urls[i],headers=header)
                if audiores.status_code==200:
                    audiosoup=BeautifulSoup(audiores.content,"html.parser")
                    label.config(text="音频链接:"+audiosoup.find("audio").get("src")+"名称:"+audio_name[i])
                    root.update_idletasks()
                    os.system(f'''curl ^"{audiosoup.find("audio").get("src")}^" -H ^"Accept: */*^" -H ^"Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6^" -H ^"Cache-Control: no-cache^" -H ^"Connection: keep-alive^" -H ^"Pragma: no-cache^" -H ^"Range: bytes=0-^" -H ^"Referer: https://paper.i21st.cn/^" -H ^"Sec-Fetch-Dest: audio^" -H ^"Sec-Fetch-Mode: no-cors^" -H ^"Sec-Fetch-Site: cross-site^" -H ^"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0^" -H ^"sec-ch-ua: ^\\^"Chromium^\\^";v=^\\^"130^\\^", ^\\^"Microsoft Edge^\\^";v=^\\^"130^\\^", ^\\^"Not?A_Brand^\\^";v=^\\^"99^\\^"^" -H ^"sec-ch-ua-mobile: ?0^" -H ^"sec-ch-ua-platform: ^\\^"Windows^\\^"^" --output ".\\{fpath}\\{audio_name[i]}.mp3"''')
                else:
                    label.config(text="获取"+audio_name[i]+"音频发生错误")
                    root.update_idletasks()
            label.config(text="下载完成！")
            root.update_idletasks()
        else :
            label.config(text="获取"+soup.find_all("a")[26].get_text()+"的具体内容时发生错误")
            root.update_idletasks()
    else :
        label.config(text="连接至服务器失败，状态码"+str(res.status_code))


root = tk.Tk()
root.title("报纸音频下载器")
import sys
bundle_dir = getattr(sys, '_MEIPASS')
 

data_file_path = os.path.join(bundle_dir)
path=os.path.join(bundle_dir,'icon.ico')
root.iconbitmap(path)
root.geometry("900x300")
gradevar = tk.StringVar()

radio1 = tk.Radiobutton(root, text="初一", variable=gradevar, value="1")
radio2 = tk.Radiobutton(root, text="初二", variable=gradevar, value="2")
radio3 = tk.Radiobutton(root, text="初三", variable=gradevar, value="3")


radio1.pack()
radio2.pack()
radio3.pack()

label = tk.Label(root, text="")
label.pack(pady=10)


button = tk.Button(root, text="点击下载最新Teens", command=on_button_click)
button.pack(pady=10)
input_entry = tk.Entry(root, width=4)
input_entry.pack(pady=10)


input_button = tk.Button(root, text="下载特定期数Teens", command=on_input_button_click)
input_button.pack(pady=10)

root.mainloop()
