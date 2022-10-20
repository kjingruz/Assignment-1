import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3

warning = True
connection = True


class LoginDatabase:
    def __init__(self):
        self.dbConnection = sqlite3.connect("userlogin.db")
        self.dbCursor = self.dbConnection.cursor()
        self.dbCursor.execute(
            "CREATE TABLE IF NOT EXISTS Login_table (userID PRIMARYKEY text, firstname text, lastname text, password text)")

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def Insert(self, userID, firstname, lastname, password):
        self.dbCursor.execute("INSERT INTO Login_table VALUES (?, ?, ?, ?)",
                              (userID, firstname, lastname, password))
        self.dbConnection.commit()

    def Search(self,lastname,password):
        self.dbCursor.execute("SELECT * FROM Login_table WHERE lastname = ? and password = ?",
                              (lastname,password))
        searchResults = self.dbCursor.fetchall()
        return searchResults

    def Display(self):
        self.dbCursor.execute("SELECT * FROM login_table")
        records = self.dbCursor.fetchall()
        return records

    def Check(self):
        self.dbCursor.execute("SELECT COUNT(*) FROM Login_table")
        result = self.dbCursor.fetchone()
        return result


class AAIParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("AAIparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS AAIparameter_table (UserID PRIMARYKEY text, LRL text, URL text, AtrialAmplitude text, AtrialWidth text, AtrialSensitivity text, ARP text, PVARP text, Hysteresis text, RateSmoothing text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()

    def Insert(self, userID, LRL, URL,Atrial_Amplitude, Atrial_Pulse_Width, Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing):
        self.Cursor.execute("INSERT INTO AAIparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width,Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing))
        self.connection.commit()

    def Display(self):
        self.Cursor.execute("SELECT * FROM AAIparameter_table")
        records = self.Cursor.fetchall()
        return records

    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM AAIparameter_table WHERE userID = ?", userID)
        searchResults = self.Cursor.fetchall()
        return searchResults

    def Update(self, LRL, URL,Atrial_Amplitude, Atrial_Pulse_Width, Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing, userID):
        self.Cursor.execute(
            "UPDATE patient_table SET LRL = ?, URL = ?, AtrialAmplitude = ?, Atrial_Width = ?, AtrialSensitivity = ?, ARP = ?, PVARP = ?, Hysteresis = ?, RateSmoothing = ? WHERE userID = ?",
            (LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width,Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing, userID))
        self.Connection.commit()

    def Delete(self, userID):
        self.Cursor.execute("DELETE FROM patient_table WHERE userID = ?", (userID,))
        #tkinter.messagebox.showinfo("Deleted data", "Successfully Deleted the Patient data in the database")
        self.Connection.commit()


class Values:
    def Validate(self, firstname, lastname, password, passwordreentry):
        if not (firstname.isalpha()):
            return "firstname"
        elif not (lastname.isalpha()):
            return "lastname"
        elif password != passwordreentry:
            return "password does not match"
        else:
            return "SUCCESS"


class RegisterationWindow:
    def __init__(self, userID):
        self.window = tkinter.Tk()
        self.UserID = userID
        print(self.UserID)
        self.window.wm_title("Registration")
        bg_color = "Blue"
        fg_color = "white"
        cha_color = "black"

        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.passwordreentry = tkinter.StringVar()

        # Labels
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Patient First Name",
                      font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Patient Last Name", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Password", width=25).grid(pady=5, column=1, row=4)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Password Reentry", width=25).grid(pady=5, column=1, row=5)

        self.firstnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.lastname)
        self.passwordEntry = tkinter.Entry(self.window, width=25, textvariable=self.password)
        self.passwordreEntry = tkinter.Entry(self.window, width=25, textvariable=self.passwordreentry)

        self.firstnameEntry.grid(pady=5, column=3, row=2)
        self.lastnameEntry.grid(pady=5, column=3, row=3)
        self.passwordEntry.grid(pady=5, column=3, row=4)
        self.passwordreEntry.grid(pady=5, column=3, row=5)

        # Button widgets
        tkinter.Button(self.window, width=10, fg=cha_color, bg=bg_color, font=("times new roman",10,"bold"), text="Submit", command=self.Insert).grid(pady=15, padx=5, column=1,
                                                                                       row=14)
        tkinter.Button(self.window, width=10, fg=cha_color, bg=bg_color, font=("times new roman",10,"bold"), text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=14)
        tkinter.Button(self.window, width=10, fg=cha_color, bg=bg_color, font=("times new roman",10,"bold"), text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3,
                                                                                              row=14)
        self.window.mainloop()

    def Insert(self):
        self.values = Values()
        self.database = LoginDatabase()
        self.test = self.values.Validate(self.firstnameEntry.get(), self.lastnameEntry.get(),
                                         self.passwordEntry.get(),self.passwordreEntry.get())
        if self.test == "SUCCESS":
            self.database.Insert(self.UserID, self.firstnameEntry.get(), self.lastnameEntry.get(), self.passwordEntry.get())
            tkinter.messagebox.showinfo("Inserted data", "Successfully inserted the above data in the database")
        else:
            self.valueErrorMessage = "Invalid input in field " + self.test
            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

    def Reset(self):
        self.firstnameEntry.delete(0, tkinter.END)
        self.lastnameEntry.delete(0, tkinter.END)
        self.passwordEntry.delete(0,tkinter.END)
        self.passwordreEntry.delete(0, tkinter.END)

class AAIparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("AAI Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "AtrialAmplitude", "AtrialWidth","AtrialSensitivity",
                                        "ARP", "PVARP","Hysteresis", "RateSmoothing")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("AtrialAmplitude", text="AtrialAmplitude")
        self.databaseView.heading("AtrialWidth", text="AtrialWidth")
        self.databaseView.heading("AtrialSensitivity", text="AtrialSensitivity")
        self.databaseView.heading("ARP", text="ARP")
        self.databaseView.heading("PVARP", text="PVARP")
        self.databaseView.heading("Hysteresis", text="Hysteresis")
        self.databaseView.heading("RateSmoothing", text="RateSmoothing")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("AtrialAmplitude", width=100)
        self.databaseView.column("AtrialWidth", width=100)
        self.databaseView.column("AtrialSensitivity", width=100)
        self.databaseView.column("ARP", width=100)
        self.databaseView.column("PVARP", width=100)
        self.databaseView.column("Hysteresis", width=100)
        self.databaseView.column("RateSmoothing", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()

class LoginDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("Login Database View")

        # Label widgets
        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID","firstname", "lastname","Password")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("firstname", text="First Name")
        self.databaseView.heading("lastname", text="Last Name")
        self.databaseView.heading("Password", text="Password")

        # Treeview columns
        self.databaseView.column("UserID", width=100)
        self.databaseView.column("firstname", width=100)
        self.databaseView.column("lastname", width=100)
        self.databaseView.column("Password",width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


class LoginWindow:
    def __init__(self, userID):
        self.window = tkinter.Tk()
        self.window.wm_title("Login")
        self.UserID = userID
        bg_color = "Blue"
        fg_color = "white"
        cha_color = "black"

        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.password = tkinter.StringVar()

        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="First Name",
                      font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Last Name", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Password", width=25).grid(pady=5, column=1, row=4)

        self.firstnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.lastname)
        self.passwordEntry = tkinter.Entry(self.window, width=25, textvariable=self.password)

        self.firstnameEntry.grid(pady=5, column=3, row=2)
        self.lastnameEntry.grid(pady=5, column=3, row=3)
        self.passwordEntry.grid(pady=5, column=3, row=4)

        tkinter.Button(self.window, width=10, fg=cha_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Submit", command=self.Submit).grid(pady=15, padx=5, column=1,row=14)
        self.window.mainloop()

    def Submit(self):
        self.values = Values()
        self.database = LoginDatabase()
        self.data = self.database.Search(self.lastnameEntry.get(), self.passwordEntry.get())
        if self.data:
            tkinter.messagebox.showinfo('Login success', "You are logged in!")
            self.logged_in()
        else:
            tkinter.messagebox.showerror("login fail", "Login info not correct! Please try again or register")

    def logged_in(self):
        self.logged_in_window = LoggedInWindow(self.UserID)


class LoggedInWindow:
    def __init__(self, userID):
        self.window = tkinter.Tk()
        self.window.wm_title("Welcome Page")
        self.UserID = userID
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        warning_color = "red"
        tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Welcome",
                      font=("times new roman", 20, "bold"), width=30).grid(pady=20, column=1, row=1)
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Mode",
                       font=("times new roman", 15, "bold"), command=self.Mode).grid(pady=15, column=1, row=4)
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Parameters",
                       font=("times new roman", 15, "bold"), command=self.Parameters).grid(pady=15, column=1, row=5)
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Display",
                       font=("times new roman", 15, "bold"), command=self.Display).grid(pady=15, column=1, row=6)

        if warning:
            tkinter.Label(self.window, relief=tkinter.GROOVE, fg=warning_color, bg=bg_color,
                          text="Danger! Another Pacemaker nearby!",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)

        tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Status update: Connection with DCM is " + "ON" if (connection == True)
                      else "Status update: Connection with DCM is " + "OFF",font=("times new roman", 10, "bold"),
                      width=50).grid(pady=20, column=1, row=2)

    def Mode(self):
        self.modewindow = ModeWindow()

    def Parameters(self):
        try:
            self.parameterWindow = ParametersWindow(self.modewindow,self.UserID)
        except AttributeError:
            tkinter.messagebox.showerror("Invalid Mode","Select your mode first!")

    def Display(self):
        self.database = AAIParameterDatabase()
        self.data = self.database.Display()
        self.displayWindow = AAIparametersDatabaseView(self.data)


class ParametersWindow:
    def __init__(self, modewindow, userID):
        self.currentmode = modewindow.cmode # currentmode is a variable created to record the current mode of the pacemaker
        # cmode is a variable in ModeWindow class that stores the current mode
        self.parameterwindow = tkinter.Tk()
        self.UserID = userID
        self.parameterwindow.wm_title("Current Parameters")
        self.AAI = AAIParameterDatabase()
        self.AAI_set = False
        self.VVI_set = False
        self.VOO_set = False
        self.AOO_set = False
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        print(self.currentmode)
        print(self.UserID)
        self.LRLtype = list(range(50,90))
        self.URLtype = list(range(50,175))
        self.PulseAmplitudetype = ["Off", "1.25V", "2.5V", "3.75V", "5.0V"]
        self.PulseWidthtype = [0.05]
        self.Sensitivitytype = [0.25, 0.5, 0.75]
        self.RPtype = list(range(150,500))
        self.PVARPtype = list(range(150,500))
        self.Hysteresistype = ["Off", "Same as LRL"]
        self.RateSmoothingtype = ["Off", "3%", "6%", "9%", "12%", "15%", "18%", "21%", "25%"]

        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="LRL: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="URL: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=2)
        tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Edit",
                       font=("times new roman", 15, "bold"), command=self.Edit).grid(pady=15, column=1, row=10)
        tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Save",
                       font=("times new roman", 15, "bold"), command=self.Save).grid(pady=15, column=2, row=10)
        if self.currentmode == "AAI":
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Sensitivity: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=5)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="ARP: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=6)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="PVARP: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=7)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Hysteresis: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=8)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Rate Smoothing: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=9)

            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')
            self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                       state='disabled')
            self.ARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')
            self.PVARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PVARPtype, width=20, state='disabled')
            self.HysteresisBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Hysteresistype,
                                                      width=20, state='disabled')
            self.RateSmoothingBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RateSmoothingtype, width=20,
                                                         state='disabled')

            # if self.AAI_set:
            #     self.searchresult = self.AAI.Search(self.UserID)
            #     self.LRLBox.set(self.searchresult[0])
            #     self.URLBox.set(self.searchresult[1])
            #     self.PulseAmplitudeBox.set(self.searchresult[2])
            #     self.PulseWidthBox.set(self.searchresult[3])
            #     self.SensitivityBox.set(self.searchresult[4])
            #     self.ARPBox.set(self.searchresult[5])
            #     self.PVARPBox.set(self.searchresult[6])
            #     self.HysteresisBox.set(self.searchresult[7])
            #     self.RateSmoothingBox.set(self.searchresult[8])
            # else:
            #     self.AAIdefaultSetting()
            #     self.AAI_set = True
            self.searchresult = self.AAI.Search(self.UserID)
            for result in self.searchresult:
                print(result)
            try:
                self.LRLBox.set(self.searchresult[0])
                self.URLBox.set(self.searchresult[1])
                self.PulseAmplitudeBox.set(self.searchresult[2])
                self.PulseWidthBox.set(self.searchresult[3])
                self.SensitivityBox.set(self.searchresult[4])
                self.ARPBox.set(self.searchresult[5])
                self.PVARPBox.set(self.searchresult[6])
                self.HysteresisBox.set(self.searchresult[7])
                self.RateSmoothingBox.set(self.searchresult[8])
            except IndexError:
                self.AAIdefaultSetting()

            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)
            self.SensitivityBox.grid(pady=5, column=3, row=5)
            self.ARPBox.grid(pady=5, column=3, row=6)
            self.PVARPBox.grid(pady=5, column=3, row=7)
            self.HysteresisBox.grid(pady=5, column=3, row=8)
            self.RateSmoothingBox.grid(pady=5, column=3, row=9)

        elif self.currentmode == "VVI":
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Sensitivity: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=5)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="VRP: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=6)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Hysteresis: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=7)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Rate Smoothing: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=8)

            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype,width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')
            self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                       state='disabled')
            self.VRPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')
            self.HysteresisBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Hysteresistype, width=20,
                                                      state='disabled')
            self.RateSmoothingBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RateSmoothingtype, width=20,
                                                         state='disabled')

            if self.VVI_set:
                pass
            else:
                self.VVIdefaultSetting()
                self.VVI_set = True

            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)
            self.SensitivityBox.grid(pady=5, column=3, row=5)
            self.VRPBox.grid(pady=5, column=3, row=6)
            self.HysteresisBox.grid(pady=5, column=3, row=7)
            self.RateSmoothingBox.grid(pady=5, column=3, row=8)

        elif self.currentmode == "AOO":
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype,width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')

            if self.AOO_set:
                pass
            else:
                self.AOOVOOdefaultSetting()
                self.AOO_set = True

            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)

        elif self.currentmode == "VOO":
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)

            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype,width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')
            if self.VOO_set:
                pass
            else:
                self.AOOVOOdefaultSetting()
                self.VOO_set = True

            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)

    def Save(self):
        self.counter = 0
        print(self.counter)
        self.AAIdatabase = AAIParameterDatabase()
        self.LRLBox.config(state='disabled')
        self.URLBox.config(state='disabled')
        self.PulseAmplitudeBox.config(state='disabled')
        self.PulseWidthBox.config(state='disabled')
        if self.currentmode == "AAI":
            self.ARPBox.config(state='disabled')
            self.PVARPBox.config(state='disabled')
            self.SensitivityBox.config(state='disabled')
            self.HysteresisBox.config(state='disabled')
            self.RateSmoothingBox.config(state='disabled')
            if self.counter == 0:
                self.AAIdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.ARPBox.get(),self.PVARPBox.get(),
                                        self.SensitivityBox.get(),self.HysteresisBox.get(),self.RateSmoothingBox.get())
                self.counter += 1
            else:
                self.AAIdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.ARPBox.get(),self.PVARPBox.get(),
                                        self.SensitivityBox.get(),self.HysteresisBox.get(),self.RateSmoothingBox.get(),
                                        self.UserID)
                # self.AAIdatabase.Delete(self.UserID)
                # self.AAIdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                #                         self.PulseWidthBox.get(), self.ARPBox.get(), self.PVARPBox.get(),
                #                         self.SensitivityBox.get(), self.HysteresisBox.get(),
                #                         self.RateSmoothingBox.get())
        elif self.currentmode == "VVI":
            self.VRPBox.config(state='disabled')
            self.SensitivityBox.config(state='disabled')
            self.HysteresisBox.config(state='disabled')
            self.RateSmoothingBox.config(state='disabled')
        tkinter.messagebox.showinfo("Saved", "Saved")

    def AAIdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(90)
        self.PulseAmplitudeBox.set("Off")
        self.PulseWidthBox.set(0.05)
        self.SensitivityBox.set(0.25)
        self.ARPBox.set(200)
        self.PVARPBox.set(200)
        self.HysteresisBox.set("Same as LRL")
        self.RateSmoothingBox.set("Off")

    def VVIdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(90)
        self.PulseAmplitudeBox.set("Off")
        self.PulseWidthBox.set(0.05)
        self.SensitivityBox.set(0.25)
        self.VRPBox.set(200)
        self.HysteresisBox.set("Same as LRL")
        self.RateSmoothingBox.set("Off")

    def AOOVOOdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(90)
        self.PulseAmplitudeBox.set("Off")
        self.PulseWidthBox.set(0.05)


    def Edit(self):
        self.LRLBox.config(state='active')
        self.URLBox.config(state='active')
        self.PulseAmplitudeBox.config(state='active')
        self.PulseWidthBox.config(state='active')
        self.SensitivityBox.config(state='active')
        self.ARPBox.config(state='active')
        self.PVARPBox.config(state='active')
        self.HysteresisBox.config(state='active')
        self.RateSmoothingBox.config(state='active')
        tkinter.messagebox.showinfo("Edit Mode on", "Edit Mode on")


class ModeWindow:
    def __init__(self):
        self.cmode = " "
        self.cmode = self.cMode()
        print(self.cmode)
        self.window = tkinter.Tk()
        self.window.wm_title("Pacemaker Modes")
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Current Mode: ",
                      font=("times new roman", 20, "bold"), width=30).grid(pady=20, column=1, row=1)
        self.label1 = tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text=self.cmode,
                      font=("times new roman", 20, "bold"), width=30)
        self.label1.grid(pady=20, column=2, row=1)
        self.AOObutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="AOO",
                       font=("times new roman", 15, "bold"), command=self.AOO)
        self.AOObutton.grid(pady=15, column=1, row=2)
        self.VOObutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="VOO",
                       font=("times new roman", 15, "bold"), command=self.VOO)
        self.VOObutton.grid(pady=15, column=1, row=3)
        self.AAIbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="AAI",
                       font=("times new roman", 15, "bold"), command=self.AAI)
        self.AAIbutton.grid(pady=15, column=1, row=4)
        self.VVIbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="VVI",
                       font=("times new roman", 15, "bold"), command=self.VVI)
        self.VVIbutton.grid(pady=15, column=1, row=5)

    def cMode(self):
        return self.cmode

    def AOO(self):
        self.cmode = "AOO"
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="disabled")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")

    def VOO(self):
        self.cmode = "VOO"
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="disabled")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")

    def AAI(self):
        self.cmode = "AAI"
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="disabled")
        self.VVIbutton.config(state="active")

    def VVI(self):
        self.cmode = "VVI"
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="disabled")


class HomePage:
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("Pacemaker Home Page")
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        lbl_color = 'GREEN'
        self.index = 0
        self.UserIDALL = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.userID = self.UserIDALL[self.index]
        tkinter.Label(self.homePageWindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Home Page",
                      font=("times new roman",20,"bold"), width=30).grid(pady=20, column=1, row=1)
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Register",
                       font=("times new roman",15,"bold"), command=self.Register).grid(pady=15, column=1, row=2)
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Login",
                       font=("times new roman",15,"bold"), command=self.Login).grid(pady=15, column=1, row=3)
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Display",
                       font=("times new roman",15,"bold"), command=self.Display).grid(pady=15, column=1,row=4)
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Mode",
                       font=("times new roman", 15, "bold"), command=self.Mode).grid(pady=15,column=1, row=5)
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Parameters",
                       font=("times new roman", 15, "bold"), command=self.Parameters).grid(pady=15, column=1, row=6)
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Exit",
                       font=("times new roman",15,"bold"), command=self.homePageWindow.destroy).grid(pady=15,column=1,row=7)

        self.homePageWindow.mainloop()

    def Register(self):
        self.database = LoginDatabase()
        num = self.database.Check()[0]
        if num < 10:
            self.registerWindow = RegisterationWindow(self.userID)
            self.index += 1
        else:
            tkinter.messagebox.showerror("Registeration Full", "Registeration full, please log in")

    def Display(self):
        self.database = LoginDatabase()
        self.data = self.database.Display()
        self.displayWindow = LoginDatabaseView(self.data)

    def Login(self):
        self.loginWindow = LoginWindow(self.userID)

    def Mode(self):
        self.modeWindow = ModeWindow()

    def Parameters(self):
        pass
        # try:
        #     print(1)
        #     self.parameterWindow = ParametersWindow(self.modeWindow)
        #     print(2)
        # except AttributeError:
        #     print(3)
        #     tkinter.messagebox.showerror("Invalid Mode", "Select your mode first!")
        #     print(4)
        # finally:
        #     self.parameterWindow = ParametersWindow(self.modeWindow)
        #self.parameterWindow = ParametersWindow(self.modeWindow, self.userID)

homepage = HomePage()
