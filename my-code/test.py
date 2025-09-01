from tkinter import *

test_window = Tk()

#Size + màu màn hình
test_window.geometry('1600x900')
test_window.resizable(0, 0)
test_window.configure(bg = '#1E645A')

#Title
test_window.title('Test')

#Tiêu đề
heading = Label(test_window, text = 'Đây chỉ là màn hình test thay cho màn hình game :)', font = ('Font/01 Digit.ttf', 30, 'bold'), fg = 'white', bg = '#1E645A')
heading.place(x = 300, y = 110)

test_window.mainloop()