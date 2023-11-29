import customtkinter as ctk
import IO as io
import time
import threading

ctk.set_appearance_mode("light")

class Window(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.title("Cinema Kiosk System")
    self.columnconfigure(0,weight=1)
    self.rowconfigure(0,weight=1)
    self.toplevel_window = None
    self.propagate(False)

    self.frames = {}

    self.initF("loginframe", LoginFrame)

  def initF(self, name, obj,*arg):
    frame = obj(self,*arg)
    self.frames[name] = frame
    frame.grid(row=0,column=0,sticky="nsew")
    for i in self.frames:
      if i != name:
        self.frames[i].grid_forget()

class LoginFrame(ctk.CTkFrame):
  def __init__(self,master):
    super().__init__(master)

    self.columnconfigure(0,weight=1)
    self.columnconfigure(1,weight=1)

    lbl_welcome = ctk.CTkLabel(self, text="Welcome. Please login.")
    lbl_welcome.grid(column=0, row=0, columnspan=2,pady=10)
    lbl_username = ctk.CTkLabel(self, text="Username:")
    lbl_username.grid(column=0,row=1,sticky="E")
    lbl_password = ctk.CTkLabel(self, text="Password:")
    lbl_password.grid(column=0,row=2,sticky="E")
    ent_username = ctk.CTkEntry(self,placeholder_text="Username", placeholder_text_color="gray")
    ent_username.grid(column=1,row=1,padx=12,pady=10,sticky="W")
    ent_password = ctk.CTkEntry(self,placeholder_text="Password", placeholder_text_color="gray",show="*")
    ent_password.grid(column=1,row=2,padx=12,pady=10,sticky="W")
    btn_login = ctk.CTkButton(self, text="Login", cursor="hand2", command=lambda:self.verfAdmin(master,ent_username.get(), ent_password.get()))
    btn_login.grid(column=0, row=3, columnspan=2,pady=10)
    self.lbl_message = ctk.CTkLabel(self, text="")
    self.lbl_message.grid(column=0, row=4, columnspan=2,pady=10)

  def verfAdmin(self,master,u,p):
    if u == "user" and p == "bhjs":
      self.lbl_message.configure(text="login as user")
      self.changeFrame(master,"u")
    elif u == "admin" and p == "pass":
      self.lbl_message.configure(text="login as admin")
      self.changeFrame(master,"a")
    else:
      self.lbl_message.configure(text="login failed")

  def changeFrame(self,master,f):
    if f == "u":
      master.initF("userframe",UserFrame)
    elif f == "a":
      master.initF("adminframe",AdminFrame)
    self.grid_forget()

class UserFrame(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    list = io.fetchfilms()
    filmNames = []
    for i in list:
      filmNames.append([i[1],i[0]])
    fnames = self.returnDistinct([i[0] for i in filmNames])
    

    lbl_user = ctk.CTkLabel(self, text="Please select the film.")
    lbl_user.pack(side="top")
    lbox_f = ctk.CTkOptionMenu(self,
                                 values=fnames)
    lbox_f.pack(side="top",pady=5)
    btn_changeToAdmin = ctk.CTkButton(self, text="I am admin",text_color="black", width=20, height=5, fg_color="#dbdbdb", hover_color="#dbdbdb", cursor="hand2", command=lambda:self.changeToAdmin(master))
    btn_changeToAdmin.pack(side="bottom",pady=5)
    btn_user = ctk.CTkButton(self,text="Confirm",command=lambda: self.submit(master,lbox_f.get()))
    btn_user.pack(side="bottom",pady=10)

  def submit(self,master,f):
    master.initF(f+"frame", filmFrame, f)

  def changeToAdmin(self,master):
    master.toplevel_window = TopLoginPage(master)
    master.toplevel_window.focus()

  def returnDistinct(self, li):
    last = li[0]
    arr = [li[0]]
    for i in range(1,len(li)):
      if li[i] != last:
        arr.append(li[i])
        last = li[i]
    return arr

class filmFrame(ctk.CTkFrame):
  def __init__(self,master,name):
    super().__init__(master)
    self.columnconfigure((0,1,2,3), {"minsize": master.winfo_screenwidth()/4})
    self.rowconfigure([i for i in range(100)],weight=1)
    
    list = io.fetchfilms()
    houses = []
    for i in list:
      if i[1] == name:
        houses.append([i[0],i[2],i[3]])

    lbl_m = ctk.CTkLabel(self, text="Please select the timeslot.")
    lbl_m.grid(row=0,column=0,columnspan=4,pady=20)
    lbl_house = ctk.CTkLabel(self, text="House")
    lbl_house.grid(row=1,column=0,pady=20)
    lbl_date = ctk.CTkLabel(self, text="Date(YYYY/MM/DD)")
    lbl_date.grid(row=1,column=1,pady=20)
    lbl_time = ctk.CTkLabel(self, text="Time")
    lbl_time.grid(row=1,column=2,pady=20)
    lbl_houses = []
    lbl_dates = []
    lbl_times = []
    btn_confirms = []
    for i in range(len(houses)):
      lbl_houses.append(ctk.CTkLabel(self, text=houses[i][0]))
      lbl_houses[-1].grid(row=i+2, column=0,pady=10)
      d = houses[i][1][0:4]+"/"+houses[i][1][4:6]+"/"+houses[i][1][6:8]
      lbl_dates.append(ctk.CTkLabel(self, text=d))
      lbl_dates[-1].grid(row=i+2, column=1,pady=10)
      t = houses[i][2][0:2]+":"+houses[i][2][2:4]
      lbl_times.append(ctk.CTkLabel(self, text=t))
      lbl_times[-1].grid(row=i+2, column=2,pady=10)
      btn_confirms.append(ctk.CTkButton(self, text="Confirm", command=lambda:self.showseat(master,name,houses[i][0])))
      btn_confirms[-1].grid(row=i+2, column=3,pady=10)
      if io.checkseats(name,houses[i][0]) == 0:
        btn_confirms[-1].configure(state="disabled")
        btn_confirms[-1].configure(text="Sold")
    btn_changeToAdmin = ctk.CTkButton(self, text="I am admin",text_color="black", width=20, height=5, fg_color="#dbdbdb", hover_color="#dbdbdb", cursor="hand2", command=lambda:self.changeToAdmin(master))
    btn_changeToAdmin.grid(row=99,column=1,columnspan=2,sticky="s")
    btn_Back = ctk.CTkButton(self, text="Back", command=lambda:self.back(master))
    btn_Back.grid(row=99,column=0)

  def back(self,master):
    master.initF("userframe",UserFrame)

  def changeToAdmin(self,master):
    master.toplevel_window = TopLoginPage(master)
    master.toplevel_window.focus()

  def showseat(self,master,name,house):
    master.initF(master,SeatFrame,name,house)

class SeatFrame(ctk.CTkFrame):
  def __init__(self,master,name,house):
    super().__init__(master, fg_color="#dbdbdb")
    self.seat = io.fetchseats(name,house)
    self.width = len(self.seat[0])+1
    self.height = len(self.seat)+2
    self.columnconfigure(0, {"minsize": master.winfo_screenwidth() / 3})
    self.columnconfigure(1, {"minsize": master.winfo_screenwidth() / 3})
    self.columnconfigure(2, {"minsize": master.winfo_screenwidth() / 3})
    self.rowconfigure(0, {"minsize": master.winfo_screenheight() / 2})
    self.rowconfigure(1, {"minsize": master.winfo_screenheight() / 2})

    self.selected = {}
    
    self.seatFrame = ctk.CTkFrame(self,fg_color="#dbdbdb")
    filmName_lbl = ctk.CTkLabel(self.seatFrame,text="screen",font=("Arial",14))
    filmName_lbl.grid(row=0,column=0,columnspan=self.width,pady=1)
    self.seat_lbl = []
    for i in range(self.width-1):
      self.seat_lbl.append(ctk.CTkLabel(self.seatFrame,text=f"0{i+1}"[-2:],height=10,width=10))
      self.seat_lbl[-1].grid(row=1,column=i,ipadx=3,pady=1)
    for i in range(self.height-2):
      for j in range(self.width-1):
        if self.seat[i][j] == "0":
          self.seat_lbl.append(ctk.CTkLabel(self.seatFrame, text="0", fg_color="green",text_color="green",height=10,width=10))
          self.seat_lbl[-1].grid(row=i+2,column=j,padx=1,pady=1)
        elif self.seat[i][j] == "x":
          self.seat_lbl.append(ctk.CTkLabel(self.seatFrame, text="x", fg_color="red",text_color="red",height=10,width=10))
          self.seat_lbl[-1].grid(row=i+2,column=j,padx=1,pady=1)
      self.seat_lbl.append(ctk.CTkLabel(self.seatFrame, text=chr(i+65),height=10,width=5))
      self.seat_lbl[-1].grid(row=i+2,column=self.width-1,ipadx=3,pady=1)
      self.seatFrame.grid(row=0,column=1)

    self.entry_frame = ctk.CTkFrame(self,fg_color="#dbdbdb")
    message_lbl = ctk.CTkLabel(self.entry_frame,text="Please select seat")
    message_lbl.grid(row=0,column=0,columnspan=2,pady=1)
    row_lbl = ctk.CTkLabel(self.entry_frame,text="Row:",justify="right")
    row_lbl.grid(row=1,column=0,padx=2,pady=2)
    row_lbox = ctk.CTkOptionMenu(self.entry_frame,values=[chr(i+65) for i in range(self.height-2)])
    row_lbox.grid(row=1,column=1,padx=2,pady=2)
    column_lbl = ctk.CTkLabel(self.entry_frame,text="Column:",justify="right")
    column_lbl.grid(row=2,column=0,padx=2,pady=2)
    column_lbox = ctk.CTkOptionMenu(self.entry_frame,values=[str(i) for i in range(1,self.width)])
    column_lbox.grid(row=2,column=1,padx=2,pady=2)
    sub_btn = ctk.CTkButton(self.entry_frame, text="Select", command=lambda:self.seatSelect(row_lbox.get(),column_lbox.get()))
    sub_btn.bind("<Leave>", self.clear_message)
    sub_btn.grid(row=3,column=0,columnspan=2,pady=10)
    self.warn_lbl = ctk.CTkLabel(self.entry_frame,text="This seat is already taken.\nPlease choose another one.",text_color="#dbdbdb")
    self.warn_lbl.grid(row=4,column=0,columnspan=2)
    btn_changeToAdmin = ctk.CTkButton(self.entry_frame, text="I am admin",text_color="black", width=20, height=5, fg_color="#dbdbdb", hover_color="#dbdbdb", cursor="hand2", command=lambda: self.changeToAdmin(master))
    btn_changeToAdmin.grid(row=5,column=0,columnspan=2)
    self.entry_frame.grid(row=1,column=1,sticky="ns")

    self.selectionFrame = ctk.CTkFrame(self,fg_color="#dbdbdb")
    lbl_selected = ctk.CTkLabel(self.selectionFrame, text="Selected:")
    lbl_selected.pack(side="top",pady=20)
    self.lbl_selectedSeat = []
    self.btn_unselect = ctk.CTkButton(self.selectionFrame, text="Unselect", state="disabled", command=lambda: self.unselectLast(self.lbl_selectedSeat[-1].cget("text")))
    self.btn_unselect.pack(side="bottom", pady=20)
    self.selectionFrame.grid(row=0,column=0,rowspan=2,sticky="nsew")

    self.continueFrame = ctk.CTkFrame(self,fg_color="#dbdbdb")
    btn_exit = ctk.CTkButton(self.continueFrame, fg_color="#dbdbdb", hover_color="#dbdbdb",text="Back", text_color="black", command=lambda: self.exit(master))
    btn_exit.pack(side="top",pady=20)
    list = io.fetchfilms()
    price = 0
    for i in list:
      if i[1] == name and i[0] == house:
        price = i[5]
    lbl_price = ctk.CTkLabel(self.continueFrame,text=f"Price:${price}")
    lbl_price.pack(side="top",pady=200)
    self.btn_continue = ctk.CTkButton(self.continueFrame, text="Confirm", command=lambda:self.GoToPay(master,self.selected.keys(),price,name,house), state="disabled")
    self.btn_continue.pack(side="bottom",pady=20)
    self.continueFrame.grid(row=0,column=2,rowspan=2,sticky="nsew")

  def exit(self,master):
    master.initF("userframe",UserFrame)

  def seatSelect(self,r,c):
    r = ord(r) - 65
    c = int(c)
    index = self.width-2 + r*self.width + c
    if self.seat_lbl[index].cget("text") == "0":
      self.seat_lbl[index].configure(text="x", fg_color="yellow",text_color="yellow")
      tstr = chr(r+65) + str(c)
      self.selected[tstr] = index
      tempLBL = ctk.CTkLabel(self.selectionFrame, text=tstr, fg_color="blue",corner_radius=10)
      if len(self.lbl_selectedSeat) != 0:
        self.lbl_selectedSeat[-1].configure(fg_color="#dbdbdb")
      self.lbl_selectedSeat.append(tempLBL)
      self.btn_unselect.configure(state="normal")
      self.lbl_selectedSeat[-1].pack(side="top",ipadx=5,ipady=2)
      self.btn_continue.configure(state="normal")
    elif self.seat_lbl[index].cget("text") == "x":
      self.warn_lbl.configure(text_color="red")

  def unselectLast(self,last):
    index = self.selected[last]
    self.seat_lbl[index].configure(text="0", fg_color="green",text_color="green")
    self.lbl_selectedSeat[-1].pack_forget()
    self.lbl_selectedSeat.pop(-1)
    if len(self.lbl_selectedSeat) != 0:
      self.lbl_selectedSeat[-1].configure(fg_color="blue")
    else:
      self.btn_unselect.configure(state="disabled")
      self.btn_continue.configure(state="disabled")

  def clear_message(self,event):
    if self.warn_lbl.cget("text_color") == "red":
      self.warn_lbl.configure(text_color="#dbdbdb")

  def changeToAdmin(self,master):
    master.toplevel_window = TopLoginPage(master)
    master.toplevel_window.focus()

  def GoToPay(self,master,seats,price,name,house):
    master.initF(f"{name}+payframe",PayFrame,seats,price,name,house)

class PayFrame(ctk.CTkFrame):
  def __init__(self,master,seats,price,name,house):
    super().__init__(master)
    str = ""
    for i in seats:
      str += f"{i},"
    str = str[:-1]
    lbl_message = ctk.CTkLabel(self,text="Your selected seats:")
    lbl_message.pack(side="top", pady=30)
    lbl_selected = ctk.CTkLabel(self,text=f"{name}, house {house}\n{str}")
    lbl_selected.pack(side="top", pady=5)
    total = float(price)*len(seats)
    lbl_total = ctk.CTkLabel(self,text=f"Total: ${total}")
    lbl_total.pack(side="top", pady=5)
    list = io.fetchfilms()
    taken = ""
    for i in list:
      if i[1] == name and i[0] == house:
        taken = i[4]
    selected = taken+str+","
    self.btn_pay = ctk.CTkButton(self, text="Pay", command=lambda: self.payment(master,name,house,selected))
    self.btn_pay.pack(side="bottom", pady=20)
    self.pbar_pay = ctk.CTkProgressBar(self, border_color="white", fg_color="#dbdbdb",progress_color="white")
    self.pbar_pay.set(0)
    self.lbl_paying = ctk.CTkLabel(self, text="Processing transaction...")

  def payment(self,master,name,house,s):
    io.selectseat(name,house,s)
    self.pbar_pay.pack(side="bottom",pady=10)
    self.lbl_paying.pack(side="bottom")
    master.configure(mouse="none")
    for i in range(1,101):
      self.pbar_pay.set(i/100)
      master.update()
      time.sleep(0.02)
    master.toplevel_window = TopFinishPay(master)
    master.toplevel_window.focus()
    threading.Timer(3,lambda: master.toplevel_window.returnToUser(master)).start()

class TopFinishPay(ctk.CTkToplevel):
  def __init__(self, master):
    super().__init__(master)
    self.title("transaction received")
    self.resizable(False, False)
    self.geometry("400x300")
    
    frame = ctk.CTkFrame(self)
    lbl_m1 = ctk.CTkLabel(frame, text="Your payment is received.", fg_color="#dbdbdb")
    lbl_m2 = ctk.CTkLabel(frame, text="Thank you for your purchase.", fg_color="#dbdbdb")
    lbl_m1.pack(side="top", pady=5)
    lbl_m2.pack(side="top", pady=5)
    frame.pack(side="top", pady=20)

  def returnToUser(self,master):
    master.initF("userframe",UserFrame)
    self.destroy()

class TopLoginPage(ctk.CTkToplevel):
  def __init__(self, master):
    super().__init__(master)
    self.title("Login as admin")
    self.resizable(False, False)
    self.geometry("400x300")

    self.columnconfigure(0,weight=1)
    self.columnconfigure(1,weight=1)

    lbl_welcome = ctk.CTkLabel(self, text="Welcome. Please login.")
    lbl_welcome.grid(column=0, row=0, columnspan=2,pady=10)
    lbl_username = ctk.CTkLabel(self, text="Username:")
    lbl_username.grid(column=0,row=1,sticky="E")
    lbl_password = ctk.CTkLabel(self, text="Password:")
    lbl_password.grid(column=0,row=2,sticky="E")
    ent_username = ctk.CTkEntry(self,placeholder_text="Username", placeholder_text_color="gray")
    ent_username.grid(column=1,row=1,padx=12,pady=10,sticky="W")
    ent_password = ctk.CTkEntry(self,placeholder_text="Password", placeholder_text_color="gray",show="*")
    ent_password.grid(column=1,row=2,padx=12,pady=10,sticky="W")
    btn_login = ctk.CTkButton(self, text="Login", cursor="hand2", command=lambda:self.verfAdmin(master,ent_username.get(), ent_password.get()))
    btn_login.grid(column=0, row=3, columnspan=2,pady=10)
    self.lbl_message = ctk.CTkLabel(self, text="")
    self.lbl_message.grid(column=0, row=4, columnspan=2,pady=10)

  def verfAdmin(self,master,u,p):
    if u == "admin" and p == "pass":
      self.lbl_message.configure(text="login as admin")
      self.change(master,"a")
    else:
      self.lbl_message.configure(text="login failed")

  def change(self,master,f):
    master.initF("adminframe",AdminFrame)
    self.destroy()

class AdminFrame(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    lbl_admin = ctk.CTkLabel(self, text="Please select your action")
    lbl_admin.pack(side="top")
    lbox_admin = ctk.CTkOptionMenu(self, values=["create film","delete film","create house","delete house"])
    lbox_admin.pack(side="top", pady=5)
    self.curShow = "f"
    self.frame = FilmList(self)
    self.btn_admin = ctk.CTkButton(self,text="Show houses",command=lambda:self.switchDisplay())
    self.btn_admin.pack(side="top", pady=5)
    self.frame.pack(side="top", pady=5)
    btn_signOut = ctk.CTkButton(self,text="Sign out", text_color="black", width=20, height=5, fg_color="#dbdbdb", hover_color="#dbdbdb", cursor="hand2", command=lambda: self.signOut(master))
    btn_signOut.pack(side="bottom", pady = 2)
    btn_sub = ctk.CTkButton(self,text="Confirm",command=lambda: self.adminSubmit(master,lbox_admin.get()))
    btn_sub.pack(side="bottom",pady=10)

  def switchDisplay(self):
    if self.curShow == "h":
      self.curShow = "f"
      self.btn_admin.configure(text="Show houses")
      self.frame.pack_forget()
      self.frame = FilmList(self)
      self.frame.pack(side="top", pady=5)
    elif self.curShow == "f":
      self.curShow = "h"
      self.btn_admin.configure(text="Show films")
      self.frame.pack_forget()
      self.frame = HouseList(self)
      self.frame.pack(side="top", pady=5)

  def signOut(self,master):
    master.initF("loginframe",LoginFrame)

  def adminSubmit(self,master,entry):
    match entry:
      case "create film":
        master.initF("createfilmframe", CreateFilm)
      case "delete film":
        master.initF("deletefilmframe", DeleteFilm)
      case "create house":
        master.initF("createhouseframe", CreateHouse)
      case "delete house":
        master.initF("deletehouseframe", DeleteHouse)

class FilmList(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.configure(fg_color=master.cget("fg_color"))
    self.columnconfigure((0,1,2,3,4,5), weight=1)

    self.filmlist = io.fetchfilms()

    lbl_name = ctk.CTkLabel(self,text="Name",font=("Helvetica", 18, "bold"))
    lbl_house = ctk.CTkLabel(self,text="House",font=("Helvetica", 18, "bold"))
    lbl_date = ctk.CTkLabel(self,text="Date",font=("Helvetica", 18, "bold"))
    lbl_time = ctk.CTkLabel(self,text="Time",font=("Helvetica", 18, "bold"))
    lbl_price = ctk.CTkLabel(self,text="Price",font=("Helvetica", 18, "bold"))
    lbl_seat = ctk.CTkLabel(self,text="No. of available seats",font=("Helvetica", 18, "bold"))
    lbl_name.grid(row=0,column=0,padx=10,pady=10)
    lbl_house.grid(row=0,column=1,padx=10,pady=10)
    lbl_date.grid(row=0,column=2,padx=10,pady=10)
    lbl_time.grid(row=0,column=3,padx=10,pady=10)
    lbl_price.grid(row=0,column=4,padx=10,pady=10)
    lbl_seat.grid(row=0,column=5,padx=10,pady=10)
    names = []
    houses = []
    dates = []
    times = []
    prices = []
    seats = []
    r = 0
    for i in self.filmlist:
      r += 1
      names.append(ctk.CTkLabel(self, text=i[1]))
      names[-1].grid(row=r,column=0,padx=5,pady=5)
      houses.append(ctk.CTkLabel(self, text=i[0]))
      houses[-1].grid(row=r,column=1,padx=5,pady=5)
      dates.append(ctk.CTkLabel(self, text=f"{i[2][0:4]}-{i[2][4:6]}-{i[2][6:8]}"))
      dates[-1].grid(row=r,column=2,padx=5,pady=5)
      times.append(ctk.CTkLabel(self, text=f"{i[3][0:2]}:{i[3][2:4]}"))
      times[-1].grid(row=r,column=3,padx=5,pady=5)
      prices.append(ctk.CTkLabel(self, text=f"${i[5]}"))
      prices[-1].grid(row=r,column=4,padx=5,pady=5)
      seats.append(ctk.CTkLabel(self, text=io.checkseats(i[1],i[0])))
      seats[-1].grid(row=r,column=5,padx=5,pady=5)

class HouseList(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.configure(fg_color=master.cget("fg_color"))
    self.columnconfigure((0,1,2), weight=1)

    self.houseslist = io.fetchhouses()

    lbl_no = ctk.CTkLabel(self,text="House no.",font=("Helvetica", 18, "bold"))
    lbl_row = ctk.CTkLabel(self,text="Row",font=("Helvetica", 18, "bold"))
    lbl_col = ctk.CTkLabel(self,text="Column",font=("Helvetica", 18, "bold"))
    lbl_no.grid(row=0,column=0,padx=10,pady=10)
    lbl_row.grid(row=0,column=1,padx=10,pady=10)
    lbl_col.grid(row=0,column=2,padx=10,pady=10)
    nos = []
    rows = []
    cols = []
    r = 0
    for i in self.houseslist:
      r += 1
      nos.append(ctk.CTkLabel(self, text=i[0]))
      nos[-1].grid(row=r,column=0,padx=5,pady=5)
      rows.append(ctk.CTkLabel(self, text=i[1]))
      rows[-1].grid(row=r,column=1,padx=5,pady=5)
      cols.append(ctk.CTkLabel(self, text=i[2]))
      cols[-1].grid(row=r,column=2,padx=5,pady=5)

class CreateFilm(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.columnconfigure(0, {"minsize": master.winfo_screenwidth() / 2})
    self.columnconfigure(1, {"minsize": master.winfo_screenwidth() / 2})

    self.houses = []
    for i in io.fetchhouses():
      self.houses.append(str(i[0]))

    self.lbl_message = ctk.CTkLabel(self,text="Create film", font=("Arial", 24))
    self.lbl_message.grid(row=0,column=0,columnspan=2,pady=20)
    self.lbl_name = ctk.CTkLabel(self,text="Name:")
    self.lbl_name.grid(row=1,column=0,pady=5)
    self.lbl_price = ctk.CTkLabel(self,text="Price(xx.xx):")
    self.lbl_price.grid(row=2,column=0,pady=5)
    self.lbl_date = ctk.CTkLabel(self,text="Date(YYYYMMDD):")
    self.lbl_date.grid(row=3,column=0,pady=5)
    self.lbl_time = ctk.CTkLabel(self,text="Time(24h,HHMM):")
    self.lbl_time.grid(row=4,column=0,pady=5)
    self.lbl_house = ctk.CTkLabel(self,text="House No.:")
    self.lbl_house.grid(row=5,column=0,pady=5)
    self.ent_name = ctk.CTkEntry(self,placeholder_text="Name of the film", placeholder_text_color="gray")
    self.ent_name.grid(row=1,column=1,pady=5)
    self.ent_price = ctk.CTkEntry(self,placeholder_text="Price", placeholder_text_color="gray")
    self.ent_price.grid(row=2,column=1,pady=5)
    self.ent_date = ctk.CTkEntry(self,placeholder_text="Date", placeholder_text_color="gray")
    self.ent_date.grid(row=3,column=1,pady=5)
    self.ent_time = ctk.CTkEntry(self,placeholder_text="Time", placeholder_text_color="gray")
    self.ent_time.grid(row=4,column=1,pady=5)
    self.lbox_house = ctk.CTkOptionMenu(self, values=self.houses)
    self.lbox_house.grid(row=5,column=1,pady=5)
    self.btn_submit = ctk.CTkButton(self,text="Confirm",command=lambda:self.create(master,[self.ent_name.get(),float(self.ent_price.get()),self.lbox_house.get(),self.ent_date.get(),self.ent_time.get()]))
    self.btn_submit.grid(row=9,column=0,columnspan=2,pady=5)
    self.btn_signOut = ctk.CTkButton(self, text="Sign out",text_color="black", width=20, height=5, fg_color="#dbdbdb", hover_color="#dbdbdb", cursor="hand2", command=lambda: self.signOut(master))
    self.btn_signOut.grid(row=10,column=0,columnspan=2,pady=5)

  def create(self,master,info):
    self.btn_submit.configure(state="disabled")
    self.btn_signOut.configure(state="disabled")
    self.showInfo(master,info)
    io.newfilm(info[0],info[2],info[3],info[4],info[1])

  def signOut(self,master):
    master.initF("loginframe",LoginFrame)

  def showInfo(self,master,info):
    self.frame = ctk.CTkFrame(self,fg_color=self.cget("fg_color"))
    lbl_info = ctk.CTkLabel(self.frame, text=f"name: {info[0]}\nprice: ${info[1]}\nhouse: {info[2]}\ndate: {info[3][0:4]}-{info[3][4:6]}-{info[3][6:8]}\ntime: {info[4][0:2]}:{info[4][2:4]}")
    lbl_info.pack(side="top", pady=20)
    btn_confirm = ctk.CTkButton(self.frame, text="Return",command=lambda:self.Return(master))
    btn_confirm.pack(side="top", pady=20)
    self.frame.grid(row=11,column=0,columnspan=2)

  def Return(self,master):
    master.initF("adminframe",AdminFrame)

class DeleteFilm(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.columnconfigure([0,1,2,3,4,5,6], weight=1)

    self.filmlist = io.fetchfilms()

    lbl_name = ctk.CTkLabel(self,text="Name",font=("Helvetica", 18, "bold"))
    lbl_house = ctk.CTkLabel(self,text="House",font=("Helvetica", 18, "bold"))
    lbl_date = ctk.CTkLabel(self,text="Date",font=("Helvetica", 18, "bold"))
    lbl_time = ctk.CTkLabel(self,text="Time",font=("Helvetica", 18, "bold"))
    lbl_price = ctk.CTkLabel(self,text="Price",font=("Helvetica", 18, "bold"))
    lbl_seat = ctk.CTkLabel(self,text="No. of available seats",font=("Helvetica", 18, "bold"))
    lbl_name.grid(row=0,column=0,padx=10,pady=20)
    lbl_house.grid(row=0,column=1,padx=10,pady=20)
    lbl_date.grid(row=0,column=2,padx=10,pady=20)
    lbl_time.grid(row=0,column=3,padx=10,pady=20)
    lbl_price.grid(row=0,column=4,padx=10,pady=20)
    lbl_seat.grid(row=0,column=5,padx=10,pady=20)
    names = []
    houses = []
    dates = []
    times = []
    prices = []
    seats = []
    self.buttons = []
    r = 0
    n = ""
    h = 0
    for i in self.filmlist:
      r += 1
      n = i[1]
      h = i[0]
      names.append(ctk.CTkLabel(self, text=i[1]))
      names[-1].grid(row=r,column=0,padx=5,pady=5)
      houses.append(ctk.CTkLabel(self, text=i[0]))
      houses[-1].grid(row=r,column=1,padx=5,pady=5)
      dates.append(ctk.CTkLabel(self, text=f"{i[2][0:4]}-{i[2][4:6]}-{i[2][6:8]}"))
      dates[-1].grid(row=r,column=2,padx=5,pady=5)
      times.append(ctk.CTkLabel(self, text=f"{i[3][0:2]}:{i[3][2:4]}"))
      times[-1].grid(row=r,column=3,padx=5,pady=5)
      prices.append(ctk.CTkLabel(self, text=f"${i[5]}"))
      prices[-1].grid(row=r,column=4,padx=5,pady=5)
      seats.append(ctk.CTkLabel(self, text=io.checkseats(i[1],i[0])))
      seats[-1].grid(row=r,column=5,padx=5,pady=5)
      self.buttons.append(ctk.CTkButton(self,text="Delete",command=self.buttonComm(self.delete,master,n,h)))
      self.buttons[-1].grid(row=r,column=6,padx=5,pady=5)
      
  def buttonComm(self, func, *arg):
      return lambda:func(*arg)

  def delete(self,master,name,house):
    for i in self.buttons:
      i.configure(state="disabled")
    master.toplevel_window = TopDeleteFilm(master,name,house)
    master.toplevel_window.focus()
    io.deletefilm(name,house)

class TopDeleteFilm(ctk.CTkToplevel):
  def __init__(self,master,name,house):
    super().__init__(master)
    self.title("Film deleted")
    self.resizable(False, False)
    self.geometry("400x300")

    lbl1 = ctk.CTkLabel(self,text="Film deleted:")
    lbl2 = ctk.CTkLabel(self,text=f"{name}, house {house}")
    btn = ctk.CTkButton(self,text="Return",command=lambda:self.Return(master))
    lbl1.pack(side="top",pady=10)
    lbl2.pack(side="top",pady=10)
    btn.pack(side="top",pady=20)

  def Return(self,master):
    master.initF("adminframe", AdminFrame)
    self.destroy()

class CreateHouse(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.columnconfigure(0, {"minsize": master.winfo_screenwidth() / 2})
    self.columnconfigure(1, {"minsize": master.winfo_screenwidth() / 2})

    self.house = io.fetchhouses()
    self.house_no = self.house[-1][0] + 1
    smallest = self.house_no
    for index,t in enumerate(self.house):
      print(index,t)
      if index+1 != t[0]:
        if index+1 < smallest:
          smallest = index+1
    self.house_no = smallest

    self.lbl_message = ctk.CTkLabel(self,text="Create house", font=("Arial", 24))
    self.lbl_message.grid(row=0,column=0,columnspan=2,pady=20)
    self.lbl_name = ctk.CTkLabel(self,text=f"House no.: {self.house_no}")
    self.lbl_name.grid(row=1,column=0,columnspan=2,pady=5)
    self.lbl_row = ctk.CTkLabel(self,text="Row:")
    self.lbl_row.grid(row=2,column=0,pady=5)
    self.lbl_col = ctk.CTkLabel(self,text="Column:")
    self.lbl_col.grid(row=3,column=0,pady=5)
    f_row = ctk.CTkFrame(self,fg_color=self.cget("fg_color"))
    lblr = ctk.CTkLabel(f_row,text="10")
    lblr.pack(side="right",ipadx=10)
    sliderr = ctk.CTkSlider(f_row,number_of_steps=19,from_=1,to=20,command=lambda v:self.dynamicChangeSlider(v, lblr))
    sliderr.pack(side="left")
    f_row.grid(row=2,column=1,pady=5)
    f_col = ctk.CTkFrame(self,fg_color=self.cget("fg_color"))
    lblc = ctk.CTkLabel(f_col,text="10")
    lblc.pack(side="right",ipadx=10)
    sliderc = ctk.CTkSlider(f_col,number_of_steps=19,from_=1,to=20,command=lambda v:self.dynamicChangeSlider(v, lblc))
    sliderc.pack(side="left")
    f_col.grid(row=3,column=1,pady=5)
    self.btn_submit = ctk.CTkButton(self,text="Confirm",command=lambda:self.create(master,[self.house_no, lblr.cget("text"), lblc.cget("text")]))
    self.btn_submit.grid(row=9,column=0,columnspan=2,pady=5)
    self.btn_signOut = ctk.CTkButton(self, text="Sign out", text_color="black", width=20, height=5, fg_color="#dbdbdb", hover_color="#dbdbdb", cursor="hand2", command=lambda: self.signOut(master))
    self.btn_signOut.grid(row=10,column=0,columnspan=2,pady=5)

  def dynamicChangeSlider(self, value, lbl):
    lbl.configure(text=int(value))

  def create(self,master,info):
    self.btn_submit.configure(state="disabled")
    self.btn_signOut.configure(state="disabled")
    self.showInfo(master,info)
    io.newhouse(info[0],int(info[1]),int(info[2]))

  def signOut(self,master):
    master.initF("loginframe",LoginFrame)

  def showInfo(self,master,info):
    self.frame = ctk.CTkFrame(self,fg_color=self.cget("fg_color"))
    lbl_info = ctk.CTkLabel(self.frame, text=f"house no.: {info[0]}\nno. of rows: {info[1]}\nno. of columns:{info[2]}")
    lbl_info.pack(side="top", pady=20)
    btn_confirm = ctk.CTkButton(self.frame, text="Return",command=lambda:self.Return(master))
    btn_confirm.pack(side="top", pady=20)
    self.frame.grid(row=11,column=0,columnspan=2)

  def Return(self,master):
    master.initF("adminframe",AdminFrame)

class DeleteHouse(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.columnconfigure([0,1,2,3], weight=1)

    self.houselist = io.fetchhouses()

    lbl_no = ctk.CTkLabel(self,text="House no.",font=("Helvetica", 18, "bold"))
    lbl_row = ctk.CTkLabel(self,text="Rows",font=("Helvetica", 18, "bold"))
    lbl_col = ctk.CTkLabel(self,text="Columns",font=("Helvetica", 18, "bold"))
    lbl_no.grid(row=0,column=0,padx=10,pady=20)
    lbl_row.grid(row=0,column=1,padx=10,pady=20)
    lbl_col.grid(row=0,column=2,padx=10,pady=20)
    nos = []
    rows = []
    cols = []
    self.buttons = []
    r = 0
    no = 0
    for i in self.houselist:
      r += 1
      no = i[0]
      nos.append(ctk.CTkLabel(self, text=i[0]))
      nos[-1].grid(row=r,column=0,padx=5,pady=5)
      rows.append(ctk.CTkLabel(self, text=i[1]))
      rows[-1].grid(row=r,column=1,padx=5,pady=5)
      cols.append(ctk.CTkLabel(self, text=i[2]))
      cols[-1].grid(row=r,column=2,padx=5,pady=5)
      self.buttons.append(ctk.CTkButton(self,text="Delete",command=self.returnLambda(self.warning,master,no)))
      self.buttons[-1].grid(row=r,column=3,padx=5,pady=5)

  def returnLambda(self,func,*arg):
    return lambda:func(*arg)

  def warning(self,master,no):
    print(no)
    for i in self.buttons:
      i.configure(state="disabled")
    master.toplevel_window = TopDeleteHouse(master,no)
    master.toplevel_window.focus()

class TopDeleteHouse(ctk.CTkToplevel):
  def __init__(self,master,house):
    super().__init__(master)
    self.title("Warning")
    self.resizable(False, False)
    self.geometry("400x300")

    self.frame1 = ctk.CTkFrame(self,fg_color=self.cget("fg_color"))
    lbl1 = ctk.CTkLabel(self.frame1,text=f"Confirm delete: house {house}\nThis will also delete all films in house {house}")
    btn1 = ctk.CTkButton(self.frame1,text="Confirm",command=lambda:self.confirm(master,house))
    lbl1.pack(side="top",pady=10)
    btn1.pack(side="top",pady=20)
    self.frame1.pack(side="top")

    self.frame2 = ctk.CTkFrame(self,fg_color=self.cget("fg_color"))
    lbl2 = ctk.CTkLabel(self.frame2,text=f"House deleted: house {house}")
    btn2 = ctk.CTkButton(self.frame2,text="Return",command=lambda:self.Return(master))
    lbl2.pack(side="top",pady=10)
    btn2.pack(side="top",pady=20)

  def confirm(self,master,house):
    io.deletehouse(house)
    self.frame1.pack_forget()
    self.frame2.pack(side="top")

  def Return(self,master):
    master.initF("adminframe", AdminFrame)
    self.destroy()


if __name__ == "__main__":
  w = Window()
  w.geometry(f"{w.winfo_screenwidth()}x{w.winfo_screenheight()}+-10+-10")
  w.mainloop()
