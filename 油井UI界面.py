from tkinter import *
from PIL import Image, ImageTk


def show():
    in1 = input1.get()
    in2 = input2.get()
    print("井号: %s" % in1)
    print("月份: %s" % in2)
    input1.delete(0, END)
    input2.delete(0, END)


root = Tk()
root.title("油井信息查询UI")

# img = Image.open("油井信息查询.jpeg")
# photo = ImageTk.PhotoImage(img)
# img_label = Label(root, image=photo)
# img_label.grid(row=0, column=0, columnspan=100)

Label(root, text="井号: ").grid(row=0)
Label(root, text="月份: ").grid(row=1)
input1 = Entry(root)
input2 = Entry(root)
input1.grid(row=0, column=1, padx=10, pady=5)
input2.grid(row=1, column=1, padx=10, pady=5)

Button(root, text="查询", width=10, command=show)\
    .grid(row=3, column=0, sticky=W, padx=10, pady=5)
Button(root, text="退出", width=10, command=root.quit)\
    .grid(row=3, column=1, sticky=E, padx=10, pady=5)
root.mainloop()
