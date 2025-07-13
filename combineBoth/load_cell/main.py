import threading
import signal
import tkinter as tk
from tkinter import messagebox
import scipy.io as sio

from load_cell_reader import LoadCellReader

def main(time_duration):
    port = 'COM27'
    DURATION = int(time_duration)

    root = tk.Tk()
    root.title("Load Cell + Countdown")
    root.geometry("360x160")

    weight_var = tk.StringVar(value="Waiting for dta...")
    lbl_weight = tk.Label(root, textvariable=weight_var, font=("Arial", 24))
    lbl_weight.pack(pady=(10,0), fill='x')

    reader = LoadCellReader(weight_var, port)

    def sigint_handler(signum, frame):
        print("\n[Received Ctrl+C, shutting down]")
        reader.running = False
        root.quit()

    signal.signal(signal.SIGINT, sigint_handler)

    def save_data_in_matlab_format():
        mat_data = list(reader.storage)
        dirPath = "../data/testing data"
        file_name = 'load_cell.mat'
        file_path = f"{dirPath}/{file_name}"
        sio.savemat(file_path, {'value': mat_data})
        print("[Load Cell Data saved]")

    def countdown(count, timer_var):
        if count >= 0:
            timer_var.set(f"{count} s")
            root.after(1000, countdown, count-1, timer_var)
        else:
            timer_var.set("Done")

    t = threading.Thread(target=reader.record, args=(DURATION,), daemon=True)
    t.start()

    root.after(int((DURATION + 0.5) * 1000), save_data_in_matlab_format)

    # （可选）也保留一个手动保存按钮
    btn = tk.Button(root, text="手动保存 (.mat)", command=save_data_in_matlab_format)
    btn.pack(pady=(20, 0))

    timer_var = tk.StringVar(value="10 s")
    lbl_timer = tk.Label(root, textvariable=timer_var, font=("Arial", 18), fg="blue")
    lbl_timer.pack(pady=(5,10))

    root.after(100, lambda: countdown(10, timer_var))

    root.mainloop()

if __name__ == "__main__":
    main(time_duration=10)
