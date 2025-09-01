import os
from tkinter import *
from tkinter import messagebox
import pymysql

# Xác định đường dẫn tuyệt đối đến thư mục chứa file script này
script_directory = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn đầy đủ cho các file ảnh và font
openeye_path = os.path.join(script_directory, 'Picture', 'openeye.png')
closeeye_path = os.path.join(script_directory, 'Picture', 'closeeye.png')
font_path = os.path.join(script_directory, 'Font', '01 Digit.ttf')

#Hàm nhấn biến mất ở ô username
def user_enter(event):
    if usernameEntry.get() == 'Tên tài khoản':
        usernameEntry.delete(0, END)


#Hàm nhấn biến mất ở ô password
def password_enter(event):
    if passwordEntry.get() == 'Mật khẩu':
        passwordEntry.delete(0, END)


#Hàm ẩn password
def hide():
    openeye.config(file=closeeye_path)
    passwordEntry.config(show = '*')
    eyeButton.config(command = show)


#Hàm hiện password
def show():
    openeye.config(file=openeye_path)
    passwordEntry.config(show = '')
    eyeButton.config(command = hide)


#Hàm nối qua trang đăng ký
def register_page():
    login_window.destroy()
    import Gmail


#Hàm nối qua trang face id
def faceid_page():
    login_window.destroy()
    import Face   


#Hàm nối qua game
def test_page():
    if not usernameEntry.get() or not passwordEntry.get():
        messagebox.showerror('Lỗi', 'Hãy điền đầy đủ thông tin.')
    else:
        try:
            con = pymysql.connect(host = 'localhost', user = 'root', password = '123456')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Lỗi', 'Không thể thiết lập kết nối.\nVui lòng thử lại.')
            return
        query = 'use userdata'
        mycursor.execute(query)
        query = 'select * from data where username = %s and password = %s'
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Lỗi', 'Sai tên đăng nhập hoặc mật khẩu.')
        else:
            messagebox.showinfo('Thông báo', 'Đăng nhập thành công')
            login_window.destroy()
            import test

login_window = Tk()

#Size + màu màn hình
login_window.geometry('600x600')
login_window.resizable(0, 0)
login_window.configure(bg = '#1E645A')


#Title
login_window.title('Đăng nhập')


#Tiêu đề
heading = Label(login_window, text = 'ĐĂNG NHẬP', font = (font_path, 30, 'bold'), fg = 'white', bg = '#1E645A')
heading.place(x = 180, y = 110)


#Ô username
usernameEntry = Entry(login_window, width = 25, font = ('Font/01 Digit.ttf', 20, 'bold'), fg = '#2F4F4F', bd = 0, bg = 'white')
usernameEntry.place(x = 120, y = 200)
usernameEntry.insert(0, 'Tên tài khoản')
usernameEntry.bind('<FocusIn>', user_enter)


#Ô password
passwordEntry = Entry(login_window, width = 25, font = ('Font/01 Digit.ttf', 20, 'bold'), fg = '#2F4F4F', bd = 0, bg = 'white')
passwordEntry.place(x = 120, y = 260)
passwordEntry.insert(0, 'Mật khẩu')
passwordEntry.bind('<FocusIn>', password_enter)


#Ảnh mở/đóng password
openeye = PhotoImage(file = openeye_path)
eyeButton = Button(login_window, image = openeye, bd = 0, bg = 'white', activebackground = 'white', cursor = 'hand2', command = hide)
eyeButton.place(x = 455, y = 262)


#Nút login
loginButton = Button(login_window, text = 'Đăng nhập', font = ('Font/01 Digit.ttf', 20, 'bold'), fg = 'white', bg = '#FAAA1A', 
                     activeforeground = 'white', activebackground = '#FAAA1A', cursor = 'hand2', bd = 0, width = 22, command = test_page)
loginButton.place(x = 120, y = 350)


#Nút register
registerButton = Button(login_window, text = 'Đăng ký', font = ('Font/01 Digit.ttf', 20, 'bold'), fg = 'white', bg = '#FAAA1A', 
                     activeforeground = 'white', activebackground = '#FAAA1A', cursor = 'hand2', bd = 0, width = 22, command = register_page)
registerButton.place(x = 120, y = 420)


#Nút faceid
faceidButton = Button(login_window, text = 'Face ID', font = ('Font/01 Digit.ttf', 20, 'bold'), fg = 'white', bg = '#FAAA1A', 
                     activeforeground = 'white', activebackground = '#FAAA1A', cursor = 'hand2', bd = 0, width = 22, command = faceid_page)
faceidButton.place(x = 120, y = 490)


login_window.mainloop()