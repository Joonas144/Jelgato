import tkinter as tk


def get_overlay_buttons():
    cols = 4
    rows = 2
    Buttons = [None] * cols * rows
    for i in range(0, rows):
        for j in range(0, cols):
            Buttons[j + i * 4] = Button(j + i * 4 + 1, [j, i])

    return Buttons


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.geometry("-10-40")
        # self.root.geometry("90x46")
        self.configure(bg='blue')
        self.lift()
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", "blue")
        self.attributes('-alpha', 0)

        self.buttons = get_overlay_buttons()

    def highlight(self, index, pressed):
        button = self.winfo_children()[index]

        if pressed:
            button.configure(bg="#040404")
            button.winfo_children()[0].configure(bg="#070707")
        else:
            button.configure(bg="#0d0d0d")
            button.winfo_children()[0].configure(bg="#171717")

    def updateTexts(self, texts):
        for index, button in enumerate(self.buttons):
            button.text.set(texts[index])

    def fade_in(self):
        alpha = self.attributes("-alpha")
        alpha = min(alpha + .05, 0.8)
        self.wm_attributes("-alpha", alpha)
        # app.update()
        global fadeIn
        if alpha < 0.8 and fadeIn:
            self.after(5, self.fade_in)

    def fade_out(self):
        global fadeIn
        fadeIn = False
        alpha = self.attributes("-alpha")
        alpha = max(alpha - 0.05, 0)
        self.wm_attributes("-alpha", alpha)
        self.update()
        # app.update()
        if alpha > 0:
            self.after(5, self.fade_out)


class Button(tk.Frame):
    def __init__(self, string, pos):
        super().__init__()

        self.text = tk.StringVar()
        self.text.set(string)
        self.constructCell(pos)

    def constructCell(self, pos):
        self.configure(width=50, height=50, bg="#0d0d0d")
        self.pack_propagate(0)
        self.grid(column=pos[0], row=pos[1], padx=2, pady=2)
        # self.font = TkFont.Font('Lato', '9')
        Button = tk.Label(self, textvariable=self.text, font=('Lato', '9'), bg="#171717", fg="white", width=50,
                          height=50, wraplength=40)
        Button.pack(pady=4, padx=4)


# label = tk.Label(text='Text on the screen', font=('Times','30'), fg='black', bg='white')

app = None
fadeIn = False


def start():
    global app
    app = App()


def show():
    global fadeIn
    fadeIn = True
    app.fade_in()


def hide():
    global fadeIn
    fadeIn = False
    app.fade_out()


def update():
    app.update()


def updateTexts(texts):
    app.updateTexts(texts)


def highlight(index, pressed):
    app.highlight(index, pressed)


if __name__ == "__main__":
    start()
    while True:
        app.update()
