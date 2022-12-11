import tkinter.ttk,socket
from tkinter import Button,Entry,Spinbox,WORD,W,E,Label,Tk,END,messagebox,Text
'''
License:
 This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
GUI PortScanner By: T31337
Please Note, This Porgram Claims To Be "Not Responding" During Scan,However If You Wait,
It Should Complete And Start Responding Again!
'''
class PortScanner:
	def __init__(self):
		mGUI = Tk() #create tk reference object AKA Make A Window/Frame
		self.srvr = Entry(mGUI,textvariable="server")
		self.srvr.setvar(name="server",value='127.0.0.1')
		self.srvr.grid(row=0,column=1,sticky=W)
		lbl = Label(mGUI,text="Target Address:")
		lbl.grid(row=0,column=0,sticky=W)
		self.spnr = Spinbox(mGUI,from_=1,to=49152,value=1)
		self.spnr.grid(row=1,column=1,sticky=W)
		lbl2 = Label(mGUI,text="Starting Port:")
		lbl2.grid(row=1,column=0,sticky=W)
		self.spnr.grid(row=1,column=1,sticky=W)
		self.spnr2 = Spinbox(mGUI,from_=1,to=49152,value=49152)
		self.spnr2.grid(row=2,column=1,sticky=W)
		lbl3 = Label(mGUI,text="Ending Port")
		lbl3.grid(row=2,column=0,sticky=W)
		mGUI.resizable(width=False,height=False) #Make Window Size Static (Not Resizeable)
		btn = Button(mGUI,text="Commence Port Scan!",command=self.scan)
		btn.grid(row=3,column=1,sticky=W)
		self.txt = Text(mGUI,width=50,height=20,wrap=WORD)
		self.txt.grid(row=4,column=0,columnspan=2,sticky=W)
		mGUI.title('PyPortScanner!') #set Title Of Window
		self.txt.insert(0.0,'Open Ports Will Appear Here After Scan Completes!\n\nPyScanner By: T31337\n\nNot For Illegal Usage!')
		
		mGUI.mainloop() #Show GUI Window


	def pscan(self,port):
		try:
			target = self.srvr.get()
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((target,port))
			return True
		except:
			return False

	def scan(self):
		self.txt.delete(0.0,END)
		print('Scanning',self.srvr.get())
		for x in range(int(self.spnr.get()),int(self.spnr2.get())+1):
			if self.pscan(x):
				print('Port: ',x,'Is Open!')
				msg = "Port "+str(x)+" Is Open!\n"
				self.txt.insert(0.0,msg)
			else:
				print('port: ',x,'Is Closed!')
				#msg = "Port "+str(x)+" Is Closed!\n"
				#txt.insert(0.0,msg)


		messagebox.showinfo(title="PyPortScanner!",message="Scan Completed!")

ps = PortScanner()  