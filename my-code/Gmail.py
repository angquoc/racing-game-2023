from tkinter import *
from tkinter import messagebox
import smtplib
import random
import re

#Tạo mã ngẫu nhiên
# Biến này sẽ được dùng để lưu mã xác nhận
verification_code = 0

#Hàm nhấn biến mất ở ô email
def email_enter(event):
    if emailEntry.get() == 'Email':
        emailEntry.delete(0, END)

#Hàm nhấn biến mất ở ô code
def code_enter(event):
    if codeEntry.get() == 'Mã xác nhận':
        codeEntry.delete(0, END)

#Hàm thông báo của nút gửi
def noti():
    global verification_code
    email_address = emailEntry.get()

    if not email_address or email_address == 'Email':
        messagebox.showerror('Lỗi', 'Vui lòng nhập địa chỉ email.')
        return

    if _is_valid_email(email_address):
        # Tạo mã mới mỗi khi người dùng nhấn nút Gửi
        verification_code = random.randint(100000, 999999)
        send_email(email_address, verification_code)
        messagebox.showinfo('Thông báo', 'Mã xác nhận đã được gửi về email của bạn.\nVui lòng kiểm tra email để nhập mã xác nhận.')
    else:
        messagebox.showerror('Lỗi', 'Email không hợp lệ.')

# Kiểm tra email hợp lệ
def _is_valid_email(email):
    regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    return re.fullmatch(regex, email) is not None

#Hàm gửi email
def send_email(email, code_to_send):
    sender_email = "dtatddtn2005@gmail.com"
    receiver_email = email
    password = "etdl xerj zmoz rxgj"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        message = f"Subject: Mã xác nhận\n\nMã xác nhận của bạn là {code_to_send}."
        encoded_message = message.encode("utf-8")
        
        server.sendmail(sender_email, receiver_email, encoded_message)
        print(f"Mã xác nhận {code_to_send} đã được gửi thành công đến {email}")
        
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror('Lỗi', 'Lỗi xác thực SMTP. Vui lòng kiểm tra lại mật khẩu ứng dụng và quyền truy cập của tài khoản.')
    except Exception as e:
        messagebox.showerror('Lỗi', f'Đã xảy ra lỗi khi gửi email: {e}')
    finally:
        server.quit()

#Hàm thông báo của nút xác nhận
def accept():
    # Kiểm tra xem cả 2 trường có được điền hay không
    if not emailEntry.get() or emailEntry.get() == 'Email' or not codeEntry.get() or codeEntry.get() == 'Mã xác nhận':
        messagebox.showerror('Lỗi', 'Vui lòng điền đầy đủ thông tin.')
        return
        
    try:
        # Chuyển đổi mã nhập vào thành số nguyên để so sánh
        entered_code = int(codeEntry.get())
        if entered_code != verification_code:
            messagebox.showerror('Lỗi', 'Mã xác nhận không khớp.\nVui lòng kiểm tra lại.')
        else:
            messagebox.showinfo('Thành công', 'Xác nhận thành công!')
            register1_window.destroy()
            import Register_2
    except ValueError:
        messagebox.showerror('Lỗi', 'Mã xác nhận phải là một số.')

# Giao diện
register1_window = Tk()
register1_window.geometry('600x500')
register1_window.resizable(0, 0)
register1_window.configure(bg = '#1E645A')
register1_window.title('Đăng ký')

heading = Label(register1_window, text = 'ĐĂNG KÝ', font = ('Font/01 Digit.ttf', 30, 'bold'), fg = 'white', bg = '#1E645A')
heading.place(x = 210, y = 110)

emailEntry = Entry(register1_window, width = 25, font = ('Font/01 Digit.ttf', 20, 'bold'), fg = '#2F4F4F', bd = 0, bg = 'white')
emailEntry.place(x = 120, y = 200)
emailEntry.insert(0, 'Email')
emailEntry.bind('<FocusIn>', email_enter)

codeEntry = Entry(register1_window, width = 25, font = ('Font/01 Digit.ttf', 20, 'bold'), fg = '#2F4F4F', bd = 0, bg = 'white')
codeEntry.place(x = 120, y = 250)
codeEntry.insert(0, 'Mã xác nhận')
codeEntry.bind('<FocusIn>', code_enter)

sendButton = Button(register1_window, text = 'Gửi', font = ('Font/01 Digit.ttf', 14, 'bold'), fg = 'white', bg = '#FAAA1A', 
                     activeforeground = 'white', activebackground = '#FAAA1A', cursor = 'hand2', bd = 0, width = 3, command = noti)
sendButton.place(x = 500, y = 200)

applyButton = Button(register1_window, text = 'Xác nhận', font = ('Font/01 Digit.ttf', 18, 'bold'), fg = 'white', bg = '#FAAA1A', 
                     activeforeground = 'white', activebackground = '#FAAA1A', cursor = 'hand2', bd = 0, width = 25, command = accept)
applyButton.place(x = 120, y = 320)

register1_window.mainloop()