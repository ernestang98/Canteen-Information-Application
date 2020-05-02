from time import strftime
import datetime as dt
from datetime import datetime
import tkinter as tk
import pandas as pd
import random
from PIL import Image, ImageTk
from itertools import count


# Animate GIF Label
class AnimateGif(tk.Label):
    def start_image(self, image):
        if isinstance(image, str):
            image_r = Image.open(image)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(image_r.copy()))
                image_r.seek(i)
        except EOFError:
            pass

        try:
            self.delay = image_r.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_image()

    def stop_image(self):
        self.config(image=None)
        self.frames = None

    def next_image(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_image)


# Shortest Queue Function
def queue_prob(hour):
    prob_BF_1 = [1, 2, 5, 1, 1, 3]
    prob_BF_2 = [2, 3, 5, 1, 2, 3]
    prob_LUN_1 = [3, 5, 1, 3, 2, 2]
    prob_LUN_2 = [5, 3, 1, 3, 2, 1]
    prob_DIN_1 = [3, 3, 2, 5, 3, 2]
    prob_DIN_2 = [3, 3, 2, 3, 5, 2]
    if hour == 8 or hour == 9:
        return prob_BF_1
    elif hour == 10 or hour == 11:
        return prob_BF_2
    elif hour == 12 or hour == 13:
        return prob_LUN_1
    elif hour == 14 or hour == 15:
        return prob_LUN_2
    elif hour == 16 or hour == 17:
        return prob_DIN_1
    elif hour == 18 or hour == 19 or hour == 20:
        return prob_DIN_2
    else:
        return 0


# Program's Date
class TodayDate(tk.Label):

    def __init__(self, parent):
        tk.Label.__init__(self, parent)

        self.date = strftime('%d/%m/%Y')
        self.display_date = self.date
        self.configure(text=self.display_date)


# Program's Clock
class TodayClock(tk.Label):

    def __init__(self, parent=None, seconds=True):
        tk.Label.__init__(self, parent)

        self.display_seconds = seconds
        if self.display_seconds:
            self.time = strftime('%H:%M:%S')
        else:
            self.time = strftime('%I:%M %p').lstrip('0')
        self.display_time = self.time
        self.configure(text=self.display_time)
        self.after(200, self.clock_ticking)

    def clock_ticking(self):
        if self.display_seconds:
            update_timing = strftime('%H:%M:%S')
        else:
            update_timing = strftime('%I:%M %p').lstrip('0')
        if update_timing != self.time:
            self.timing = update_timing
            self.display_time = self.timing
            self.config(text=self.display_time)
        self.after(200, self.clock_ticking)


# System Functions
def system_clock(Frame, BG, FG, Font):
    clock = TodayClock(Frame)
    clock.pack(fill=tk.X)
    clock.configure(bg=BG, fg=FG, font=Font)


def system_date(Frame, BG, FG, Font):
    date = TodayDate(Frame)
    date.pack(fill=tk.X)
    date.configure(bg=BG, fg=FG, font=Font)


# Special Program's Button Functions
# Change directory of file for picture_button
def picture_button(Frame, File, BD, HT, Relief, Command, RELX, RELY, RELW, RELH):
    button_image = tk.PhotoImage(file=File)
    button = tk.Button(Frame, bd=BD, highlightthickness=HT, image=button_image, relief=Relief,
                       command=Command)
    button.image = button_image
    button.place(relx=RELX, rely=RELY, relwidth=RELW, relheight=RELH)


def picture_button2(Frame, File, BD, HT, Relief, RELX, RELY, RELW, RELH):
    button_image = tk.PhotoImage(file=File)
    button = tk.Button(Frame, bd=BD, highlightthickness=HT, image=button_image, relief=Relief)
    button.image = button_image
    button.place(relx=RELX, rely=RELY, relwidth=RELW, relheight=RELH)
    button.config(state=tk.DISABLED)


# Special Program's Label Functions
# Change directory of file for bg_label
def bg_label(Frame, File):
    bg_photo = tk.PhotoImage(file=File)
    label = tk.Label(Frame, image=bg_photo)
    label.image = bg_photo
    label.pack()


# Program's CSV File
# Change the directory of the file
df = pd.read_csv('/Users/ernestang98/Desktop/Whole_Menu.csv')


# Menu Sorting Function
def menu_display_final(store_name=df['Store Name'], day=df['Availability (Day)'], time=df['Availability (Time)']):
    menu_display = df[
        (df['Store Name'] == store_name) & ((df['Availability (Day)'] == day) | (df['Availability (Day)'] ==
                                                                                 'Everyday')) & (
                (df['Availability (Time)'] == time) | (df['Availability (Time)'] == 'AM & PM'))]
    menu_display = menu_display[['Store Name', 'Food Item', 'Price ($)']].drop_duplicates()
    return menu_display


# Random Food Generator Function
def random_food(day1, time1, num1, frame1=None):
    menu1 = (menu_display_final(day=day1, time=time1))
    rand_fd = menu1.sample(n=int(num1), replace=True)

    def structured_menu(frame1):
        store_name_list = rand_fd['Store Name'].to_string(index=False)
        food_item_list = rand_fd['Food Item'].to_string(index=False)
        price_list = rand_fd['Price ($)'].to_string(index=False)
        label1 = tk.Label(frame1, text=store_name_list, fg="white", bg='#000000')
        label1.config(font=("Verdana", 14))
        label1.place(x=90, y=360, anchor='center')
        label2 = tk.Label(frame1, text=food_item_list, fg="white", bg='#000000')
        label2.config(font=("Verdana", 14))
        label2.place(x=240, y=360, anchor='center')
        label3 = tk.Label(frame1, text=price_list, fg="white", bg='#000000')
        label3.config(font=("Verdana", 14))
        label3.place(x=400, y=360, anchor='center')

    structured_menu(frame1)
    return rand_fd


# Function to close a pop-up window
def exit_window(self):
    self.destroy()


# Program's Backbone (Skeleton)
class AppMainframe(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(10, weight=10)
        container.grid_columnconfigure(10, weight=10)

        self.frames = {}

        for F in (WelcomePage, DtPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=10, column=10, sticky="nsew")
        self.show_frame(WelcomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Program Welcome Page GUI
class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        filter_label = tk.Label(self, text="", bg="Black", font=('Verdana', 1))
        filter_label.pack(fill=tk.X)
        title_label_1 = tk.Label(self, text="Welcome to North Spine Canteen!", bg="Black",
                                 font=('Bradley Hand', 35, 'bold'), fg='white')
        title_label_1.pack(fill=tk.X)
        filter_label = tk.Label(self, text="", bg="Black", font=('Verdana', 1))
        filter_label.pack(fill=tk.X)
        opening_hour_label = tk.Label(self, text="Opening Hours: 0800 - 2000, Monday - Friday", bg="Black",
                                      font=('Verdana', 12), fg='White')
        opening_hour_label.pack(fill=tk.X)
        opening_day_label = tk.Label(self, text="AM Hours: 0800 - 1159, PM Hours: 1200 - 2000", bg="Black",
                                     font=('Verdana', 12), fg='White')
        opening_day_label.pack(fill=tk.X)
        filter_label = tk.Label(self, text="", bg="Black", font=('Verdana', 1))
        filter_label.pack(fill=tk.X)
        current_dt_label = tk.Label(self, text="Current Date & Time:", bg="Black",
                                    font=('Verdana', 12), fg='White')
        current_dt_label.pack(fill=tk.X)
        system_date(Frame=self, BG='Black', FG='White', Font=("helvetica", 12))
        system_clock(Frame=self, BG='Black', FG='White', Font=("helvetica", 12))
        bg_label(Frame=self, File="/Users/ernestang98/Desktop/foodbg1.png")
        picture_button(Frame=self, File="/Users/ernestang98/Desktop/Enter_Button.png", BD=0, HT=0, Relief=tk.RAISED,
                       Command=lambda: controller.show_frame(DtPage), RELX=0.38, RELY=0.32, RELW=0.222, RELH=0.215)
        picture_button(Frame=self, File="/Users/ernestang98/Desktop/Close_Button.png", BD=0, HT=0, Relief=tk.RAISED,
                       Command=lambda: quit(self), RELX=0.035, RELY=0.775, RELW=0.14, RELH=0.186)


# Program Date and Time Page GUI
class DtPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        filter_label = tk.Label(self, text="", bg="Black", font=('Verdana', 1))
        filter_label.pack(fill=tk.X)
        title_label_2 = tk.Label(self, text="View Menu", bg="Black",
                                 font=('Bradley Hand', 35, 'bold'), fg='White')
        title_label_2.pack(fill=tk.X)
        filter_label = tk.Label(self, text="", bg="Black", font=('Verdana', 1))
        filter_label.pack(fill=tk.X)
        opening_hour_label = tk.Label(self, text="Opening Hours: 0800 - 2000, Monday - Friday", bg="Black",
                                      font=('Verdana', 12), fg='White')
        opening_hour_label.pack(fill=tk.X)
        opening_day_label = tk.Label(self, text="AM Hours: 0800 - 1159, PM Hours: 1200 - 2000", bg="Black",
                                     font=('Verdana', 12), fg='White')
        opening_day_label.pack(fill=tk.X)
        filter_label = tk.Label(self, text="", bg="Black", font=('Verdana', 1))
        filter_label.pack(fill=tk.X)
        current_dt_label = tk.Label(self, text="Current Date & Time:", bg="Black",
                                    font=('Verdana', 12), fg='White')
        current_dt_label.pack(fill=tk.X)
        system_date(Frame=self, BG='Black', FG='White', Font=("helvetica", 12))
        system_clock(Frame=self, BG='Black', FG='White', Font=("helvetica", 12))
        bg_label(Frame=self, File="/Users/ernestang98/Desktop/foodbg2.png")

        picture_button(Frame=self,
                       File="/Users/ernestang98/Desktop/rfg.png", BD=0,
                       HT=0, Relief=tk.RAISED, Command=lambda: food_generator1(),
                       RELX=0.775, RELY=0.08, RELW=0.144, RELH=0.188)

        def food_generator1():
            current_day = strftime('%A')
            hr = strftime('%H')
            mm = strftime('%M')
            if current_day == 'Saturday' or current_day == 'Sunday':
                closed_frame = tk.Toplevel(self)
                closed_frame.geometry('475x600')
                closed_frame.resizable(width=False, height=False)
                closed_frame.title('Random Food Generator')
                bg_label(Frame=closed_frame, File='/Users/ernestang98/Desktop/bgmenu4.png')
                picture_button(Frame=closed_frame,
                               File="/Users/ernestang98/Desktop/Exit_Button_2.png", BD=0,
                               HT=0, Relief=tk.RAISED,
                               Command=lambda: closed_frame.destroy(),
                               RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)
            else:
                if int(hr) < 8 or int(hr) > 20:
                    closed_frame = tk.Toplevel(self)
                    closed_frame.geometry('475x600')
                    closed_frame.resizable(width=False, height=False)
                    closed_frame.title('Random Food Generator')
                    bg_label(Frame=closed_frame, File='/Users/ernestang98/Desktop/bgmenu4.png')
                    picture_button(Frame=closed_frame,
                                   File="/Users/ernestang98/Desktop/Exit_Button_2.png", BD=0,
                                   HT=0, Relief=tk.RAISED,
                                   Command=lambda: closed_frame.destroy(),
                                   RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)
                elif int(hr) == 20:
                    if int(mm) > 00:
                        closed_frame = tk.Toplevel(self)
                        closed_frame.geometry('475x600')
                        closed_frame.resizable(width=False, height=False)
                        closed_frame.title('Random Food Generator')
                        bg_label(Frame=closed_frame, File='/Users/ernestang98/Desktop/bgmenu4.png')
                        picture_button(Frame=closed_frame,
                                       File="/Users/ernestang98/Desktop/Exit_Button_2.png", BD=0,
                                       HT=0, Relief=tk.RAISED,
                                       Command=lambda: closed_frame.destroy(),
                                       RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)

                    else:
                        ppl_page = tk.Toplevel(self)
                        blank_label = tk.Label(ppl_page, text='', fg="white", bg='#2D2D2D', font=("Verdana", 13))
                        blank_label.pack(side=tk.TOP)
                        blank_label_d = tk.Label(ppl_page, text='How many people are eating?',
                                                 fg="white", bg='#2D2D2D', font=("Verdana", 12))
                        blank_label_d.pack(side=tk.TOP)
                        enter_ppl1 = tk.Entry(ppl_page)
                        enter_ppl1.pack(side=tk.TOP)
                        enter_ppl_button = tk.Button(ppl_page, text="Enter", command=lambda: food_generator())
                        enter_ppl_button.pack(side=tk.TOP)
                        ppl_page.geometry('350x200')
                        ppl_page.configure(background='#2D2D2D')
                        ppl_page.resizable(width=False, height=False)
                        ppl_page.title('Random Food Generator')

                        def food_generator():
                            value1 = enter_ppl1.get()
                            if value1:
                                check_number = enter_ppl1.get().isdigit()
                                if check_number:
                                    if int(value1) < 21:
                                        ppl_page.destroy()
                                        hour, minute = int(strftime('%H')), int(strftime('%M'))
                                        day = strftime('%A')
                                        fg_page = tk.Toplevel(self)
                                        blank_label_d = tk.Label(fg_page, text='', fg="white", bg='#000000',
                                                                 font=("Verdana", 10))
                                        blank_label_d.pack(side=tk.TOP)
                                        blank_label_d.after(5000, lambda: blank_label_d.destroy())
                                        lbl1 = AnimateGif(fg_page)
                                        lbl1.pack()
                                        lbl1.start_image('/Users/ernestang98/Desktop/gif.gif')
                                        lbl1.after(5000, lambda: lbl1.destroy())
                                        label3 = tk.Label(fg_page, text='', fg="white", bg='#000000',
                                                          font=("Verdana", 10))
                                        label3.pack(side=tk.TOP)
                                        label3 = tk.Label(fg_page,
                                                          text='Please wait while we provide the best suggestions for you',
                                                          fg="white", bg='#000000', font=("Verdana", 15))
                                        label3.pack(side=tk.TOP)
                                        label3.after(5000, lambda: label3.destroy())
                                        label4 = tk.Label(fg_page, text='', fg="white", bg='#000000',
                                                          font=("Verdana", 10))
                                        label4.pack(side=tk.TOP)
                                        label4.after(5000, lambda: label3.destroy())
                                        lbl2 = AnimateGif(fg_page)
                                        lbl2.pack()
                                        lbl2.start_image('/Users/ernestang98/Desktop/gif222.gif')
                                        lbl2.after(5000, lambda: lbl2.destroy())
                                        fg_page.geometry('475x600')
                                        fg_page.configure(background='#000000')
                                        fg_page.resizable(width=False, height=False)
                                        fg_page.title('Random Food Generator')

                                        def food_generator2():
                                            afg_page = tk.Toplevel(self)
                                            bg_label(Frame=afg_page, File='/Users/ernestang98/Desktop/bgmenu3.png')
                                            random_food(day1=day, time1=hour, frame1=afg_page, num1=value1)
                                            picture_button(Frame=afg_page,
                                                           File="/Users/ernestang98/Desktop/Exit_Button_2.png", BD=0,
                                                           HT=0, Relief=tk.RAISED,
                                                           Command=lambda: afg_page.destroy(),
                                                           RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)
                                            afg_page.geometry('475x600')
                                            afg_page.configure(background='#000000')
                                            afg_page.resizable(width=False, height=False)
                                            afg_page.title('Random Food Generator')

                                        fg_page.after(5000, lambda: food_generator2())
                                        fg_page.after(5000, lambda: fg_page.destroy())

                                    else:
                                        error_page = tk.Toplevel(self)
                                        blank_label = tk.Label(error_page, text='', fg="white", bg='#000000',
                                                               font=("Verdana", 13))
                                        blank_label.pack(side=tk.TOP)
                                        error_label = tk.Label(error_page,
                                                               text='Error. Enter up to 20 people per input',
                                                               fg="white",
                                                               bg='#000000', font=("Verdana", 13))
                                        error_label.pack(side=tk.TOP)
                                        error_page.configure(background='#000000')
                                        error_page.geometry('270x100')
                                        error_page.resizable(width=False, height=False)
                                        error_page.title('Error')

                                else:
                                    error_page = tk.Toplevel(self)
                                    blank_label = tk.Label(error_page, text='', fg="white", bg='#000000',
                                                           font=("Verdana", 13))
                                    blank_label.pack(side=tk.TOP)
                                    error_label = tk.Label(error_page, text='Error. Enter Digit(s) Only', fg="white",
                                                           bg='#000000', font=("Verdana", 13))
                                    error_label.pack(side=tk.TOP)
                                    error_page.configure(background='#000000')
                                    error_page.geometry('200x100')
                                    error_page.resizable(width=False, height=False)
                                    error_page.title('Error')

                            else:
                                error_page = tk.Toplevel(self)
                                blank_label = tk.Label(error_page, text='', fg="white", bg='#000000',
                                                       font=("Verdana", 13))
                                blank_label.pack(side=tk.TOP)
                                error_label = tk.Label(error_page, text='Error. Enter Digit(s) Only', fg="white",
                                                       bg='#000000', font=("Verdana", 13))
                                error_label.pack(side=tk.TOP)
                                error_page.configure(background='#000000')
                                error_page.geometry('200x100')
                                error_page.resizable(width=False, height=False)
                                error_page.title('Error')
                else:
                    ppl_page = tk.Toplevel(self)
                    blank_label = tk.Label(ppl_page, text='', fg="white", bg='#2D2D2D', font=("Verdana", 13))
                    blank_label.pack(side=tk.TOP)
                    blank_label_d = tk.Label(ppl_page, text='How many people are eating?',
                                             fg="white", bg='#2D2D2D', font=("Verdana", 12))
                    blank_label_d.pack(side=tk.TOP)
                    enter_ppl1 = tk.Entry(ppl_page)
                    enter_ppl1.pack(side=tk.TOP)
                    enter_ppl_button = tk.Button(ppl_page, text="Enter", command=lambda: food_generator())
                    enter_ppl_button.pack(side=tk.TOP)
                    ppl_page.geometry('350x200')
                    ppl_page.configure(background='#2D2D2D')
                    ppl_page.resizable(width=False, height=False)
                    ppl_page.title('Random Food Generator')

                    def food_generator():
                        value1 = enter_ppl1.get()
                        if value1:
                            check_number = enter_ppl1.get().isdigit()
                            if check_number:
                                if int(value1) < 21:
                                    ppl_page.destroy()
                                    hour, minute = int(strftime('%H')), int(strftime('%M'))
                                    day = strftime('%A')
                                    fg_page = tk.Toplevel(self)
                                    blank_label_d = tk.Label(fg_page, text='', fg="white", bg='#000000',
                                                             font=("Verdana", 10))
                                    blank_label_d.pack(side=tk.TOP)
                                    blank_label_d.after(5000, lambda: blank_label_d.destroy())
                                    lbl1 = AnimateGif(fg_page)
                                    lbl1.pack()
                                    lbl1.start_image('/Users/ernestang98/Desktop/gif.gif')
                                    lbl1.after(5000, lambda: lbl1.destroy())
                                    label3 = tk.Label(fg_page, text='', fg="white", bg='#000000', font=("Verdana", 10))
                                    label3.pack(side=tk.TOP)
                                    label3 = tk.Label(fg_page,
                                                      text='Please wait while we provide the best suggestions for you',
                                                      fg="white", bg='#000000', font=("Verdana", 15))
                                    label3.pack(side=tk.TOP)
                                    label3.after(5000, lambda: label3.destroy())
                                    label4 = tk.Label(fg_page, text='', fg="white", bg='#000000', font=("Verdana", 10))
                                    label4.pack(side=tk.TOP)
                                    label4.after(5000, lambda: label3.destroy())
                                    lbl2 = AnimateGif(fg_page)
                                    lbl2.pack()
                                    lbl2.start_image('/Users/ernestang98/Desktop/gif222.gif')
                                    lbl2.after(5000, lambda: lbl2.destroy())
                                    fg_page.geometry('475x600')
                                    fg_page.configure(background='#000000')
                                    fg_page.resizable(width=False, height=False)
                                    fg_page.title('Random Food Generator')

                                    def food_generator2():
                                        afg_page = tk.Toplevel(self)
                                        bg_label(Frame=afg_page, File='/Users/ernestang98/Desktop/bgmenu3.png')
                                        random_food(day1=day, time1=hour, frame1=afg_page, num1=value1)
                                        picture_button(Frame=afg_page,
                                                       File="/Users/ernestang98/Desktop/Exit_Button_2.png", BD=0,
                                                       HT=0, Relief=tk.RAISED,
                                                       Command=lambda: afg_page.destroy(),
                                                       RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)
                                        afg_page.geometry('475x600')
                                        afg_page.configure(background='#000000')
                                        afg_page.resizable(width=False, height=False)
                                        afg_page.title('Random Food Generator')

                                    fg_page.after(5000, lambda: food_generator2())
                                    fg_page.after(5000, lambda: fg_page.destroy())

                                else:
                                    error_page = tk.Toplevel(self)
                                    blank_label = tk.Label(error_page, text='', fg="white", bg='#000000',
                                                           font=("Verdana", 13))
                                    blank_label.pack(side=tk.TOP)
                                    error_label = tk.Label(error_page, text='Error. Enter up to 20 people per input',
                                                           fg="white",
                                                           bg='#000000', font=("Verdana", 13))
                                    error_label.pack(side=tk.TOP)
                                    error_page.configure(background='#000000')
                                    error_page.geometry('270x100')
                                    error_page.resizable(width=False, height=False)
                                    error_page.title('Error')

                            else:
                                error_page = tk.Toplevel(self)
                                blank_label = tk.Label(error_page, text='', fg="white", bg='#000000',
                                                       font=("Verdana", 13))
                                blank_label.pack(side=tk.TOP)
                                error_label = tk.Label(error_page, text='Error. Enter Digit(s) Only', fg="white",
                                                       bg='#000000', font=("Verdana", 13))
                                error_label.pack(side=tk.TOP)
                                error_page.configure(background='#000000')
                                error_page.geometry('200x100')
                                error_page.resizable(width=False, height=False)
                                error_page.title('Error')

                        else:
                            error_page = tk.Toplevel(self)
                            blank_label = tk.Label(error_page, text='', fg="white", bg='#000000', font=("Verdana", 13))
                            blank_label.pack(side=tk.TOP)
                            error_label = tk.Label(error_page, text='Error. Enter Digit(s) Only', fg="white",
                                                   bg='#000000', font=("Verdana", 13))
                            error_label.pack(side=tk.TOP)
                            error_page.configure(background='#000000')
                            error_page.geometry('200x100')
                            error_page.resizable(width=False, height=False)
                            error_page.title('Error')

        # View Menu based on system's date and time GUI
        def current_menu():
            now = datetime.now()
            t_string = now.strftime("%H:%M:%S")
            d_string = now.strftime("%Y-%m-%d")
            day, month, year = map(int, d_string.split('-'))
            hour, minute, second = map(int, t_string.split(':'))
            my_date = dt.date(day, month, year)
            my_day = my_date.strftime("%A")
            day = my_day

            custom_menu = tk.Toplevel(self)
            custom_menu.geometry('475x600')
            custom_menu.configure(background='#19221D')
            custom_menu.resizable(width=False, height=False)
            custom_menu.title('Customized Menu')

            if my_day == 'Saturday' or my_day == 'Sunday':
                bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_close.png")
            else:
                if hour < 8 or hour > 20:
                    bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_close.png")
                elif hour == 20:
                    if minute != 00:
                        bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_close.png")
                else:
                    def create_menu():
                        selected_date_label = tk.Label(custom_menu, text=(
                                'Date Selected: ' + str(d_string) + ', ' + str(day)),
                                                       fg="white", bg='#19221D', font=('Verdana', 12))
                        selected_date_label.pack(side=tk.TOP)
                        time_selected_label = tk.Label(custom_menu,
                                                       text=('Time Selected: ' + str(t_string)),
                                                       fg="white", bg='#19221D', font=('Verdana', 12))
                        time_selected_label.pack(side=tk.TOP)

                        def shortest_queue():
                            while True:
                                store = ['Yong Tau Foo', 'Chicken Rice', 'Western Food', 'Mini Wok',
                                         'Duck Rice', 'Indian']
                                hour_input = hour
                                prob_choice = queue_prob(hour_input)
                                if prob_choice == 0:
                                    break
                                else:
                                    shortest_queue = random.choices(store, prob_choice, k=1)
                                    return shortest_queue
                                    break

                        shortest_label = tk.Label(custom_menu,
                                                  text=('Shortest Queue: ' + str(
                                                      shortest_queue()).strip('[]').strip("'")),
                                                  fg="white", bg='#19221D', font=('Verdana', 12))
                        shortest_label.pack(side=tk.TOP)

                        blank_label = tk.Label(custom_menu, text='', fg="white", bg='#19221D',
                                               font=('Verdana', 100))
                        blank_label.pack(side=tk.TOP)

                        if my_day == 'Monday':
                            bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_mon.png")
                        elif my_day == 'Tuesday':
                            bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_tue.png")
                        elif my_day == 'Wednesday':
                            bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_wed.png")
                        elif my_day == 'Thursday':
                            bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_thu.png")
                        else:
                            bg_label(Frame=custom_menu, File="/Users/ernestang98/Desktop/bgmenu_fri.png")

                        if hour < 12:
                            tme = 'AM'
                        else:
                            tme = 'PM'
                        menu_display_final(day=str(my_day), time=str(tme))
                        actual_sort = menu_display_final(day=str(my_day), time=str(tme))

                        def structured_menu(frame):
                            store_name_list = actual_sort['Store Name'].to_string(index=False)
                            food_item_list = actual_sort['Food Item'].to_string(index=False)
                            price_list = actual_sort['Price ($)'].to_string(index=False)
                            label1 = tk.Label(frame, text=store_name_list, fg="white",
                                              bg='#19221D')
                            label1.config(font=("Verdana", 10))
                            label1.place(x=80, y=450, anchor='center')
                            label2 = tk.Label(frame, text=food_item_list, fg="white",
                                              bg='#19221D')
                            label2.config(font=("Verdana", 10))
                            label2.place(x=230, y=450, anchor='center')
                            label3 = tk.Label(frame, text=price_list, fg="white", bg='#19221D')
                            label3.config(font=("Verdana", 10))
                            label3.place(x=390, y=450, anchor='center')

                        structured_menu(custom_menu)

                        custom_menu.geometry('475x600')
                        custom_menu.configure(background='#19221D')
                        custom_menu.resizable(width=False, height=False)
                        custom_menu.title('Customized Menu')

                        def specific_menu(Store1):
                            specific_window = tk.Toplevel(self)
                            specific_window.geometry('475x600')
                            specific_window.configure(background='#19221D')
                            specific_window.resizable(width=False, height=False)
                            specific_window.title('Specialized Menu')

                            selected_date_label = tk.Label(specific_window, text=(
                                    'Date Selected: ' + str(d_string) + ', ' + str(day)),
                                                           fg="white", bg='#19221D',
                                                           font=('Verdana', 12))
                            selected_date_label.pack(side=tk.TOP)
                            time_selected_label = tk.Label(specific_window,
                                                           text=('Time Selected: ' + str(t_string)),
                                                           fg="white", bg='#19221D',
                                                           font=('Verdana', 12))
                            time_selected_label.pack(side=tk.TOP)
                            blank_label = tk.Label(specific_window, text='', fg="white", bg='#19221D',
                                                   font=('Verdana', 100))
                            blank_label.pack(side=tk.TOP)
                            waiting_time_label = tk.Label(specific_window,
                                                          text='Total Average Waiting Time: Enter Number '
                                                               'of People Queuing',
                                                          fg="white", bg='#19221D',
                                                          font=('Verdana', 12))
                            waiting_time_label.pack(side=tk.TOP)
                            enter_w_time = tk.Entry(specific_window)
                            enter_w_time.pack(side=tk.TOP)
                            enter_w_time_button = tk.Button(specific_window, text="Calculate",
                                                            command=lambda: calculate(self))
                            enter_w_time_button.pack(side=tk.TOP)

                            time_selected_label = tk.Label(specific_window,
                                                           text='',
                                                           fg="white", bg='#19221D',
                                                           font=('Verdana', 12))
                            time_selected_label.pack(side=tk.TOP)

                            if str(day) == 'Monday':
                                bg_label(Frame=specific_window,
                                         File="/Users/ernestang98/Desktop/bgmenu_mon.png")
                            elif str(day) == 'Tuesday':
                                bg_label(Frame=specific_window,
                                         File="/Users/ernestang98/Desktop/bgmenu_tue.png")
                            elif str(day) == 'Wednesday':
                                bg_label(Frame=specific_window,
                                         File="/Users/ernestang98/Desktop/bgmenu_wed.png")
                            elif str(day) == 'Thursday':
                                bg_label(Frame=specific_window,
                                         File="/Users/ernestang98/Desktop/bgmenu_thu.png")
                            else:
                                bg_label(Frame=specific_window,
                                         File="/Users/ernestang98/Desktop/bgmenu_fri.png")

                            def calculate(self):
                                calculate_window = tk.Toplevel(self)
                                calculate_window.title('Waiting Time')
                                calculate_window.configure(background='#19221D')
                                calculate_window.after(3000, lambda: calculate_window.destroy())
                                check_if_digit = (enter_w_time.get()).isdigit()

                                if str(Store1) == 'Japanese':
                                    val = 2
                                elif str(Store1) == 'Chicken Rice':
                                    val = 2
                                elif str(Store1) == 'Mini Wok':
                                    val = 4
                                elif str(Store1) == 'Indian Cuisine':
                                    val = 4
                                elif str(Store1) == 'Western Food':
                                    val = 5
                                else:
                                    val = 3

                                def execute():
                                    if check_if_digit:
                                        number_of_ppl = int(enter_w_time.get())
                                        total_wt = number_of_ppl * val
                                        if total_wt > 60:
                                            total_wt_label = tk.Label(calculate_window,
                                                                      text='Total waiting time: At least an hour',
                                                                      fg="white", bg='#19221D')
                                            total_wt_label.pack(side=tk.TOP)
                                        else:
                                            total_wt_label_ = tk.Label(calculate_window, text=(
                                                    'Total waiting time: ' + str(
                                                total_wt) + ' minutes'), fg="white", bg='#19221D')
                                            total_wt_label_.pack(side=tk.TOP)
                                    else:
                                        error_wt_label = tk.Label(calculate_window,
                                                                  text='Error: Enter digit(s) only',
                                                                  fg="white", bg='#19221D')
                                        error_wt_label.pack(side=tk.TOP)

                                execute()

                            def special_menu():

                                if hour < 12:
                                    tme = 'AM'
                                else:
                                    tme = 'PM'

                                menu_display_final(store_name=str(Store1), day=str(my_day), time=str(tme))
                                actual_sort1 = menu_display_final(store_name=str(Store1),
                                                                  day=str(my_day), time=str(tme))

                                def structured_menu(frame):
                                    store_name_list = actual_sort1['Store Name'].to_string(index=False)
                                    food_item_list = actual_sort1['Food Item'].to_string(index=False)
                                    price_list = actual_sort1['Price ($)'].to_string(index=False)
                                    label1 = tk.Label(frame, text=store_name_list, fg="white",
                                                      bg='#19221D')
                                    label1.config(font=("Verdana", 15))
                                    label1.place(x=80, y=415, anchor='center')
                                    label2 = tk.Label(frame, text=food_item_list, fg="white",
                                                      bg='#19221D')
                                    label2.config(font=("Verdana", 15))
                                    label2.place(x=230, y=415, anchor='center')
                                    label3 = tk.Label(frame, text=price_list, fg="white", bg='#19221D')
                                    label3.config(font=("Verdana", 15))
                                    label3.place(x=390, y=415, anchor='center')

                                structured_menu(specific_window)

                                if str(Store1) == 'Japanese':
                                    picture_button2(Frame=specific_window,
                                                    File="/Users/ernestang98/Desktop/Jap_Symbol.png",
                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                    RELX=0.36,
                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                elif str(Store1) == 'Mini Wok':
                                    picture_button2(Frame=specific_window,
                                                    File="/Users/ernestang98/Desktop/MW_Symbol.png",
                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                    RELX=0.36,
                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                elif str(Store1) == 'Western Food':
                                    picture_button2(Frame=specific_window,
                                                    File="/Users/ernestang98/Desktop/WF_Symbol.png",
                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                    RELX=0.36,
                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                elif str(Store1) == 'Indian Cuisine':
                                    picture_button2(Frame=specific_window,
                                                    File="/Users/ernestang98/Desktop/IC_Symbol.png",
                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                    RELX=0.36,
                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                elif str(Store1) == 'Chicken Rice':
                                    picture_button2(Frame=specific_window,
                                                    File="/Users/ernestang98/Desktop/CR_Symbol.png",
                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                    RELX=0.36,
                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                else:
                                    picture_button2(Frame=specific_window,
                                                    File="/Users/ernestang98/Desktop/YTF_Symbol.png",
                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                    RELX=0.36,
                                                    RELY=0.08, RELW=0.275, RELH=0.22)

                            special_menu()

                            picture_button(Frame=specific_window,
                                           File="/Users/ernestang98/Desktop/Exit_Button.png", BD=0,
                                           HT=0, Relief=tk.RAISED,
                                           Command=lambda: specific_window.destroy(),
                                           RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)

                        picture_button(Frame=custom_menu,
                                       File="/Users/ernestang98/Desktop/YTF_Button.png",
                                       BD=0, HT=0, Relief=tk.RAISED,
                                       Command=lambda: specific_menu('Yong Tau Foo'), RELX=0.06,
                                       RELY=0.115, RELW=0.16, RELH=0.125)

                        picture_button(Frame=custom_menu,
                                       File="/Users/ernestang98/Desktop/IC_Button.png",
                                       BD=0, HT=0, Relief=tk.RAISED,
                                       Command=lambda: specific_menu('Indian Cuisine'), RELX=0.06,
                                       RELY=0.255, RELW=0.16, RELH=0.125)

                        picture_button(Frame=custom_menu,
                                       File="/Users/ernestang98/Desktop/CR_Button.png",
                                       BD=0, HT=0, Relief=tk.RAISED,
                                       Command=lambda: specific_menu('Chicken Rice'), RELX=0.41,
                                       RELY=0.115, RELW=0.16, RELH=0.1275)

                        picture_button(Frame=custom_menu,
                                       File="/Users/ernestang98/Desktop/Jap_Button.png",
                                       BD=0, HT=0, Relief=tk.RAISED,
                                       Command=lambda: specific_menu('Japanese'), RELX=0.41,
                                       RELY=0.255, RELW=0.16, RELH=0.125)

                        picture_button(Frame=custom_menu,
                                       File="/Users/ernestang98/Desktop/MW_Button.png",
                                       BD=0, HT=0, Relief=tk.RAISED,
                                       Command=lambda: specific_menu('Mini Wok'), RELX=0.78,
                                       RELY=0.115, RELW=0.16, RELH=0.125)

                        picture_button(Frame=custom_menu,
                                       File="/Users/ernestang98/Desktop/WF_Button.png",
                                       BD=0, HT=0, Relief=tk.RAISED,
                                       Command=lambda: specific_menu('Western Food'), RELX=0.78,
                                       RELY=0.255, RELW=0.16, RELH=0.125)

                    create_menu()

        picture_button(Frame=self, File="/Users/ernestang98/Desktop/button1.png", BD=0, HT=0, Relief=tk.RAISED,
                       Command=lambda: current_menu(), RELX=0.385, RELY=0.35, RELW=0.239, RELH=0.035)

        # View Menu based on personalized date and time GUI
        def open_window2(self):

            window = tk.Toplevel(self)

            title_window = tk.Label(window, text='Enter personalized date and time', fg="white", bg='#19221D')
            title_window.pack(side="top", fill="both", padx=10, pady=10)

            enter_date = tk.Entry(window)
            enter_date.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.09)

            label_date = tk.Label(window, text='Date (YYYY-MM-DD):', fg="white", bg='#19221D')
            label_date.place(relx=0.25, rely=0.175, relwidth=0.5, relheight=0.08)

            enter_time = tk.Entry(window)
            enter_time.place(relx=0.35, rely=0.475, relwidth=0.3, relheight=0.09)

            label_time = tk.Label(window, text='Time (HH:MM):', fg="white", bg='#19221D')
            label_time.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.08)

            view_button = tk.Button(window, text="View Menu", command=lambda: View_Menu())
            view_button.pack(side=tk.BOTTOM)

            window.configure(background='#19221D')
            window.resizable(width=False, height=False)
            window.title('Canteen Menu Application')
            window.geometry('350x350')

            # Function to create a menu based on specified date and time
            def View_Menu():
                date_entry = enter_date.get()
                time_entry = enter_time.get()

                sorry_input = tk.Toplevel(self)
                sorry_input.resizable(width=False, height=False)
                sorry_input.configure(background='#19221D')
                sorry_input.title("Error")
                sorry_input.geometry('450x150')
                sorry_input.after(2000, lambda: sorry_input.destroy())

                try:
                    if not date_entry and not time_entry:
                        no_input = tk.Label(sorry_input, text='No Input Detected', fg="white", bg='#19221D')
                        no_input.place(x=225, y=75, anchor='center')
                    elif not date_entry:
                        no_date = tk.Label(sorry_input, text='Date Input Missing', fg="white", bg='#19221D')
                        no_date.place(x=225, y=75, anchor='center')
                    elif not time_entry:
                        no_time = tk.Label(sorry_input, text='Time Input Missing', fg="white", bg='#19221D')
                        no_time.place(x=225, y=75, anchor='center')
                    else:
                        year, month, day = map(int, date_entry.split('-'))
                        my_date = dt.date(year, month, day)
                        my_day = my_date.strftime("%A")
                        date_input = my_day
                        hour, minute = map(int, time_entry.split(':'))
                        if date_input == 'Saturday' or date_input == 'Sunday':
                            try:
                                if 20 < hour < 24 or 0 <= hour < 8:
                                    if minute >= 60 or minute < 0:
                                        error_label = tk.Label(sorry_input, text='MM must be in between 0 and 59, '
                                                                                 'Re-Enter Time in HH:MM format',
                                                               fg="white", bg='#19221D')
                                        error_label.place(x=225, y=75, anchor='center')
                                    else:
                                        close_hour = tk.Label(sorry_input, text='Canteen is closed on Weekends',
                                                              fg="white", bg='#19221D')
                                        close_hour.place(x=225, y=75, anchor='center')
                                elif hour == 20:
                                    if minute >= 60 or minute < 0:
                                        error_label = tk.Label(sorry_input, text='MM must be in between 0 and 59, '
                                                                                 'Re-Enter Time in HH:MM format',
                                                               fg="white", bg='#19221D')
                                        error_label.place(x=225, y=75, anchor='center')
                                    else:
                                        close_hour = tk.Label(sorry_input, text='Canteen is closed on Weekends',
                                                              fg="white", bg='#19221D')
                                        close_hour.place(x=225, y=75, anchor='center')
                                elif hour >= 24 or hour < 0:
                                    if minute >= 60 or minute < 0:
                                        error_label = tk.Label(sorry_input, text='HH must be in between 0 and 23 & MM '
                                                                                 'must be in between 0 and 59',
                                                               fg="white",
                                                               bg='#19221D')
                                        error_label.place(x=225, y=65, anchor='center')
                                        error_label = tk.Label(sorry_input, text='Re-Enter Time in HH:MM format',
                                                               fg="white", bg='#19221D')
                                        error_label.place(x=225, y=85, anchor='center')
                                    else:
                                        error_label = tk.Label(sorry_input, text='HH must be in between 0 and 23, '
                                                                                 'Re-Enter Time in HH:MM format',
                                                               fg="white", bg='#19221D')
                                        error_label.place(x=225, y=75, anchor='center')
                                else:
                                    if minute >= 60 or minute < 0:
                                        error_label = tk.Label(sorry_input, text='MM must be in between 0 and 59, '
                                                                                 'Re-Enter Time in HH:MM format',
                                                               fg="white", bg='#19221D')
                                        error_label.place(x=225, y=75, anchor='center')
                                    else:
                                        close_weekend = tk.Label(sorry_input, text='Canteen is closed on Weekends',
                                                                 fg="white", bg='#19221D')
                                        close_weekend.place(x=225, y=75, anchor='center')
                            except:
                                improper_label = tk.Label(sorry_input, text='Improper format, re-enter date '
                                                                            '(YYYY-MM-DD) and/or time (HH:MM)',
                                                          fg="white",
                                                          bg='#19221D').place(x=225, y=75, anchor='center')
                                improper_label.place(x=225, y=75, anchor='center')

                        elif my_day == 'Monday' or 'Tuesday' or 'Wednesday' or 'Thursday' or 'Friday':
                            if 20 < hour < 24 or 0 <= hour < 8:
                                if minute >= 60 or minute < 0:
                                    error_label = tk.Label(sorry_input, text='MM must be in between 0 and 59, '
                                                                             'Re-Enter Time in HH:MM format',
                                                           fg="white", bg='#19221D')
                                    error_label.place(x=225, y=75, anchor='center')
                                else:
                                    close_hour = tk.Label(sorry_input, text='Canteen is closed at this hour',
                                                          fg="white", bg='#19221D')
                                    close_hour.place(x=225, y=75, anchor='center')
                            elif hour == 20:
                                if 00 < minute < 60:
                                    close_hour = tk.Label(sorry_input, text='Canteen is closed at this hour',
                                                          fg="white", bg='#19221D')
                                    close_hour.place(x=225, y=75, anchor='center')
                                elif minute == 00:
                                    exit_window(window)
                                    exit_window(sorry_input)

                                    def create_menu():
                                        custom_menu2 = tk.Toplevel(self)
                                        selected_date_label = tk.Label(custom_menu2, text=(
                                                'Date Selected: ' + str(date_entry) + ', ' + str(date_input)),
                                                                       fg="white", bg='#19221D', font=('Verdana', 12))
                                        selected_date_label.pack(side=tk.TOP)
                                        time_selected_label = tk.Label(custom_menu2,
                                                                       text=('Time Selected: ' + str(time_entry)),
                                                                       fg="white", bg='#19221D', font=('Verdana', 12))
                                        time_selected_label.pack(side=tk.TOP)

                                        def shortest_queue():
                                            while True:
                                                store = ['Yong Tau Foo', 'Chicken Rice', 'Western Food', 'Mini Wok',
                                                         'Duck Rice', 'Indian']
                                                hour_input = hour
                                                prob_choice = queue_prob(hour_input)
                                                if prob_choice == 0:
                                                    break
                                                else:
                                                    shortest_queue = random.choices(store, prob_choice, k=1)
                                                    return shortest_queue
                                                    break

                                        shortest_label = tk.Label(custom_menu2,
                                                                  text=('Shortest Queue: ' + str(
                                                                      shortest_queue()).strip('[]').strip("'")),
                                                                  fg="white", bg='#19221D', font=('Verdana', 12))
                                        shortest_label.pack(side=tk.TOP)

                                        blank_label = tk.Label(custom_menu2, text='', fg="white", bg='#19221D',
                                                               font=('Verdana', 100))
                                        blank_label.pack(side=tk.TOP)

                                        if my_day == 'Monday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_mon.png")
                                        elif my_day == 'Tuesday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_tue.png")
                                        elif my_day == 'Wednesday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_wed.png")
                                        elif my_day == 'Thursday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_thu.png")
                                        else:
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_fri.png")

                                        if hour < 12:
                                            tme = 'AM'
                                        else:
                                            tme = 'PM'
                                        menu_display_final(day=str(my_day), time=str(tme))
                                        actual_sort = menu_display_final(day=str(my_day), time=str(tme))

                                        def structured_menu(frame):
                                            store_name_list = actual_sort['Store Name'].to_string(index=False)
                                            food_item_list = actual_sort['Food Item'].to_string(index=False)
                                            price_list = actual_sort['Price ($)'].to_string(index=False)
                                            label1 = tk.Label(frame, text=store_name_list, fg="white",
                                                              bg='#19221D')
                                            label1.config(font=("Verdana", 10))
                                            label1.place(x=80, y=450, anchor='center')
                                            label2 = tk.Label(frame, text=food_item_list, fg="white",
                                                              bg='#19221D')
                                            label2.config(font=("Verdana", 10))
                                            label2.place(x=230, y=450, anchor='center')
                                            label3 = tk.Label(frame, text=price_list, fg="white", bg='#19221D')
                                            label3.config(font=("Verdana", 10))
                                            label3.place(x=390, y=450, anchor='center')

                                        structured_menu(custom_menu2)

                                        custom_menu2.geometry('475x600')
                                        custom_menu2.configure(background='#19221D')
                                        custom_menu2.resizable(width=False, height=False)
                                        custom_menu2.title('Customized Menu')

                                        def specific_menu(Store):
                                            specific_window = tk.Toplevel(self)
                                            specific_window.geometry('475x600')
                                            specific_window.configure(background='#19221D')
                                            specific_window.resizable(width=False, height=False)
                                            specific_window.title('Specialized Menu')

                                            selected_date_label = tk.Label(specific_window, text=(
                                                    'Date Selected: ' + str(date_entry) + ', ' + str(date_input)),
                                                                           fg="white", bg='#19221D',
                                                                           font=('Verdana', 12))
                                            selected_date_label.pack(side=tk.TOP)
                                            time_selected_label = tk.Label(specific_window,
                                                                           text=('Time Selected: ' + str(time_entry)),
                                                                           fg="white", bg='#19221D',
                                                                           font=('Verdana', 12))
                                            time_selected_label.pack(side=tk.TOP)
                                            blank_label = tk.Label(specific_window, text='', fg="white", bg='#19221D',
                                                                   font=('Verdana', 100))
                                            blank_label.pack(side=tk.TOP)
                                            waiting_time_label = tk.Label(specific_window,
                                                                          text='Total Average Waiting Time: Enter Number '
                                                                               'of People Queuing',
                                                                          fg="white", bg='#19221D',
                                                                          font=('Verdana', 12))
                                            waiting_time_label.pack(side=tk.TOP)
                                            enter_w_time = tk.Entry(specific_window)
                                            enter_w_time.pack(side=tk.TOP)
                                            enter_w_time_button = tk.Button(specific_window, text="Calculate",
                                                                            command=lambda: calculate(self))
                                            enter_w_time_button.pack(side=tk.TOP)

                                            time_selected_label = tk.Label(specific_window,
                                                                           text='',
                                                                           fg="white", bg='#19221D',
                                                                           font=('Verdana', 12))
                                            time_selected_label.pack(side=tk.TOP)

                                            if date_input == 'Monday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_mon.png")
                                            elif date_input == 'Tuesday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_tue.png")
                                            elif date_input == 'Wednesday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_wed.png")
                                            elif date_input == 'Thursday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_thu.png")
                                            else:
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_fri.png")

                                            def calculate(self):
                                                calculate_window = tk.Toplevel(self)
                                                calculate_window.title('Waiting Time')
                                                calculate_window.configure(background='#19221D')
                                                calculate_window.after(3000, lambda: calculate_window.destroy())
                                                check_if_digit = (enter_w_time.get()).isdigit()

                                                if str(Store) == 'Japanese':
                                                    val = 2
                                                elif str(Store) == 'Chicken Rice':
                                                    val = 2
                                                elif str(Store) == 'Mini Wok':
                                                    val = 4
                                                elif str(Store) == 'Indian Cuisine':
                                                    val = 4
                                                elif str(Store) == 'Western Food':
                                                    val = 5
                                                else:
                                                    val = 3

                                                def execute():
                                                    if check_if_digit:
                                                        number_of_ppl = int(enter_w_time.get())
                                                        total_wt = number_of_ppl * val
                                                        if total_wt > 60:
                                                            total_wt_label = tk.Label(calculate_window,
                                                                                      text='Total waiting time: At least an hour',
                                                                                      fg="white", bg='#19221D')
                                                            total_wt_label.pack(side=tk.TOP)
                                                        else:
                                                            total_wt_label_ = tk.Label(calculate_window, text=(
                                                                    'Total waiting time: ' + str(
                                                                total_wt) + ' minutes'), fg="white", bg='#19221D')
                                                            total_wt_label_.pack(side=tk.TOP)
                                                    else:
                                                        error_wt_label = tk.Label(calculate_window,
                                                                                  text='Error: Enter digit(s) only',
                                                                                  fg="white", bg='#19221D')
                                                        error_wt_label.pack(side=tk.TOP)

                                                execute()

                                            def special_menu():
                                                if hour < 12:
                                                    tme = 'AM'
                                                else:
                                                    tme = 'PM'
                                                menu_display_final(store_name=str(Store),
                                                                   day=str(date_input), time=str(tme))
                                                actual_sort = menu_display_final(store_name=str(Store),
                                                                                 day=str(date_input), time=str(tme))

                                                def structured_menu(frame):
                                                    store_name_list = actual_sort['Store Name'].to_string(index=False)
                                                    food_item_list = actual_sort['Food Item'].to_string(index=False)
                                                    price_list = actual_sort['Price ($)'].to_string(index=False)
                                                    label1 = tk.Label(frame, text=store_name_list, fg="white",
                                                                      bg='#19221D')
                                                    label1.config(font=("Verdana", 15))
                                                    label1.place(x=80, y=415, anchor='center')
                                                    label2 = tk.Label(frame, text=food_item_list, fg="white",
                                                                      bg='#19221D')
                                                    label2.config(font=("Verdana", 15))
                                                    label2.place(x=230, y=415, anchor='center')
                                                    label3 = tk.Label(frame, text=price_list, fg="white", bg='#19221D')
                                                    label3.config(font=("Verdana", 15))
                                                    label3.place(x=390, y=415, anchor='center')

                                                structured_menu(specific_window)

                                                if str(Store) == 'Japanese':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/Jap_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Mini Wok':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/MW_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Western Food':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/WF_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Indian Cuisine':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/IC_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Chicken Rice':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/CR_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                else:
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/YTF_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)

                                            special_menu()

                                            picture_button(Frame=specific_window,
                                                           File="/Users/ernestang98/Desktop/Exit_Button.png", BD=0,
                                                           HT=0, Relief=tk.RAISED,
                                                           Command=lambda: specific_window.destroy(),
                                                           RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/YTF_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Yong Tau Foo'), RELX=0.06,
                                                       RELY=0.115, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/IC_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Indian Cuisine'), RELX=0.06,
                                                       RELY=0.255, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/CR_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Chicken Rice'), RELX=0.41,
                                                       RELY=0.115, RELW=0.16, RELH=0.1275)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/Jap_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Japanese'), RELX=0.41,
                                                       RELY=0.255, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/MW_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Mini Wok'), RELX=0.78,
                                                       RELY=0.115, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/WF_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Western Food'), RELX=0.78,
                                                       RELY=0.255, RELW=0.16, RELH=0.125)

                                    create_menu()

                                else:
                                    error_label = tk.Label(sorry_input, text='MM must be in between 0 and 59, '
                                                                             'Re-Enter Time in HH:MM format',
                                                           fg="white", bg='#19221D')
                                    error_label.place(x=225, y=75, anchor='center')
                            elif hour >= 24 or hour < 0:
                                if minute >= 60 or minute < 0:
                                    error_label = tk.Label(sorry_input, text='HH must be in between 0 and 23 & MM '
                                                                             'must be in between 0 and 59',
                                                           fg="white", bg='#19221D')
                                    error_label.place(x=225, y=65, anchor='center')
                                    error_label = tk.Label(sorry_input, text='Re-Enter Time in HH:MM format',
                                                           fg="white", bg='#19221D')
                                    error_label.place(x=225, y=85, anchor='center')
                                else:
                                    error_label = tk.Label(sorry_input, text='HH must be in between 0 and 23, '
                                                                             'Re-Enter Time in HH:MM format',
                                                           fg="white", bg='#19221D')
                                    error_label.place(x=225, y=75, anchor='center')
                            else:
                                if minute >= 60 or minute < 0:
                                    error_label = tk.Label(sorry_input, text='MM must be in between 0 and 59, '
                                                                             'Re-Enter Time in HH:MM format',
                                                           fg="white", bg='#19221D')
                                    error_label.place(x=225, y=75, anchor='center')
                                else:
                                    exit_window(window)
                                    exit_window(sorry_input)

                                    def create_menu():
                                        custom_menu2 = tk.Toplevel(self)
                                        selected_date_label = tk.Label(custom_menu2, text=(
                                                'Date Selected: ' + str(date_entry) + ', ' + str(date_input)),
                                                                       fg="white", bg='#19221D', font=('Verdana', 12))
                                        selected_date_label.pack(side=tk.TOP)
                                        time_selected_label = tk.Label(custom_menu2,
                                                                       text=('Time Selected: ' + str(time_entry)),
                                                                       fg="white", bg='#19221D', font=('Verdana', 12))
                                        time_selected_label.pack(side=tk.TOP)

                                        def shortest_queue():
                                            while True:
                                                store = ['Yong Tau Foo', 'Chicken Rice', 'Western Food', 'Mini Wok',
                                                         'Duck Rice', 'Indian']
                                                hour_input = hour
                                                prob_choice = queue_prob(hour_input)
                                                if prob_choice == 0:
                                                    break
                                                else:
                                                    shortest_queue = random.choices(store, prob_choice, k=1)
                                                    return shortest_queue
                                                    break

                                        shortest_label = tk.Label(custom_menu2,
                                                                  text=('Shortest Queue: ' + str(
                                                                      shortest_queue()).strip('[]').strip("'")),
                                                                  fg="white", bg='#19221D', font=('Verdana', 12))
                                        shortest_label.pack(side=tk.TOP)

                                        blank_label = tk.Label(custom_menu2, text='', fg="white", bg='#19221D',
                                                               font=('Verdana', 100))
                                        blank_label.pack(side=tk.TOP)

                                        if my_day == 'Monday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_mon.png")
                                        elif my_day == 'Tuesday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_tue.png")
                                        elif my_day == 'Wednesday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_wed.png")
                                        elif my_day == 'Thursday':
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_thu.png")
                                        else:
                                            bg_label(Frame=custom_menu2,
                                                     File="/Users/ernestang98/Desktop/bgmenu_fri.png")

                                        if hour < 12:
                                            tme = 'AM'
                                        else:
                                            tme = 'PM'
                                        menu_display_final(day=str(my_day), time=str(tme))
                                        actual_sort = menu_display_final(day=str(my_day), time=str(tme))

                                        def structured_menu(frame):
                                            store_name_list = actual_sort['Store Name'].to_string(index=False)
                                            food_item_list = actual_sort['Food Item'].to_string(index=False)
                                            price_list = actual_sort['Price ($)'].to_string(index=False)
                                            label1 = tk.Label(frame, text=store_name_list, fg="white",
                                                              bg='#19221D')
                                            label1.config(font=("Verdana", 10))
                                            label1.place(x=80, y=450, anchor='center')
                                            label2 = tk.Label(frame, text=food_item_list, fg="white",
                                                              bg='#19221D')
                                            label2.config(font=("Verdana", 10))
                                            label2.place(x=230, y=450, anchor='center')
                                            label3 = tk.Label(frame, text=price_list, fg="white", bg='#19221D')
                                            label3.config(font=("Verdana", 10))
                                            label3.place(x=390, y=450, anchor='center')

                                        structured_menu(custom_menu2)

                                        custom_menu2.geometry('475x600')
                                        custom_menu2.configure(background='#19221D')
                                        custom_menu2.resizable(width=False, height=False)
                                        custom_menu2.title('Customized Menu')

                                        def specific_menu(Store):
                                            specific_window = tk.Toplevel(self)
                                            specific_window.geometry('475x600')
                                            specific_window.configure(background='#19221D')
                                            specific_window.resizable(width=False, height=False)
                                            specific_window.title('Specialized Menu')

                                            selected_date_label = tk.Label(specific_window, text=(
                                                    'Date Selected: ' + str(date_entry) + ', ' + str(date_input)),
                                                                           fg="white", bg='#19221D',
                                                                           font=('Verdana', 12))
                                            selected_date_label.pack(side=tk.TOP)
                                            time_selected_label = tk.Label(specific_window,
                                                                           text=('Time Selected: ' + str(time_entry)),
                                                                           fg="white", bg='#19221D',
                                                                           font=('Verdana', 12))
                                            time_selected_label.pack(side=tk.TOP)
                                            blank_label = tk.Label(specific_window, text='', fg="white", bg='#19221D',
                                                                   font=('Verdana', 100))
                                            blank_label.pack(side=tk.TOP)
                                            waiting_time_label = tk.Label(specific_window,
                                                                          text='Total Average Waiting Time: Enter Number '
                                                                               'of People Queuing',
                                                                          fg="white", bg='#19221D',
                                                                          font=('Verdana', 12))
                                            waiting_time_label.pack(side=tk.TOP)
                                            enter_w_time = tk.Entry(specific_window)
                                            enter_w_time.pack(side=tk.TOP)
                                            enter_w_time_button = tk.Button(specific_window, text="Calculate",
                                                                            command=lambda: calculate(self))
                                            enter_w_time_button.pack(side=tk.TOP)

                                            time_selected_label = tk.Label(specific_window,
                                                                           text='',
                                                                           fg="white", bg='#19221D',
                                                                           font=('Verdana', 12))
                                            time_selected_label.pack(side=tk.TOP)

                                            if date_input == 'Monday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_mon.png")
                                            elif date_input == 'Tuesday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_tue.png")
                                            elif date_input == 'Wednesday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_wed.png")
                                            elif date_input == 'Thursday':
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_thu.png")
                                            else:
                                                bg_label(Frame=specific_window,
                                                         File="/Users/ernestang98/Desktop/bgmenu_fri.png")

                                            def calculate(self):
                                                calculate_window = tk.Toplevel(self)
                                                calculate_window.title('Waiting Time')
                                                calculate_window.configure(background='#19221D')
                                                calculate_window.after(3000, lambda: calculate_window.destroy())
                                                check_if_digit = (enter_w_time.get()).isdigit()

                                                if str(Store) == 'Japanese':
                                                    val = 2
                                                elif str(Store) == 'Chicken Rice':
                                                    val = 2
                                                elif str(Store) == 'Mini Wok':
                                                    val = 4
                                                elif str(Store) == 'Indian Cuisine':
                                                    val = 4
                                                elif str(Store) == 'Western Food':
                                                    val = 5
                                                else:
                                                    val = 3

                                                def execute():
                                                    if check_if_digit:
                                                        number_of_ppl = int(enter_w_time.get())
                                                        total_wt = number_of_ppl * val
                                                        if total_wt > 60:
                                                            total_wt_label = tk.Label(calculate_window,
                                                                                      text='Total waiting time: At least an hour',
                                                                                      fg="white", bg='#19221D')
                                                            total_wt_label.pack(side=tk.TOP)
                                                        else:
                                                            total_wt_label_ = tk.Label(calculate_window, text=(
                                                                    'Total waiting time: ' + str(
                                                                total_wt) + ' minutes'), fg="white", bg='#19221D')
                                                            total_wt_label_.pack(side=tk.TOP)
                                                    else:
                                                        error_wt_label = tk.Label(calculate_window,
                                                                                  text='Error: Enter digit(s) only',
                                                                                  fg="white", bg='#19221D')
                                                        error_wt_label.pack(side=tk.TOP)

                                                execute()

                                            def special_menu():
                                                if hour < 12:
                                                    tme = 'AM'
                                                else:
                                                    tme = 'PM'
                                                menu_display_final(store_name=str(Store),
                                                                   day=str(date_input), time=str(tme))
                                                actual_sort = menu_display_final(store_name=str(Store),
                                                                                 day=str(date_input), time=str(tme))

                                                def structured_menu(frame):
                                                    store_name_list = actual_sort['Store Name'].to_string(index=False)
                                                    food_item_list = actual_sort['Food Item'].to_string(index=False)
                                                    price_list = actual_sort['Price ($)'].to_string(index=False)
                                                    label1 = tk.Label(frame, text=store_name_list, fg="white",
                                                                      bg='#19221D')
                                                    label1.config(font=("Verdana", 15))
                                                    label1.place(x=80, y=415, anchor='center')
                                                    label2 = tk.Label(frame, text=food_item_list, fg="white",
                                                                      bg='#19221D')
                                                    label2.config(font=("Verdana", 15))
                                                    label2.place(x=230, y=415, anchor='center')
                                                    label3 = tk.Label(frame, text=price_list, fg="white", bg='#19221D')
                                                    label3.config(font=("Verdana", 15))
                                                    label3.place(x=390, y=415, anchor='center')

                                                structured_menu(specific_window)

                                                if str(Store) == 'Japanese':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/Jap_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Mini Wok':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/MW_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Western Food':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/WF_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Indian Cuisine':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/IC_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                elif str(Store) == 'Chicken Rice':
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/CR_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)
                                                else:
                                                    picture_button2(Frame=specific_window,
                                                                    File="/Users/ernestang98/Desktop/YTF_Symbol.png",
                                                                    BD=0, HT=0, Relief=tk.RAISED,
                                                                    RELX=0.36,
                                                                    RELY=0.08, RELW=0.275, RELH=0.22)

                                            special_menu()

                                            picture_button(Frame=specific_window,
                                                           File="/Users/ernestang98/Desktop/Exit_Button.png", BD=0,
                                                           HT=0, Relief=tk.RAISED,
                                                           Command=lambda: specific_window.destroy(),
                                                           RELX=0.36, RELY=0.9, RELW=0.28, RELH=0.09)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/YTF_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Yong Tau Foo'), RELX=0.06,
                                                       RELY=0.115, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/IC_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Indian Cuisine'), RELX=0.06,
                                                       RELY=0.255, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/CR_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Chicken Rice'), RELX=0.41,
                                                       RELY=0.115, RELW=0.16, RELH=0.1275)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/Jap_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Japanese'), RELX=0.41,
                                                       RELY=0.255, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/MW_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Mini Wok'), RELX=0.78,
                                                       RELY=0.115, RELW=0.16, RELH=0.125)

                                        picture_button(Frame=custom_menu2,
                                                       File="/Users/ernestang98/Desktop/WF_Button.png",
                                                       BD=0, HT=0, Relief=tk.RAISED,
                                                       Command=lambda: specific_menu('Western Food'), RELX=0.78,
                                                       RELY=0.255, RELW=0.16, RELH=0.125)

                                    create_menu()

                except:
                    improper_label = tk.Label(sorry_input,
                                              text='Improper format, re-enter date (YYYY-MM-DD) and/or time (HH:MM)',
                                              fg="white", bg='#19221D').place(x=225, y=75, anchor='center')
                    improper_label.pack()

        picture_button(Frame=self, File="/Users/ernestang98/Desktop/button2.png", BD=0, HT=0, Relief=tk.RAISED,
                       Command=lambda: open_window2(self), RELX=0.36, RELY=0.5, RELW=0.279, RELH=0.035)

        # View Full Menu GUIf
        def FullMenu():
            Full_Menu = tk.Toplevel(self)
            Full_Menu.geometry('700x600')
            Full_Menu.configure(background='#19221D')
            Full_Menu.resizable(width=False, height=False)
            Full_Menu.title('Full Menu')
            bg_label(Frame=Full_Menu, File='/Users/ernestang98/Desktop/fullmenubg.png')

            store_name_list = df['Store Name'].to_string(index=False)
            food_item_list = df['Food Item'].to_string(index=False)
            price_list = df['Price ($)'].to_string(index=False)
            operating_hours_list = df['Operating Hours'].to_string(index=False)
            availability_time_list = df['Availability (Time)'].to_string(index=False)
            availability_day_list = df['Availability (Day)'].to_string(index=False)

            label1 = tk.Label(Full_Menu, text=store_name_list, fg="white", bg='#2D2D2D')
            label1.config(font=("Verdana", 12))
            label1.place(x=80, y=335, anchor='center')
            label2 = tk.Label(Full_Menu, text=food_item_list, fg="white", bg='#2D2D2D')
            label2.config(font=("Verdana", 12))
            label2.place(x=320, y=335, anchor='center')
            label3 = tk.Label(Full_Menu, text=price_list, fg="white", bg='#2D2D2D')
            label3.config(font=("Verdana", 12))
            label3.place(x=440, y=335, anchor='center')
            label4 = tk.Label(Full_Menu, text=operating_hours_list, fg="white", bg='#2D2D2D')
            label4.config(font=("Verdana", 12))
            label4.place(x=200, y=335, anchor='center')
            label5 = tk.Label(Full_Menu, text=availability_time_list, fg="white", bg='#2D2D2D')
            label5.config(font=("Verdana", 12))
            label5.place(x=530, y=335, anchor='center')
            label6 = tk.Label(Full_Menu, text=availability_day_list, fg="white", bg='#2D2D2D')
            label6.config(font=("Verdana", 12))
            label6.place(x=615, y=335, anchor='center')

        picture_button(Frame=self, File="/Users/ernestang98/Desktop/button3.png", BD=0, HT=0, Relief=tk.RAISED,
                       Command=lambda: FullMenu(), RELX=0.385, RELY=0.65, RELW=0.24, RELH=0.0371)

        picture_button(Frame=self, File="/Users/ernestang98/Desktop/Previous_Button.png", BD=0, HT=0, Relief=tk.RAISED,
                       Command=lambda: controller.show_frame(WelcomePage), RELX=0.4, RELY=0.89, RELW=0.215, RELH=0.09)


app = AppMainframe()
app.geometry("800x600")
app.resizable(width=False, height=False)
app.title("Where got time?")
app.mainloop()
