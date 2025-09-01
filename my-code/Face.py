from tkinter import *
from tkinter import messagebox
import cv2
import face_recognition
import os
import threading

# Khai báo đường dẫn tương đối đến thư mục lưu ảnh Face ID
FACE_DIR = 'Face'

# Tạo một cửa sổ Tkinter cho camera
camera_window = None
capture_thread = None
is_running = False

# Hàm nhấn biến mất ở ô username
def user_enter(event):
    if usernameEntry.get() == 'Tên tài khoản':
        usernameEntry.delete(0, END)

# Hàm đóng camera
def close_camera(cap):
    global camera_window, is_running
    is_running = False
    cap.release()
    cv2.destroyAllWindows()
    if camera_window:
        camera_window.destroy()
        camera_window = None

# Hàm xử lý luồng camera
def camera_thread_handler(mode):
    global camera_window, is_running
    is_running = True
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror('Lỗi', 'Không thể mở camera.')
        return

    # Tạo cửa sổ hiển thị camera
    cv2.namedWindow('Camera')
    
    # Thêm nút thoát cho cửa sổ camera
    cv2.setMouseCallback('Camera', lambda event, x, y, flags, param: None)
    
    # Hiển thị camera trong luồng riêng
    while is_running:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Camera', frame)
        
        # Nhấn 'q' để thoát cửa sổ camera
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if mode == 'register':
            process_register_frame(frame, cap)
        elif mode == 'login':
            process_login_frame(frame, cap)

    close_camera(cap)

# Hàm xử lý đăng ký
def process_register_frame(frame, cap):
    global is_running
    username = usernameEntry.get().lower()

    if not username or username == 'Tên tài khoản':
        messagebox.showerror('Lỗi', 'Vui lòng nhập tên tài khoản.')
        close_camera(cap)
        return

    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        # Kiểm tra xem tên người dùng đã tồn tại hay chưa
        if os.path.exists(os.path.join(FACE_DIR, f"{username}_R.jpg")):
            messagebox.showerror('Lỗi', 'Tên tài khoản này đã đăng ký Face ID.\nVui lòng tạo tên tài khoản mới.')
            close_camera(cap)
            return

        # Lưu ảnh vào file
        cv2.imwrite(os.path.join(FACE_DIR, f"{username}_R.jpg"), frame)
        messagebox.showinfo('Thông báo', 'Đăng ký thành công.')
        close_camera(cap)
        is_running = False
        face_window.after(100, face_window.destroy)

# Hàm xử lý đăng nhập
def process_login_frame(frame, cap):
    global is_running
    username = usernameEntry.get().lower()
    
    path = os.path.join(FACE_DIR, f"{username}_R.jpg")
    if not os.path.exists(path):
        messagebox.showerror('Lỗi', 'Tên tài khoản chưa đăng ký Face ID.')
        close_camera(cap)
        return
        
    try:
        # Load ảnh của người dùng và ảnh đã chụp từ file
        faceR = face_recognition.load_image_file(path)
        faceL = frame
        
        faceR_encodings = face_recognition.face_encodings(faceR)
        faceL_encodings = face_recognition.face_encodings(faceL)

        if not faceR_encodings or not faceL_encodings:
            messagebox.showerror('Lỗi', 'Không tìm thấy khuôn mặt trong ảnh.')
            return

        # So sánh hai mã hóa khuôn mặt
        results = face_recognition.compare_faces([faceR_encodings[0]], faceL_encodings[0])

        if results[0]:
            messagebox.showinfo('Thông báo', 'Đăng nhập thành công.')
            close_camera(cap)
            is_running = False
            face_window.after(100, face_window.destroy)
        else:
            messagebox.showerror('Lỗi', 'Khuôn mặt không khớp.\nVui lòng thử lại.')
            close_camera(cap)
            return
            
    except Exception as e:
        messagebox.showerror('Lỗi', f'Đã xảy ra lỗi: {e}')
        close_camera(cap)
        return

# Hàm hành động sau khi nhấn nút đăng ký
def register():
    global capture_thread
    if capture_thread and capture_thread.is_alive():
        messagebox.showinfo('Thông báo', 'Camera đang hoạt động. Vui lòng thử lại sau.')
        return
    
    capture_thread = threading.Thread(target=lambda: camera_thread_handler('register'))
    capture_thread.daemon = True
    capture_thread.start()

# Hàm hành động sau khi nhấn nút đăng nhập
def login():
    global capture_thread
    if capture_thread and capture_thread.is_alive():
        messagebox.showinfo('Thông báo', 'Camera đang hoạt động. Vui lòng thử lại sau.')
        return
        
    capture_thread = threading.Thread(target=lambda: camera_thread_handler('login'))
    capture_thread.daemon = True
    capture_thread.start()

# Giao diện
face_window = Tk()
face_window.geometry('600x600')
face_window.resizable(0, 0)
face_window.configure(bg = '#1E645A')
face_window.title('Face ID')

heading = Label(face_window, text = 'FACE ID', font = ('Font/01 Digit.ttf', 30, 'bold'), fg = 'white', bg = '#1E645A')
heading.place(x = 230, y = 110)

note = Label(face_window, text = '*Lưu ý: Camera sẽ tự động nhận diện khuôn mặt.\nHãy nhấn "q" để thoát khỏi màn hình camera.', font = ('Font/01 Digit.ttf', 13, 'bold'), fg = '#FAAA1A', bg = '#1E645A')
note.place(x = 112, y = 450)

usernameEntry = Entry(face_window, width = 25, font = ('Font/01 Digit.ttf', 20, 'bold'), fg = '#2F4F4F', bd = 0, bg = 'white')
usernameEntry.place(x = 120, y = 200)
usernameEntry.insert(0, 'Tên tài khoản')
usernameEntry.bind('<FocusIn>', user_enter)

loginButton = Button(face_window, text = 'Đăng nhập', font = ('Font/01 Digit.ttf', 20, 'bold'), fg = 'white', bg = '#FAAA1A', 
                     activeforeground = 'white', activebackground = '#FAAA1A', cursor = 'hand2', bd = 0, width = 22, command = login)
loginButton.place(x = 120, y = 280)

registerButton = Button(face_window, text = 'Đăng ký', font = ('Font/01 Digit.ttf', 20, 'bold'), fg = 'white', bg = '#FAAA1A', 
                        activeforeground = 'white', activebackground = '#FAAA1A', cursor = 'hand2', bd = 0, width = 22, command = register)
registerButton.place(x = 120, y = 350)

face_window.mainloop()