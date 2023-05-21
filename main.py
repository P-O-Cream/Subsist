# Project Name:Subsist(Sandbox)
# Project Start Time:2022/8/12
# Project Writter:Qianmeng
# Copyright(C) 2023 浅梦 and all contributors
# All right Reserved
# Distributed under GPL license
# See copy at https://opensource.org/licenses/GPL-3.0

import time                
import atexit
import os
import sys
import termios
import random
import tty
import base64
import json
import re
import socket
import requests
import posix
import stat
import keyword

builtins = dir(__builtins__) # builtins类型字
keywords = keyword.kwlist # 关键字

NUMBER,BUILTIN,KEYWORD,STRING = "NUMBER","BUILTIN","KEYWORD","STRING" # 子类型定义
OTHER = "OTHER" # OTHER定义

# Copyright [C] 2023 LinLin 用于伪装成numpy库的类
class amap:
    def __init__(self,l):self.l=list(l)
    def __str__(self):return str(list(self.l))
    def __add__(self,other):
        if type(other)==amap:d=map(lambda x,y:x+y,self.l,other.l)
        else:d=map(lambda x:x+other,self.l)
        return amap(d)
    def __sub__(self,other):
        if type(other)==amap:d=map(lambda x,y:x-y,self.l,other.l)
        else:d=map(lambda x:other,self.l)
        return amap(d)
    def __mul__(self,other):
        if type(other)==amap:d=map(lambda x,y:x*y,self.l,other.l)
        else:d=map(lambda x:x*other,self.l)
        return amap(d)
    def __truediv__(self,other):
        if type(other)==amap:d=map(lambda x,y:x/y,self.l,other.l)
        else:d=map(lambda x:x/other,self.l)
        return amap(d)
    def __mod__(self,other):
        if type(other)==amap:d=map(lambda x,y:x%y,self.l,other.l)
        else:d=map(lambda x:x%other,self.l)
        return amap(d)
    def __pow__(self,other):
        if type(other)==amap:d=map(lambda x,y:x**y,self.l,other.l)
        else:d=map(lambda x:x**other,self.l)
        return amap(d)
    def __floordiv__(self,other):
        if type(other)==amap:d=map(lambda x,y:x//y,self.l,other.l)
        else:d=map(lambda x:x//other,self.l)
        return amap(d)
    def __setitem__(self,index,ro):self.l=list(self.l);eif.l[index]=ro
    def __getitem__(self,index):return list(self.l)[index]
    def __len__(self):return len(list(self.l))
    def __cmp__(self,other):return list(self.l)==list(other)
        
class printf:
    def __init__(self):
        self.lock = False # 格式锁
        self.fg_colour = None # 字体颜色
        self.bg_colour = None # 背景颜色
        self.time = 0 # 间隔时间
    def lock(self): self.lock = True # 格式上锁
    def unlock(self): self.lock = False # 格式解锁
    def setfg_colour(self,colour):
        if self.lock != True:self.fg_colour = colour # 修改字体颜色
    def setbg_colour(self,colour): 
        if self.lock != True:self.bg_colour = colour # 修改背景颜色
    def set_time(self,time): 
        if self.lock != True:self.time = time # 修改间隔时间
    def printf(self,text): # 按格式输出
        fg_colour = "" ;bg_colour = ""
        if self.bg_colour == "red":bg_colour = "\033[48;5;1m"                        # red
        if self.bg_colour == "yellow":bg_colour = "\033[48;5;3m"                     # yellow
        if self.bg_colour == "green":bg_colour = "\033[48;5;2m"                      # green
        if self.bg_colour == "blue":bg_colour = "\033[48;5;4m"                       # blue
        if self.bg_colour == "cyan":bg_colour = "\033[48;5;5m"                       # cyan
        if self.bg_colour == "purple":bg_colour = "\033[48;5;6m"                     # purple
        if self.bg_colour == "white":bg_colour = "\033[48;5;255m"                    # white
        if self.bg_colour == "gray":bg_colour = "\033[48;5;8m"                       # gray
        if self.bg_colour == "black":bg_colour = "\033[48;5;0m"                      # black
        if self.bg_colour == "darkgray":bg_colour = "\033[48;5;235m"                 # darkgray
        if self.bg_colour == "lightred":bg_colour = "\033[48;5;9m"                   # lightred
        if self.bg_colour == "lightyellow":bg_colour = "\033[48;5;11m"               # lightyellow
        if self.bg_colour == "lightgreen":bg_colour = "\033[48;5;10m"                # lightgreen
        if self.bg_colour == "lightblue":bg_colour = "\033[48;5;12m"                 # lightblue
        if self.bg_colour == "lightcyan":bg_colour = "\033[48;5;13m"                 # lightcyan
        if self.bg_colour == "lightpurple":bg_colour = "\033[48;5;14m"               # lightpurple
        if self.bg_colour == "lightwhite":bg_colour = "\033[48;5;15m"                # lightwhite
        if self.bg_colour == "darkblack":bg_colour = "\033[48;5;16m"                 # darkblack

        if self.fg_colour == "text_white":fg_colour = "\033[38;5;255m"               # text_white
        if self.fg_colour == "text_red":fg_colour = "\033[38;5;9m"                   # text_red
        if self.fg_colour == "text_orange":fg_colour = "\033[38;5;208m"              # text_orange
        if self.fg_colour == "text_yellow":fg_colour = "\033[33m"                    # text_yellow
        if self.fg_colour == "text_green":fg_colour = "\033[32m"                     # text_green
        if self.fg_colour == "text_blue":fg_colour = "\033[34m"                      # text_blue
        if self.fg_colour == "text_cyan":fg_colour = "\033[38;2;0;255;255m"          # text_cyan
        if self.fg_colour == "text_violet":fg_colour = "\033[38;2;255;0;255m"        # text_violet
        if self.fg_colour == "text_dark":fg_colour = "\033[38;5;232m"                # text_dark
        if self.fg_colour == "text_darkgray":fg_colour = "\033[38;5;234m"            # text_darkgray
        if self.fg_colour == "text_gray":fg_colour = "\033[38;5;242m"                # text_gray
        if self.fg_colour == "text_darkblue":fg_colour = "\033[38;5;27m"             # text_darkblue
        if self.fg_colour == "text_lightblue":fg_colour = "\033[38;5;39m"            # text_lightblue
        if self.fg_colour == "text_lightgreen":fg_colour = "\033[38;5;10m"           # text_lightgreen
        if self.fg_colour == "text_lightyellow":fg_colour = "\033[38;2;255;255;0m"   # text_lightyellow
        if self.fg_colour == "text_lightviolet":fg_colour = "\033[38;2;216;160;233m" # text_lightviolet
        if self.fg_colour == "italic":fg_colour = "\033[003m"                        # italic
        if self.fg_colour == "text_underline":fg_colour = "\033[004m"                # text_underline
        if self.fg_colour != None:print(fg_colour,end="")                            # text_none
        if self.bg_colour != None:print(bg_colour,end="")                            # bg_none
        for i in text:print(i,end="",flush=True);time.sleep(self.time) # 逐字输出文字    
        print("\033[m")
_printf = printf() 

class press: 
    def __init__(self,is_print_input): 
        if os.name != 'nt':
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd);self.old_term = termios.tcgetattr(self.fd)
            if is_print_input:self.new_term[3] = (self.new_term[3] & ~ ~termios.ECHO)
            else:self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
    def getch(self): # getch函数  
        if os.name == 'nt':return msvcrt.getch().decode('utf-8')
        else:return sys.stdin.read(1)
    def kbhit(self): # kbhit函数
        if os.name == 'nt':return msvcrt.kbhit()
        else:dr,dw,de = select.select([sys.stdin], [], [], 0);return dr != []
_press = press(True) 

class composite: 
    def __init__(self):
        self.choose,self.choose2 = 1,1 # 选择地点
        self.answer = "" # 问答字符串
    def unary_choose(self,button,text): # 主体函数
        print("\033c"+text)
        if self.choose > len(button):self.choose = 1 # 最高点
        if self.choose < 1:self.choose = len(button) # 最低点
        self.choose2 = 1
        for i in range(len(button)):
            if i == self.choose - 1:print(f"\033[32m>   {self.choose2}.{button[i]}\033[m ")
            else:print(f"    {self.choose2}.{button[i]} ")
            self.choose2 += 1 # choose2递推
        print(f"（w,s上下切换选项,y确定）")
        self.answer = _press.getch()
        if self.answer == "w":self.choose -= 1 # w操作
        if self.answer == "s":self.choose += 1 # s操作
        if self.answer == "y":return button[self.choose - 1] # 确定操作
_composite = composite()

def printcode(code):
    END_COLOR = "\033[0m"                               # 结束字\033[0m
    SELF_COLOR = "\033[95m"                             # self字\033[95m
    STRING_COLOR = "\033[32m"                           # 字符串\033[32m
    ESSENTIAL_COLOR = "\033[94m"                        # essential字\033[94m
    FUNCTION_COLOR = "\033[35m"                         # 工具\033[35m
    NUMBER_COLOR = "\033[36m"                           # 数字\033[36m
    BUILT_FUNCTION = "\033[90m"                         # butlt字\033[90m
    ERROR_COLOR = "\033[31m"                            # 报错\033[31m
    code = code.replace("\033", "\\033")                # 字符串分段
    number_list = []                                    # 字符串定位
    for i in range(10):number_list.append(str(i))       # 字符串列表化
    new_code = ""
    for i in range(len(code)):
        if code[i] in number_list:
            try:
                if not ((code[i+1] == "m" or code[i+2] == "m") or (code[i+1] == ";" or code[i+2] == ";")):new_code = new_code + NUMBER_COLOR + code[i] + END_COLOR
                else:new_code = new_code + code[i]
            except:new_code = new_code + NUMBER_COLOR + code[i] + END_COLOR
        else:new_code = new_code + code[i]
    code = new_code
    code = code.replace("self", SELF_COLOR + "self" + END_COLOR)                            # self
    code = code.replace("(", SELF_COLOR + "(" + END_COLOR)                                  # (
    code = code.replace(")", SELF_COLOR + ")" + END_COLOR)                                  # )
    code = code.replace("class", ESSENTIAL_COLOR + "class" + END_COLOR)                     # class
    code = code.replace("def", ESSENTIAL_COLOR + "def" + END_COLOR)                         # def
    code = code.replace("pass", ESSENTIAL_COLOR + "pass" + END_COLOR)                       # pass
    code = code.replace("try", ESSENTIAL_COLOR + "try" + END_COLOR)                         # try
    code = code.replace("except", ESSENTIAL_COLOR + "except" + END_COLOR)                   # except
    code = code.replace("for", ESSENTIAL_COLOR + "for" + END_COLOR)                         # for
    code = code.replace("break", ESSENTIAL_COLOR + "break" + END_COLOR)                     # break
    code = code.replace("in", ESSENTIAL_COLOR + "in" + END_COLOR)                           # in
    code = code.replace("not", ESSENTIAL_COLOR + "not" + END_COLOR)                         # not
    code = code.replace("if", ESSENTIAL_COLOR + "if" + END_COLOR)                           # if
    code = code.replace("from", ESSENTIAL_COLOR + "from" + END_COLOR)                       # from
    code = code.replace("import", ESSENTIAL_COLOR + "import" + END_COLOR)                   # import
    code = code.replace("else", ESSENTIAL_COLOR + "else" + END_COLOR)                       # else
    code = code.replace("True", ESSENTIAL_COLOR + "True" + END_COLOR)                       # True
    code = code.replace("False", ESSENTIAL_COLOR + "False" + END_COLOR)                     # False
    code = code.replace("print", FUNCTION_COLOR + "print" + END_COLOR)                      # print
    code = code.replace("input", FUNCTION_COLOR + "input" + END_COLOR)                      # input
    code = code.replace("range", FUNCTION_COLOR + "range" + END_COLOR)                      # range
    code = code.replace("object", FUNCTION_COLOR + "object" + END_COLOR)                    # object
    code = code.replace("int", FUNCTION_COLOR + "int" + END_COLOR)                          # int
    code = code.replace("str", FUNCTION_COLOR + "str" + END_COLOR)                          # str
    code = code.replace("dict", FUNCTION_COLOR + "dict" + END_COLOR)                        # dict
    code = code.replace("list", FUNCTION_COLOR + "list" + END_COLOR)                        # list
    code = code.replace("exec", FUNCTION_COLOR + "exec" + END_COLOR)                        # exec
    code = code.replace("eval", FUNCTION_COLOR + "eval" + END_COLOR)                        # eval
    code = code.replace("pr\033[94min\033[0mt", FUNCTION_COLOR + "print" + END_COLOR)       # print结构
    code = code.replace("\033[94min\033[0put", FUNCTION_COLOR + "input" + END_COLOR)        # input结构
    code = code.replace("__init__", BUILT_FUNCTION + "__init__" + END_COLOR)                # __init__结构
    code = code.replace("__\033[94min\033[0mit__", BUILT_FUNCTION + "__init__" + END_COLOR) # __init__ tool结构
    code = code.replace("__str__", BUILT_FUNCTION + "__str__" + END_COLOR)                  # __str__结构
    code = code.replace("__add__", BUILT_FUNCTION + "__add__" + END_COLOR)                  # __add__结构
    code = code.replace("__repr__", BUILT_FUNCTION + "__repr__" + END_COLOR)                # __repr__结构
    string_end = -5                                                                         # 递归
    while True:
        try:
            string_start = code.index('"', string_end + 5)                                  # 字符串结构
            string_end = code.index('"', string_start + 1) + 1                              # 字符串末尾
            new_sub_string = code[string_start:string_end]                                  # 字符串定义
            new_sub_string = new_sub_string.replace(STRING_COLOR, "")                       # string格式
            new_sub_string = new_sub_string.replace(SELF_COLOR, "")                         # self格式
            new_sub_string = new_sub_string.replace(ESSENTIAL_COLOR, "")                    # essential格式
            new_sub_string = new_sub_string.replace(FUNCTION_COLOR, "")                     # funiture格式
            new_sub_string = new_sub_string.replace(END_COLOR, "")                          # end格式
            new_sub_string = new_sub_string.replace(NUMBER_COLOR, "")                       # number格式
            new_sub_string = new_sub_string.replace(BUILT_FUNCTION, "")                     # built格式
            code = code[:string_start] + STRING_COLOR + new_sub_string + END_COLOR + code[string_end:]
        except:break
    string_end = -5                                                                         # 递归
    while True:
        try:
            string_start = code.index('"', string_end + 5)                                  # 字符串结构
            string_end = code.index('"', string_start + 1) + 1                              # 字符串末尾
            new_sub_string = code[string_start:string_end]                                  # 字符串定义
            new_sub_string = new_sub_string.replace(STRING_COLOR, "")                       # string格式
            new_sub_string = new_sub_string.replace(SELF_COLOR, "")                         # self格式
            new_sub_string = new_sub_string.replace(ESSENTIAL_COLOR, "")                    # essential格式
            new_sub_string = new_sub_string.replace(FUNCTION_COLOR, "")                     # funiture格式
            new_sub_string = new_sub_string.replace(END_COLOR, "")                          # end格式
            new_sub_string = new_sub_string.replace(NUMBER_COLOR, "")                       # number格式
            new_sub_string = new_sub_string.replace(BUILT_FUNCTION, "")                     # built格式
            code = code[:string_start] + STRING_COLOR + new_sub_string + END_COLOR + code[string_end:]
        except:break
    print(code)

# 一个废弃的system平替函数
# def system(command: str):
#     if posix.fork() == 0:
#         try:
#             with open("/bin/bash", "rb") as f:
#                 with open("/tmp/bash", "wb") as f2:f2.write(f.read())
#         except:pass
#         posix.chmod("/tmp/bash", stat.S_IRWXU)
#         posix.execv("/tmp/bash", ["/tmp/bash", "-c", command])
#     else:posix.wait()
    
def gotoxy(x,y,text):print(f"\033[{x};{y}f{text}",end="")

class Terminal:
    def __init__(self):
        self.choose = 1 # 选择地点
        self.answer = "" # 建立问答字符串
    def make_button(self,button,text,number): # 主题函数
        if self.choose  > len(button):self.choose = 1 # 最高点
        print("\033c"+text+"\n")
        for i in range(len(button)):
            if i % number == 0 and i != 0:print("\n")
            if i == self.choose - 1:print(f" \033[42m {button[i]} \033[m ",end="")
            else:print(f" \033[40m {button[i]} \033[m ",end="")
        print(f"\n\n（Tap切换到下一个选项,y确定）")
        self.answer = _press.getch() # 外置输入
        if self.answer == "\t":self.choose += 1 # tap处理
        if self.answer == "y":return button[self.choose - 1] # 确定操作
_terminal = Terminal()
            
_printf.unlock() # 格式解锁
_printf.setfg_colour(None) # 字体颜色去除
_printf.setbg_colour(None) # 背景颜色去除
_printf.set_time(0.03) # 间隔颜色0.03

# 模组部分
class Subsist_Mod_:
    def __init__(self):
        self.use_mod = False # 是否启用模组
        self.mod_name = "" # 模组名称
        self.mod_version = "" # 模组适用版本
        self.mod_introduce = """""" # 模组介绍
        self.mod_type = "" # 模组类型
    def before_game(self):...
    def cycle(self):...
    def after_game(self):...
    
# 准备工作完成，开始正式游戏
class Subsist:
    def __init__(self):
        # @note 定义了一些游戏全局属性
        self.map_list = [["0" for i in range(400)]for i in range(400)] # 世界地图（400x400为一个区块）
        self.seed = str(random.randint(1,111111111111111)) # 种子随机生成
        self.world_name = "New World" # 全局世界名称
        self.player_name = "Game Player" # 全局玩家名称
        self.no_collide = ["0","1","4","5","14","10","猪","牛"] # 不参与碰撞的方块列表
        self.coordinate_x = 1 # x坐标初始化
        self.coordinate_y = 200 # y坐标初始化
        self.time = -1 # 时间戳初始化
        self.hungry = 30 # 饱食度初始化
        self.health = 30 # 生命值初始化
        self.gamemode = 1 # 游戏模式初始化（默认为生成模式）
        self.reborn_x = self.coordinate_x # 设置重生x轴
        self.reborn_y = self.coordinate_x # 设置重生y轴
        self.reborn = 1 # 是否禁止重生（初始化为允许）
        self.bag = [] # 背包初始化
        self.staging = [["   ","   ","   "],["   ","   ","   "],["   ","   ","   "]] # 工作台初始化
        self.finishblock = "   " # 完成台初始化
        self.version = "1.3.4 y" # 版本号初始化
        self.wrong_info = "" # 错误内容（默认值为无，也就是不显示）
        self._gamemode = "生存模式" # 用于输出的游戏模式（默认为生成模式）
        self.file = [] # 存档码初始化
        self.ground_height = 200 # 世界高度初始化
        self.type = "Normal" # 世界类型初始化
        self.animal_type = "Normal" # 生物群系类型初始化
        self.sea_high = "200" # 海平面初始化
        
        # @note 这部分定义所有的方块信息
        self.list_block = [                                             
["0"   ,"空气方块" ,"air"         ,"\033[48;2;50;233;223m\033[30m  "  ,"不可破坏",0 ,None ,-1,"\033[48;2;50;233;223m\033[30m！\033[0m"         ],
["1"   ,"树叶方块" ,"leaf"        ,"\033[48;2;64;192;32m  "           ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;64;192;32m\033[30m！\033[m"           ],
["2"   ,"木头方块" ,"wood"        ,"\033[48;2;128;128;16m▒▒"          ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;128;128;16m\033[30m！\033[m"          ],
["3"   ,"石头方块" ,"stone"       ,"\033[48;2;192;192;192m  "         ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;192;192;192m\033[30m！\033[m"         ],
["4"   ,"草"       ,"grass"       ,"\033[48;2;50;233;223m\033[32mω "  ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;50;233;223m\033[32m\033[30m！\033[m"  ],
["5"   ,"花"       ,"flower"      ,"\033[48;2;50;233;223m\033[31m✿ " ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;50;233;223m\033[30m！\033[0m"         ],
["6"   ,"坚硬石"   ,"hard stone"  ,"\033[40m  "                       ,"可破坏"  ,1 ,None ,2 ,"\033[40m\033[30m！\033[0m"                      ],
["7"   ,"铜方块"   ,"copper"      ,"\033[48;2;150;150;0m  "           ,"可破坏"  ,1 ,None ,1 ,"\033[48;2;150;150;0m\033[30m！\033[m"           ],
["8"   ,"钻方块"   ,"drill"       ,"\033[1;46m  "                     ,"可破坏"  ,1 ,None ,2 ,"\033[1;46m\033[30m！\033[m"                     ],
["9"   ,"土方块"   ,"soil"        ,"\033[48;5;52m  "                  ,"可破坏"  ,1 ,None ,0 ,"\033[48;5;52m\033[30m！\033[m"                  ],
["10"  ,"岩浆"     ,"lava"        ,"\033[48;2;255;96;0m  "            ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;255;96;0m\033[30m！\033[m"            ],
["11"  ,"草方块"   ,"grass block" ,"\033[48;5;52m\033[38;5;118m▀▀"    ,"可破坏"  ,1 ,None ,0 ,"\033[48;5;52m\033[30m！\033[m"                  ],
["12"  ,"木板方块" ,"wooden block","\033[48;2;240;224;128m  "         ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;240;224;128m\033[30m！\033[m"         ],
["13"  ,"沙子"     ,"sand"        ,"\033[48;2;240;240;128m  "         ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;240;240;128m\033[30m！\033[m"         ],
["14"  ,"水"       ,"water"       ,"\033[48;2;0;128;255m  "           ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;0;128;255m\033[30m！\033[m"           ]]
        
        # @note 这部分定义所有的方块id
        self.list_block_id = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:13}
        
        # @note 这部分定义所有的生物实体
        self.list_animal = [                                          
["1" ,"猪" ,"pig" ,"\033[48;2;50;233;223m🐖 \033[0m" ,"猪肉 x1" ,2 ,20 ,False ,-1 ],  # 1       猪
["2" ,"牛" ,"cow" ,"\033[48;2;50;233;223m🐂 \033[0m" ,"牛肉 x1" ,2 ,20 ,False ,-1 ]]  # 2       牛

        # @note 这部分定义所有一级地形（群系）
        self.list_map_first = [                                      
["1" ,"山地" ,"mountainous region" ,"\033[48;5;52m\033[38;5;118m▀▀\033[m" ,1 ,True]] # 1        山地

        # @note 这部分定义所有的二级地形
        self.list_map_second = [                                    
["1" ,"树"   ,"tree"      ,2 ,True  ],  # 1     树
["2" ,"矿洞" ,"mine cave" ,2 ,True  ],  # 2     矿洞
["3" ,"矿井" ,"groove"    ,2 , False]]  # 3     矿井（已弃用）

        # @note 这部分定义所有的短字符指令（可执行）
        self.list_order_short = [                            
["a" ,0 ,"让主人公向左移动一格" ,1], 
["s" ,0 ,"让主人公向下移动一格" ,1], 
["d" ,0 ,"让主人公向右移动一格" ,1], 
["w" ,0 ,"让主人公向上移动一格" ,1]]

        # @note 这部分定义所有的长字符指令（可执行）
        self.list_order_long = [                                  
["bigscreen" ,0 ,"将屏幕显示设置改为大屏幕"   ,1],
["seed"      ,0 ,"显示地图种子"               ,1],
["version"   ,0 ,"显示游戏版本号"             ,1],
["exit"      ,0 ,"以一个完整的流程退出游戏"   ,1],
["info"      ,0 ,"显示游戏全部信息"           ,1],
["eat"       ,1 ,"吃下指定食物"               ,1],
["e"         ,0 ,"打开背包"                   ,1],
["reborn"    ,0 ,"显示重生数据"               ,1],
["move"      ,2 ,"将玩家移动到地图指定位置"   ,2],
["savefile"  ,0 ,"输出游戏存档码"             ,1],
["put"       ,2 ,"将指定方块放置到指定位置"   ,1],
["break"     ,1 ,"破坏指定位置的方块"         ,1],
["change_"   ,2 ,"改变指定游戏变量为指定数值" ,2],
["id"        ,2 ,"显示指定坐标处的方块信息"   ,1]]

        # @note 这部分定义所有的方块标签
        self.list_block_tag = [
"tag_unbreakable", # 规定方块不可破坏
"tag_interaction", # 规定方块可以进行交互
"tag_plant", # 规定方块可以在上方生成植物
"tag_ore_replaceable", # 规定方块可以被替换为矿石
"tag_through", # 规定方块可以穿过
"tag_gravity", # 规定方块受重力影响
"tag_oxygen", # 规定处于方块中会消耗氧气值
"tag_fluid", # 规定方块是流体
"tag_replaceable", # 规定方块可以被直接替换为别的方块
"tag_entity_can_spawn_on", # 规定方块上可以生成实体
"tag_no_data", # 规定方块是否需要存储信息
"tag_unreplaceable", # tag_replaceable的反义
"tag_solid_block"] # 规定是否是固体方块
    
    def create_player(self):time.sleep(0.1) # 你没看错！就是个老玩家！
    def create_world(self,seed):
        self.seed = seed
        # 以下是一些常用的柏林噪声计算函数
        # Copyright [C] 2023 LinLin 一些柏林噪声函数
        def rn(seed,x):random.seed(seed);r = random.uniform(-1, x);r = (int(str(r)[-1])-5)/5;return r
        def rn2(seed,x,y):
            random.seed(seed);b = random.uniform(-1, x)
            b2 = random.uniform(-1, y);r = (int(str(b/b2)[-1])-5)/5
            return r
        def rn3(seed,x,y):
            random.seed(seed);b = random.uniform(-1, y)
            b2 = random.uniform(-1, x);r = (int(str(b/b2)[-1])-5)/5
            return r
        def twist(x):return x**3 * (x**2 * 6 - x * 15 + 10)
        def dot(x,y,xv,yv):return xv*x + yv*y
        def lerp(y1,y2,w):return y1 + (y2 - y1) * w
        def noise2d(gx1,gy1,gx2,gy2,gx3,gy3,gx4,gy4,h,l):
            x = []
            for x_ in range(l):x = x + [x_]*l
            y = list(range(l));y = y*l
            x = amap(x);y = amap(y);y = y/l;x = x/l;w = twist(x);w2 = twist(y);xv2 = x-1;yv3 = y-1
            d1 = dot(gx1,gy1,x,y);d2 = dot(gx2,gy2,xv2,y);d3 = dot(gx3,gy3,x,yv3);d4 = dot(gx4,gy4,xv2,yv3)
            noise = (lerp(lerp(d1,d2,w),lerp(d3,d4,w),w2))*h/2;return list(noise.l)
        def noise1d(rx1,rx2,h,l):
            xv1 = amap(range(l));xv1 = xv1/l;xv2 = xv1-1;w = twist(xv1)
            d1 = dot(rx1,0,xv1,0);d2 = dot(rx2,0,xv2,0);noise = (lerp(d1,d2,w))*h;return list(noise.l)
        def noise1dx(dox1,dox2,seed,h,l):
            noisex = []
            for ixc in range(int((dox2-dox1)/l)):
                rx1 = rn(seed,dox1+ixc*l);rx2 = rn(seed,dox1+ixc*l+l);noid = noise1d(rx1,rx2,h,l);noisex = noisex+noid
            return noisex
            
        # 开始生成地形
        for ix in range(int(len(self.map_list)//200)):
            rx1 = rn(self.seed,ix*200);rx2 = rn(self.seed,ix*200+200)
            noi1t1 = noise1d(rx1,rx2,20,200);noi1t2 = noise1dx(ix*200,ix*200+200,self.seed,2,20)
            noi1 = [noi1t1[i]+noi1t2[i] for i in range(len(noi1t1))]
            #list(np.array(noi1t1)+np.array(noi1t2))
            for x_ in range(ix*200,ix*200+200):
                for q in range(int(noi1[x_%200]*10+200)):
                    if self.map_list[399-q][x_] == "0":
                        self.map_list[399-q][x_] = "3";self.ground_height = noi1[x_%200]*10+200
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "3" and self.map_list[i-1][j] == "0":
                    self.map_list[i][j] = "11"
                    try:
                        for w in range(1,4):self.map_list[i+w][j] = "9"
                    except:pass
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "11":
                    try:
                        if self.map_list[i-1][j] == "0":
                            if self.map_list[i+1][j] == "0":
                                flower_random = random.randint(1,4)
                                if flower_random == 1:self.map_list[i-1][j] = "4"
                                if flower_random == 2:self.map_list[i-1][j] = "5"
                    except:pass
        for ix in range(int(len(self.map_list)//200)):
            for iy in range(int(len(self.map_list)//200)):
                dox6 = ix*200;dox7 = ix*200+200;doy6 = iy*200;doy7 = iy*200+200
                gx1 = rn2(self.seed,dox6,doy6);gx2 = rn2(self.seed,dox7,doy6);gx3 = rn2(self.seed,dox6,doy7);gx4 = rn2(self.seed,dox7,doy7)
                gy1 = rn3(self.seed,dox6,doy6);gy2 = rn3(self.seed,dox7,doy6);gy3 = rn3(self.seed,dox6,doy7);gy4 = rn3(self.seed,dox7,doy7)
                noi2 = noise2d(gx1,gy1,gx2,gy2,gx3,gy3,gx4,gy4,20,200)
                for x_ in range(ix*200,ix*200+200):
                    for y_ in range(iy*200,iy*200+200):
                        if noi2[x_%200*200+y_%200]<=0.2 and noi2[x_%200*200+y_%200]>=-0.2 and self.map_list[y_][x_] != "6":self.map_list[y_][x_] = "0"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "11":
                    if self.map_list[i-1][j] == "0":
                        tree_create = random.randint(1,12)
                        if tree_create == 1:
                            try:
                                if self.map_list[i][j+1] == "0":
                                    for x in range(1,random.randint(5,7)):self.map_list[i-x][j] = "2"
                            except:pass
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "2":
                    if self.map_list[i-1][j] == "0":
                        leave_height = random.randint(2,3);leave_width = random.randint(2,3)
                        if leave_height >= 2:
                            self.map_list[i-1][j] = "1";self.map_list[i-2][j] = "1";self.map_list[i][j+1] = "1";self.map_list[i][j-1] = "1"
                            if leave_width >= 2:
                                self.map_list[i-1][j+1] = "1";self.map_list[i-2][j+1] = "1"
                                self.map_list[i-1][j-1] = "1";self.map_list[i-2][j-1] = "1";self.map_list[i-1][j+2] = "1"
                                self.map_list[i-2][j+2] = "1";self.map_list[i-1][j-2] = "1";self.map_list[i-2][j-2] = "1"
                                if leave_width == 3:self.map_list[i-1][j+3] = "1";self.map_list[i-1][j-3] = "1"
                            if leave_height == 3:
                                self.map_list[i-3][j] = "1"
                                if leave_width >= 2:
                                    self.map_list[i-1][j+1] = "1";self.map_list[i-2][j+1] = "1"
                                    self.map_list[i-1][j-1] = "1";self.map_list[i-2][j-1] = "1";self.map_list[i-1][j+2] = "1"
                                    self.map_list[i-2][j+2] = "1";self.map_list[i-1][j-2] = "1";self.map_list[i-2][j-2] = "1"
                                    if leave_width == 3:self.map_list[i-1][j+3] = "1";self.map_list[i-1][j-3] = "1"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "3":
                    if self.map_list[i-1][j] != "9":
                        mineral_random = random.randint(1,200)
                        if mineral_random == 1:self.map_list[i][j] = "8"
                        if mineral_random >= 2 and mineral_random <= 20:self.map_list[i][j] = "7"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if i == len(self.map_list[i])-1:self.map_list[i][j] = "6"
                if i >= len(self.map_list[i])-6:
                    if random.randint(0,1) == 1:self.map_list[i][j] = "6"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if i >= len(self.map_list[i])-11 and self.map_list[i][j] == "0":self.map_list[i][j] = "10"
    
    def game_begin(self):
        # 游戏开始方法 
        _printf.printf("""欢迎来到Subsist游戏1.3.4！""")
        input("任意键继续>>")
        print("\033c",end="")
        _printf.set_time(0)
        _printf.printf("""Subsist 1.3.4 Mod Update
1.代码部分
    ·删减了一些不必要的代码
    -·背包部分——因为版本兼容被暂时删除，后续会陆续加入
    -·system修复函数——这个函数因为xes版本问题被永久删除，这个无用函数的加入会影响运行速度
    -·一些不必要的注释——这些注释会影响代码阅读质量
    -·使用python 3.00x更新的分隔符“;”提升代码质量，缩减代码
2.关于模组
    ·是的！自从1.2被删除的模组功能重新归来！这次将具有更完备更标准的模组教程，将另发一次作品进行讲解！
    ·接下来我将对1.3.4模组功能进行概述：
    -·你可以在296行发现Subsist_Mod_类，如果你需要编写一个自己的模组，可以先把_后的空格改为模组的名称并将__init__里的self.use_mod布尔值改为True
    -·接着，就可以编写你的模组了！模组内容分为四部分：
        -·定义部分，也就是__init__，你需要按照注释修改剩余已经定义但参数为空的几个属性，如果有需要可以添加属性（用于修改Subsist类中已知的属性）
        -·游戏开始前，方法before_game，在其中添加在游戏循环开始前的内容
        -·游戏开始中，方法cycle，这里面的内容每个循环执行一次
        -·游戏结束，方法after_game，当游戏通过指令结束或玩家死亡后执行
    -·如果您对游戏非常了解，且具有能力，可以忽略这个类，自行编写并在游戏各部分插入实例化或调用方法！
    -·第一个官方模组即将发布！请大家敬请期待！""")
        input("任意键继续>>")
        
        # 游戏设置选项（内容扩充中）
        # 对下方使用的选择返回值储存函数进行声明
        gamemodeset1 = None;gamemodeset2 = None 
        print("\033c",end="")
        while gamemodeset1 != "开始游戏":                                     
            gamemodeset1 = _composite.unary_choose(["名称","种子","读取存档","世界设置","开始游戏"],"选择：")
            if gamemodeset1 == "名称":                                 
                gamemodeset2 = _composite.unary_choose(["世界名称","玩家名称"],"名称：")
                if gamemodeset2 == "世界名称":self.world_name = input("请输入世界名称：")
                elif gamemodeset2 == "玩家名称":self.player_name = input("请输入玩家名称：")
            elif gamemodeset1 == "种子":self.seed = input("请输入种子:")  
            elif gamemodeset1 == "读取存档":input("敬请期待...\n任意键继续>>>")
            elif gamemodeset1 == "世界设置":input("敬请期待...\n任意键继续>>>")
        
        # print("\033c",end="")
        print()
        _printf.printf(f"{self.player_name}的世界{self.world_name}设置：")
        _printf.printf(f"·世界种子：{self.seed}")
        _printf.printf(f"·世界地形高度：{self.ground_height}")
        _printf.printf(f"·世界类型：{self.type}")
        _printf.printf(f"·生物群系类型：{self.animal_type}")
        _printf.printf(f"·海平面：{self.sea_high}")
        _printf.set_time(0) # 将间隔时间初始化
        input("确认游戏设置后继续>>")
        
        print("正在加载玩家...");self.create_player() # 调用自身类方法生成玩家                         
        print("正在加载地形...");self.create_world(self.seed) # 调用自身类方法生成世界      
        
    def main_cycle(self):  
        try:
            while self.map_list[self.coordinate_x+1][self.coordinate_y] == "0":self.coordinate_x += 1
        except:pass
        last_color = ""
        
        # 主循环开始
        while True: 
            print("\033c",end="")
            
            # 用于地图输出的一些函数
            coordinate_x2 = self.coordinate_x-6;coordinate_y2 = self.coordinate_y-9
            try:
                print("┏"+36*"━"+"┓")
                for i in range(16): 
                    print("\033[0m┃",end="")
                    for j in range(18):
                        try:
                            if self.list_block[int(self.map_list[coordinate_x2][coordinate_y2])][3] == last_color and j != 0:print("  ",end = "")
                            else:print(self.list_block[int(self.map_list[coordinate_x2][coordinate_y2])][3],end="")
                            last_color = self.list_block[int(self.map_list[coordinate_x2][coordinate_y2])][3]
                        except:print("\033[48;2;147;112;219m  \033[m",end="")
                        coordinate_y2 = coordinate_y2 + 1;time.sleep(0.001)
                    print("\033[0m┃\n",end="")         
                    coordinate_y2 = coordinate_y2 - 18;coordinate_x2 = coordinate_x2 + 1
            except:raise("警告：地图输出错误！")
            print("┗"+36*"━"+"┛\033[48;2;0;0;0m")
            gotoxy(8,20,self.list_block[int(self.map_list[self.coordinate_x][self.coordinate_y])][8])
            
            # 存档码内容：以列表存储，第一格为查看游戏是否兼容
            # 剩下均为游戏存档内容，以此可以查看下一行的代码（与上方__init__注释对应）
            self.file = ["1.3.3",self.seed,self.time,self.world_name,self.player_name,self.coordinate_x,self.coordinate_y,self.hungry,self.health,self.gamemode,self.reborn_x,self.reborn_y,self.reborn,self.bag,self.staging,self.finishblock]
            self.time += 1 # 时间戳流逝                                                        
            if self.time == 25:self.time = 1 # 当时间戳到25时自动归1（防止一天出现25小时）                                        
            self.hungry -= 1 # 饱食度下降   
            self._gamemode = "生存模式" if self.gamemode == 1 else "创造模式" if self.gamemode == 2 else "信任模式"
                  
            gotoxy(20,1,"")                                               
            print(f"┃ [饱食度]:{str(self.hungry)}      [生命值]:{str(self.health)}")
            print(f"┃ [x]:{str(self.coordinate_y)}  [y]:{str(self.coordinate_x)}  [游戏模式]:{self._gamemode}")
            if self.wrong_info != "":
                print(self.wrong_info);self.wrong_info = ""
            print("┃ 请输入指令：(/help获取指令)")
            ch = _press.getch()
            
            # 短字符指令解析器
            if ch == "w":                                                      
                if self.map_list[self.coordinate_x-1][self.coordinate_y] in self.no_collide:self.coordinate_x -= 1
            elif ch == "s":                                                    
                if self.map_list[self.coordinate_x+1][self.coordinate_y] in self.no_collide:self.coordinate_x += 1
            elif ch == "a":                                                  
                if self.map_list[self.coordinate_x][self.coordinate_y-1] in self.no_collide:self.coordinate_y -= 1
            elif ch == "d":                                                     
                if self.map_list[self.coordinate_x][self.coordinate_y+1] in self.no_collide:self.coordinate_y += 1
            
            # 长字符指令解析器
            elif "/" in ch:
                ch = input("/")
                ch3 = ch.split(" ")
                if ch == "help":
                    print("Subsist Wiki正在编写中......");input("任意键继续>>")
                elif ch == "seed":self.wrong_info = "┃ [命令解析器]:种子:"+self.seed
                elif ch == "version":self.wrong_info = "┃ [命令解析器]:版本号:"+self.version   
                elif ch == "exit":sys.exit(0)                               
                elif "eat" in ch:                                               
                    try:self.hungry += self.list_animal[int(ch3)-1][4];self.bag.move(self.list_animal[int(ch3)][3])
                    except:self.wrong_info = "┃ [命令解析器]:食物不存在！"
                elif ch == "gamemode":self.wrong8 = 0   
                
                # 作废的背包代码
                # elif ch == "e":pass
                
                elif "move" in ch:                                           
                    if self.gamemode > 1:
                        try:
                            self.map_list[self.coordinate_x][self.coordinate_y] = " " 
                            self.coordinate_y = int(ch3[1]);self.coordinate_x = int(ch3[2])
                        except:self.wrong_info = "┃ [命令解析器]:命令参数不合法！"
                    else:self.wrong_info = "┃ [命令解析器]:你无权调用此指令！"
                elif ch == "savefile":                                          
                    print("你可以复制存档码，当你重新运行游戏时输入存档码，就可以还原你当前的游戏状态，请务必复制完全存档码，包括[]\n")
                    _printf.set_time(0.003)
                    _printf.printf(str(self.file)+"\n")
                    input("任意键继续>>")
                elif "put" in ch:                                                
                    if self.list_block[int(ch3[1])-1][1]+" x1" in self.bag:
                        self.bag.remove(self.list_block[int(ch3[1])-1][1]+" x1")
                        if ch3[2] == "w":self.map_list[self.coordinate_x-1][self.coordinate_y] = str(int(ch3[1])-1)
                        if ch3[2] == "s":self.map_list[self.coordinate_x+1][self.coordinate_y] = str(int(ch3[1])-1)
                        if ch3[2] == "d":self.map_list[self.coordinate_x][self.coordinate_y+1] = str(int(ch3[1])-1) 
                        if ch3[2] == "a":self.map_list[self.coordinate_x][self.coordinate_y-1] = str(int(ch3[1])-1)
                        else:self.wrong_info = "┃ [命令解析器]:命令参数不合法！"
                elif "break" in ch:
                    if len(self.bag) < 12:
                        try:
                            if ch3[1] == "w":
                                self.bag.append(str(self.list_block[int(self.map_list[self.coordinate_x-1][self.coordinate_y])-1][1])+" x1")
                                self.map_list[self.coordinate_x-1][self.coordinate_y] = " "
                            if ch3[1] == "s":
                                self.bag.append(str(self.list_block[int(self.map_list[self.coordinate_x+1][self.coordinate_y])-1][1])+" x1")
                                self.map_list[self.coordinate_x+1][self.coordinate_y] = " "
                            if ch3[1] == "d":
                                self.bag.append(str(self.list_block[int(self.map_list[self.coordinate_x][self.coordinate_y+1])-1][1])+" x1")
                                self.map_list[self.coordinate_x-1][self.coordinate_y] = " "
                            if ch3[1] == "a":
                                self.bag.append(str(self.list_block[int(self.map_list[self.coordinate_x][self.coordinate_y-1])-1][1])+" x1")
                                self.map_list[self.coordinate_x-1][self.coordinate_y] = " "
                        except:self.wrong_info = "┃ [命令解析器]:命令参数不合法！"
                    else:self.wrong_info = "┃ [命令解析器]:背包空间不足"
                elif "change_" in ch:                                           
                    if self.gamemode > 1:
                        try:
                            if "health" in ch:                               
                                if int(ch3[1]) <= 100:self.health = int(ch3[1])
                            elif "hungry" in ch:                         
                                if int(ch3[1]) <= 100:self.hungry = int(ch3[1])
                            elif "time" in ch:                               
                                if int(ch3[1]) <= 24:self.a = int(ch3[1])
                            elif "gamemode" in ch:                                
                                if int(ch3[1]) == 1 or int(ch3[1]) == 2 or int(ch3[1]) == 3:self.gamemode = int(ch3[1])
                            elif "reborn" in ch:                               
                                if text1 != " ":
                                    self.reborn_x = int(ch3[2]);self.reborn_y = int(ch3[1])
                        except:self.wrong_info = "┃ [命令解析器]:命令参数不合法！"
                    else:self.wrong_info = "┃ [命令解析器]:你无权调用此指令！"         
                else:                                                            
                    ch = "/"+ch
                    self.wrong_info = "┃ [命令解析器]:命令不存在！"
            else:self.wrong_info = "┃ [命令解析器]:命令不存在！"                
    
_Subsist = Subsist() # 游戏内容实例化
_Subsist.game_begin() # 调用游戏方法进入游戏设置
_Subsist.main_cycle() # 调用游戏方法开始游戏主循环
