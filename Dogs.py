from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO


def get_dog_image():
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        response.raise_for_status()
        data = response.json()
        return data['message']
    except Exception as e:
        mb.showerror("Ошибка", f"Возникла ошибка при запросе к API {e}")
        return None


def show_image():
    image_url = get_dog_image()
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img_size = (int(width_spin.get()), int(heigth_spin.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)
            new_window = Toplevel()
            new_window.title("Случайное изображение")
            lbl = ttk.Label(new_window, image=img)
            lbl.pack()
            lbl.image = img

            label.config(image=img)
            label.image = img
        except Exception as e:
            mb.showerror("Ошибка", f"Возникла ошибка при загрузке изображения {e}")
    progress_bar.stop()


def progress():
    progress_bar['value'] = 0
    progress_bar.start(30)
    window.after(3000, show_image)


window = Tk()
window.title("Картинки с собачками")
window.geometry("500x660")

label = ttk.Label()
label.pack(expand=True, pady=10)

button = ttk.Button(text="Загрузить изображение", command=progress)
button.pack(fill=BOTH, pady=10)

progress_bar = ttk.Progressbar(mode="determinate", length=300, orient=HORIZONTAL)  # , orient=HORIZONTAL
progress_bar.pack(fill=BOTH, pady=10)

width_label = ttk.Label(text="Ширина")
width_label.pack(side=LEFT, padx=(10, 0))
width_spin = ttk.Spinbox(from_=200, to=500, increment=50, width=5)  # , textvariable=width_label
width_spin.pack(side=LEFT, padx=(0, 10))

heigth_label = ttk.Label(text="Высота")
heigth_label.pack(side=LEFT, padx=(10, 0))
heigth_spin = ttk.Spinbox(from_=200, to=500, increment=50, width=5)  # , textvariable=width_label
heigth_spin.pack(side=LEFT, padx=(0, 10))

window.mainloop()
