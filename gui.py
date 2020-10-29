import tkinter
def hello():
    print("hello")
top = tkinter.Tk()
top.geometry("200x200")
label = tkinter.Label(text ="下单数量")
label.pack(side="left")
order_num = tkinter.Entry()
order_num.pack(side="left")
button = tkinter.Button(text="hello",command=hello())
button.pack()
#order_num = tkinter.Entry()
#order_num = tkinter.Entry()

top.mainloop()
