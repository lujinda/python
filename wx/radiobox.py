import wx
class RadioBoxFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,"radio box example",pos=(100,100),size=(350,200))
		panel=wx.Panel(self,-1)
		sampleList=['zero','one','two']
		wx.RadioBox(panel,-1,"A radio Box",(10,10),wx.DefaultSize,sampleList,2,wx.RA_SPECIFY_COLS)
		wx.RadioBox(panel,-1,"",(150,10),wx.DefaultSize,sampleList,3,wx.NO_BORDER)
if __name__ == '__main__':
	app=wx.App()
	RadioBoxFrame().Show()
	app.MainLoop()

