from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import csv
import datetime

nowtime = datetime.datetime.now()
millisecond, second, minute, hour, second2, minute2, hour2  = 0, 0, 0, 0, 0, 0, 0
lissec, lismin, lishour = [0], [0], [0]
running_split = False
running = False

def start():
    global running
    print('start timer')
    if not running:
        update()
        running = True

def pause():
    global running
    print('pause timer')
    if running:
        stopwatch_label.after_cancel(update_time)
        running = False

def reset():
    global running
    print('reset timer')
    if running:
        stopwatch_label.after_cancel(update_time)
        running = False
    global millisecond, second, minute, hour
    millisecond, second, minute, hour = 0, 0, 0, 0
    stopwatch_label.config(text='00:00:00')

def update():
    global millisecond, second, minute, hour, second2, minute2, hour2, running_split
    second += 1
    if second == 60:
        minute += 1
        second = 0
    if minute == 60:
        hour += 1
        minute = 0

    global hour_str, minute_str, second_str
    hour_str = f'{hour}' if hour > 9 else f'0{hour}'
    minute_str = f'{minute}' if minute > 9 else f'0{minute}'
    second_str = f'{second}' if second > 9 else f'0{second}'

    stopwatch_label.config(text=f'{hour_str}:{minute_str}:{second_str}')
    global update_time, time_label
    time_label = (f'{hour_str}:{minute_str}:{second_str}')
    update_time = stopwatch_label.after(1000, update)

def save():
    global files
    print('save timer successed')
    files = filedialog.asksaveasfilename(
        defaultextension='.csv',
        filetypes=[
            ('csv File','.csv'),
            ('text File','.txt'),
            ('All File','.*')
        ]
    )
    with open(files, "w", newline='') as nf:
        newf = csv.writer(nf)
        newf.writerow(['MM/DD/YYYY:Time','Time StopWatch','Split'])
    cutname = files.split('/', -1)[-1]
    filename_label.config(text=f'file name : {cutname}')

def split():
    global running_split
    running_split = True
    if running_split:
        lissec.append(second)
        lismin.append(minute)
        lishour.append(hour)
        second2 = lissec[-1] - lissec[-2]
        minute2 = lismin[-1] - lismin[-2]
        hour2 = lishour[-1] - lishour[-2]
        running_split = False
    global hour_str2, minute_str2, second_str2
    hour_str2 = f'{hour2}' if hour2 > 9 else f'0{hour2}'
    minute_str2 = f'{minute2}' if minute2 > 9 else f'0{minute2}'
    second_str2 = f'{second2}' if second2 > 9 else f'0{second2}'
    split_label = (f'{hour_str2}:{minute_str2}:{second_str2}')
    print(split_label)
    if hour2 < 0 or minute2 < 0 or second2 < 0:
        print('split < 0 unsave')
    else:
        with open(files, "a", newline='') as f:
            writef = csv.writer(f)
            writef.writerow([nowtime.strftime('%x%X'),time_label,split_label])

gui = Tk()
gui.geometry('280x150')
gui.title('Stop Watch')

filename_label = Label(gui, text='โปรดเลือกไลฟ์/เซฟไฟล์ก่อน', font=('prompt',15))
filename_label.pack()

stopwatch_label = Label(gui, text='00:00:00', font=('Arial',20))
stopwatch_label.pack()

save_bt = Button(gui, text=' Save ', font=('prompt',10), command=save)
save_bt.pack(ipadx=1)
start_bt = Button(gui, text='Start', font=('prompt',10), command=start)
start_bt.pack(side=LEFT, ipadx=5)
pause_bt = Button(gui, text='Pause ', font=('prompt',10), command=pause)
pause_bt.pack(side=LEFT, ipadx=5)
split_bt = Button(gui, text='Split', font=('prompt',10), command=split)
split_bt.pack(side=LEFT, ipadx=8)
reset_bt = Button(gui, text='Reset', font=('prompt',10), command=reset)
reset_bt.pack(side=LEFT, ipadx=7)
quit_bt = Button(gui, text=' Kill ', font=('prompt',10), command=gui.quit)
quit_bt.pack(side=LEFT, ipadx=7)


gui.mainloop()