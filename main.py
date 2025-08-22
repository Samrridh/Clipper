import tkinter as tk, pyperclip, time, threading, json, os 

HIST_file = "history.json"
MAX_ITEMS = 50

class ClipMgr:
    def __init__(s):
        s.root = tk.Tk(); s.root.title("Clipboard Manager")
        s.data=[]; s.pins=set(); s.sens=set()

        s.load_history()
        s.lb = tk.Listbox(s.root, width=50, height=15, relief="solid", bd=1)
        s.lb.pack(padx=5, pady=5)

        tk.Button(s.root, text="Sensitive", command=s.add_sens).pack()

        search_frame = tk.Frame(s.root)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        s.search_entry = tk.Entry(search_frame, width=30, relief="solid", bd=1)
        s.search_entry.pack(side="left")

        s.search_entry.bind("<KeyRelease>", lambda e: s.search(e.widget.get()))
        s.lb.bind("<Button-3>", s.menu)


        threading.Thread(target=s.watch, daemon=True).start()
        s.root.protocol("WM_DELETE_WINDOW", s.on_close)

        s.refresh()
        s.root.mainloop()

    
    

    def load_history(s):
        if os.path.exists(HIST_file):
            try:
                with open(HIST_file,"r") as f:
                    all_data = json.load(f)
                s.data = all_data[-MAX_ITEMS:]
            except:
                s.data = []
        else:
            s.data = []


    def save_history(s):
        with open(HIST_file,"w") as f:
            json.dump(s.data,f,indent=2)





    def watch(s):
        try:
            old = pyperclip.paste()
        except:
            old = ""
        while True:
            try:
                c=pyperclip.paste()
                if c!=old and c.strip():
                    old=c; s.add(c)
            except: pass
            time.sleep(1)


    def add(s,text):
        if text not in (t for t,_ in s.data):
            s.data.append((text,time.time()))
            s.data = s.data[-MAX_ITEMS:] 
            s.save_history()
            s.refresh()

    def add_sens(s):
        t=pyperclip.paste(); s.add(t); s.sens.add(t)
        threading.Timer(30, lambda: s.rm_by_val(t)).start()

    def rm_by_val(s,val):
        s.data = [d for d in s.data if d[0]!=val]
        s.sens.discard(val)
        s.pins.discard(val)
        s.save_history()
        s.refresh()





    def refresh(s):
        s.lb.delete(0,tk.END)
        pins = [(t,ts) for t,ts in s.data if t in s.pins]
        unpins = [(t,ts) for t,ts in s.data if t not in s.pins]



        for group in (pins[::-1], unpins[::-1]):
            for t,_ in group:
                tag=""
                if t in s.pins: tag+="(PIN) "
                if t in s.sens: tag+="(SENS) "
                s.lb.insert(tk.END, tag+t)

    def search(s,kw):
        s.lb.delete(0,tk.END)
        pins = [(t,ts) for t,ts in s.data if t in s.pins and kw.lower() in t.lower()]
        unpins = [(t,ts) for t,ts in s.data if t not in s.pins and kw.lower() in t.lower()]

        for group in (pins[::-1], unpins[::-1]):
            for t,_ in group:
                tag=""
                if t in s.pins: tag+="(PIN) "
                if t in s.sens: tag+="(SENS) "
                s.lb.insert(tk.END, tag+t)


    def menu(s,e):
        idx = s.lb.nearest(e.y)
        if idx<0: return
        real_idx = len(s.data) - 1 - idx
        val = s.data[real_idx][0]

        m = tk.Menu(s.root, tearoff=0)
        m.add_command(label="Copy", command=lambda: pyperclip.copy(val))
        if val in s.pins: 
            m.add_command(label="UNpin", command=lambda: s.pins.discard(val) or s.refresh())
        else: 
            m.add_command(label="pin", command=lambda: s.pins.add(val) or s.refresh())
        m.add_command(label="Delete", command=lambda: s.rm_by_val(val))
        m.post(e.x_root, e.y_root)

    def on_close(s):
        s.save_history()
        s.root.destroy()

ClipMgr()
