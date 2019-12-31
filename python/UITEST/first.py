#coding:utf-8
#这个脚本是用来生成界面
from Tkinter import  *
from tkMessageBox import  showinfo,showwarning,showerror
from Tix import ComboBox

def btnOkClick():
    print "Hello"
def scaleClick(ev=None):
    print scale.get()
scaleLam=lambda : showinfo("gggg")
top=Tk()
# top.geometry('250 X 600')

btnOK=Button(top,text="OK",command=btnOkClick)
btnOK.pack(fill=X)
btnCancle=Button(top,text="cancle",command=top.quit,bg='red',fg='white')
btnCancle.pack()

scale = Scale(top,orient=HORIZONTAL,command=scaleClick)
scale.pack()

# # box = ComboBox(top,lable="type:",editable=True)
# # for animal in('dog','cat','rit'):
# #     box.insert(END,animal)
# box.pack()
#TODO:如何水平排列
mainloop()

