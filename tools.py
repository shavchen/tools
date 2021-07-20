
from tkinter import *
import requests;requests.packages.urllib3.disable_warnings()
import re
from tkinter import ttk,scrolledtext
import traceback

class MY_GUI():
    def __init__(self,root):
        self.root = root
        self.root.title("Repeater")
        # mac不支持设置图标
        self.root.iconbitmap(default = r'burp.ico')
        self.root.minsize(1000,802)
        self.root.maxsize(1000,802)
        self.root.option_add("*Font", "kaiti")
        self.root["bg"] = self._from_rgb((240, 240, 245))
        self.https = IntVar()
        self.redirection = IntVar()
        style = ttk.Style()
        style.theme_use('xpnative')
        style.configure("Vertical.TScrollbar", gripcount=0,troughcolor="blue", bordercolor="blue", arrowcolor="green")
        style.configure("TButton",foreground="black",background='WhiteSmoke',font = ('kaiti','10'), relief = "RAISED", borderwidth = 3)

    def set_init_window(self):
        #标签
        self.init_send_button = ttk.Button(self.root, text = "Send", style = "TButton", command = self.send)
        self.init_send_button.grid(row = 1, column = 0)
        self.https_box = Checkbutton(self.root, text="Use HTTPS",foreground = "black",background='WhiteSmoke', font = ('kaiti','10'), variable= self.https)
        self.https_box.grid(row = 1, column = 6)
        self.https_box = Checkbutton(self.root, text="Follow redirection",foreground = "black",background='WhiteSmoke', font = ('kaiti','10'), variable= self.redirection)
        self.https_box.grid(row = 1, column = 8)
        self.init_data_label = Label(self.root, text="Requests",  foreground = "red", )
        self.init_data_label.grid(row = 2, column = 0)
        self.result_data_label = Label(self.root, text="Response", foreground = "red", )
        self.result_data_label.grid(row = 2, column=12)


        #文本框
        self.init_data_Text = Text(self.root, width = 60, height = 45, undo = True)
        self.init_data_Text.grid(row = 3, column = 0, rowspan = 10, columnspan = 10,  sticky=S + W + E + N)

        self.scroll_bar_init = ttk.Scrollbar(style = "Vertical.TScrollbar",orient="vertical",command = self.init_data_Text.yview)
        self.init_data_Text.config(yscrollcommand = self.scroll_bar_init.set)
        self.scroll_bar_init.grid(row = 3, column = 11, rowspan = 10, sticky=S + W + E + N)

        self.result_data_Text = Text(self.root, width = 60, height = 45, undo = False) 
        self.result_data_Text.grid(row = 3, column = 12, columnspan= 24)

        self.scroll_bar_result = ttk.Scrollbar(style = "Vertical.TScrollbar", orient="vertical",command = self.result_data_Text.yview)
        self.result_data_Text.config(yscrollcommand = self.scroll_bar_result.set)
        self.scroll_bar_result.grid(row = 3, column = 36, rowspan = 10, sticky=S + W + E + N)


    def _from_rgb(self,rgb):
        return "#%02x%02x%02x" % rgb

    def send(self):
        src = self.init_data_Text.get(1.0,END).encode()
        if src:
            res = Hackrequest(src,self.https.get(),self.redirection.get())
            self.result_data_Text.delete(1.0,END)
            self.result_data_Text.insert(1.0,res)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

def Hackrequest(raw,https,redirection):
    try:
        protocol = "https" if https == 1 else "http"
        redirection = True if redirection == 1 else False
        raw = str(raw, encoding="utf-8")
        method = re.search("(.*?) ",raw.split("\n")[0])[1]
        host = re.search("Host:(.*)",raw)[1].strip()
        path = re.search("(POST|GET)(.*) HTTP",raw)[2].strip()
        data = ''.join(raw.split("\n\n")[1:] if '\n\n' in raw else '')
        while True:
            if data.startswith("\n"):
                data = data.split("\n")[1]
            break
        target = protocol + "://" + host + path
        head = raw.split("\n\n")[0].split("\n")[2:] if '\n\n' in raw else raw.split("\n")[2:]
        header = {}
        for i in head:
            k = i.split(": ")[0]
            v = i.split(": ")[1]
            header[k] = v
        if method == "POST":
            res = requests.post(target, verify = False, timeout = 5, data = data, headers = header, allow_redirects = redirection)
        elif method == "GET":
            res = requests.get(target, verify = False, timeout = 5, headers = header, allow_redirects = redirection, stream=True)
        if res:
            http_vsn_str = res.raw._pool.ConnectionCls._http_vsn_str
            header_str = ""
            for k in res.headers.keys() :
                header_str = header_str + k + ":" + res.headers[k] + "\n"
            return http_vsn_str + "\n" + header_str + "\n\n" + res.text
    except Exception as e:
        return traceback.print_exc()

gui_start()