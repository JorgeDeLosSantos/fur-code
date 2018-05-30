# License: MIT License
# Author: Pedro Jorge De Los Santos
# E-mail: delossantosmfq@gmail.com
import wx
import wx.grid as grid
import wx.html as html
import numpy as np
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from sympy import symbols
from sympy.matrices import Matrix


class wxTruss(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,title="IRO-MTH",size=(900,600))
        
        self.initMenu()
        self.initCtrls()
        
        self.SetBackgroundColour("#ffffff")
        self.Centre(True)
        self.Show()
        
    def initCtrls(self):
        self.mainsz = wx.BoxSizer(wx.VERTICAL)
        self.upsz = wx.BoxSizer(wx.HORIZONTAL)
        # Initial box
        self.sboxini = wx.StaticBox(self, -1, "Initial position and orientation")
        self.sboxinisz = wx.StaticBoxSizer(self.sboxini, wx.HORIZONTAL)
        # Transformation box
        self.sbox = wx.StaticBox(self, -1, "Transformation Parameters")
        self.sboxsz = wx.StaticBoxSizer(self.sbox, wx.HORIZONTAL)
        
        self.datasz = wx.BoxSizer(wx.HORIZONTAL)
        self.datainisz = wx.BoxSizer(wx.HORIZONTAL)
        
        # Creating figures, axes and canvas
        self._set_mpl()
        self.figure = Figure()
        self.axes = self.figure.add_subplot(121)
        self.axes2 = self.figure.add_subplot(122)
        self.axes2.axis('off')
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.upsz.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 2)
        #~ self.figure.set_facecolor("w")
        self.text = self.figure.text(0.5,0.5,"")
        self.text.set_fontsize(8)
        
        self.x0label = wx.StaticText(self.sboxini, -1, "x0")
        self.x0 = wx.TextCtrl(self.sboxini, -1, "0")
        self.y0label = wx.StaticText(self.sboxini, -1, "y0")
        self.y0 = wx.TextCtrl(self.sboxini, -1, "0")
        self.alpha0label = wx.StaticText(self.sboxini, -1, "alpha0")
        self.alpha0 = wx.TextCtrl(self.sboxini, -1, "0")
        #~ self.calc = wx.Button(self.sboxini, -1, "Calcular")
        
        self.dxlabel = wx.StaticText(self.sbox, -1, "Du")
        self.dx = wx.TextCtrl(self.sbox, -1, "1")
        self.dylabel = wx.StaticText(self.sbox, -1, "Dv")
        self.dy = wx.TextCtrl(self.sbox, -1, "1")
        self.rotlabel = wx.StaticText(self.sbox, -1, "Rw")
        self.rot = wx.TextCtrl(self.sbox, -1, "90")
        self.calc = wx.Button(self.sbox, -1, "Calcular")
        
        self.datainisz.Add(self.x0label, 1, wx.EXPAND|wx.ALL,5)
        self.datainisz.Add(self.x0, 6, wx.EXPAND|wx.ALL,5)
        self.datainisz.Add(self.y0label, 1, wx.EXPAND|wx.ALL,5)
        self.datainisz.Add(self.y0, 6, wx.EXPAND|wx.ALL,5)
        self.datainisz.Add(self.alpha0label, 1, wx.EXPAND|wx.ALL,5)
        self.datainisz.Add(self.alpha0, 6, wx.EXPAND|wx.ALL,5)
        #~ self.datainisz.Add(self.calc, 3, wx.EXPAND|wx.ALL,5)
        self.sboxinisz.Add(self.datainisz, 0, wx.ALL)
        
        self.datasz.Add(self.dxlabel, 1, wx.EXPAND|wx.ALL,5)
        self.datasz.Add(self.dx, 6, wx.EXPAND|wx.ALL,5)
        self.datasz.Add(self.dylabel, 1, wx.EXPAND|wx.ALL,5)
        self.datasz.Add(self.dy, 6, wx.EXPAND|wx.ALL,5)
        self.datasz.Add(self.rotlabel, 1, wx.EXPAND|wx.ALL,5)
        self.datasz.Add(self.rot, 6, wx.EXPAND|wx.ALL,5)
        self.datasz.Add(self.calc, 3, wx.EXPAND|wx.ALL,5)
        self.sboxsz.Add(self.datasz, 0, wx.ALL)
        
        self.mainsz.Add(self.sboxinisz, 1, wx.EXPAND|wx.ALL, 2)
        self.mainsz.Add(self.sboxsz, 1, wx.EXPAND|wx.ALL, 2)
        self.mainsz.Add(self.upsz, 5, wx.EXPAND)
        #~ self.mainsz.Add(self.txtout, 3, wx.EXPAND)
        self.SetSizer(self.mainsz)
        
        self.Bind(wx.EVT_BUTTON, self.calcular, self.calc)
        
    def calcular(self,event):
        self.axes.cla()
        x0 = float(self.x0.GetValue())
        y0 = float(self.y0.GetValue())
        alpha0 = float(self.alpha0.GetValue())*np.pi/180
        dx = float(self.dx.GetValue())
        dy = float(self.dy.GetValue())
        rot = float(self.rot.GetValue())*np.pi/180
        self.H0 = self.MT(x0,y0,0)*self.MR(alpha0)
        self.T = self.MT(dx,dy,0)*self.MR(rot)
        self.H = (self.H0*self.T).evalf(4,chop=True)
        self.draw_uvw(self.H0, self.axes)
        self.draw_uvw(self.H, self.axes)
        #self.axes.set_aspect("equal")
        self.axes.grid(ls="--")
        self.text.set_text("$$"+self.array2latex(self.H)+"$$")
        self.canvas.draw()
        
    def array2latex(self,M):
        out = r"H = \begin{pmatrix} "
        r,c = M.shape
        for ii in range(r):
            for jj in range(c):
                if abs(float(M[ii,jj]))<1e-10:
                    out += "{0}&".format(str(0))
                else:
                    out += "{0}&".format(str(M[ii,jj]))
                print(M[ii,jj])
            out = out[:-1]+r"\\"
        return out + r"  \end{pmatrix}"
        
    def MR(self,t,axis="z"):
        """
        Calcula la matriz de transformación homogénea correspondiente a una rotación 
        en cualesquiera de los ejes coordenados.
        """
        from sympy import sin,cos,tan,eye
        if axis in ("z","Z",3):
            M = Matrix([[cos(t),-sin(t),0,0],
                      [sin(t),cos(t),0,0],
                      [0,0,1,0],
                      [0,0,0,1]])
        elif axis in ("y","Y",2):
            M = Matrix([[cos(t),0,sin(t),0],
                      [0,1,0,0],
                      [-sin(t),0,cos(t),0],
                      [0,0,0,1]])
        elif axis in ("x","X",1):
            M = Matrix([[1,0,0,0],
                      [0,cos(t),-sin(t),0,],
                      [0,sin(t),cos(t),0],
                      [0,0,0,1]])
        else:
            return eye(4)
        return M

    def MT(self,x,y,z):
        M = Matrix([[1,0,0,x],
                      [0,1,0,y,],
                      [0,0,1,z],
                      [0,0,0,1]])
        return M
        
    def draw_uvw(self,H,ax,sz=1):
        u = H[:3,0]
        v = H[:3,1]
        w = H[:3,2]
        o = H[:3,3]
        L = sz/5
        ax.quiver(float(o[0]),float(o[1]),float(u[0]),float(u[1]),color="r")
        ax.quiver(float(o[0]),float(o[1]),float(v[0]),float(v[1]),color="g")
        
        
    def _set_mpl(self):
        matplotlib.rc('figure', facecolor="#ffffff")
        matplotlib.rc('axes', facecolor="#ffffff", linewidth=0.1, grid=True)
        matplotlib.rc('font', family="Times New Roman")
        matplotlib.rc('text', usetex=True)
        matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"
    
    def initMenu(self):
        m_file = wx.Menu()
        quit_app = m_file.Append(-1, "Quit \tCtrl+Q")
        
        m_help = wx.Menu()
        _help = m_help.Append(-1, "Help")
        about = m_help.Append(-1, "About...")
        
        menu_bar = wx.MenuBar()
        menu_bar.Append(m_file, "File")
        menu_bar.Append(m_help, "Help")
        self.SetMenuBar(menu_bar)
        
        self.Bind(wx.EVT_MENU, self.on_about, about)
        self.Bind(wx.EVT_MENU, self.on_quit, quit_app)
        
    def on_about(self,event):
        AboutDialog(None)
        
    def on_quit(self,event):
        self.Close(True)
        

class AboutDialog(wx.Frame):
    def __init__(self,parent,*args,**kwargs):
        _styles = wx.CAPTION|wx.CLOSE_BOX
        wx.Frame.__init__(self,parent=parent,title="IRO-MTH",
        size=(350,220), style=_styles)
        #~ self.SetIcon(ic.wxtruss.GetIcon())
        self.winhtml = HTMLWindow(self)
        self.winhtml.SetPage(ABOUT_HTML)
        self.Centre(True)
        self.Show()


ABOUT_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title></title>
  <link rel="stylesheet" href="">
</head>
<body bgcolor="#0A3865" link="#E5E5E5" vlink="#F0F0F0" alink="#F0F0F0">
  <center>
  <h1><font color="#FFFF00"> IRO-MTH 0.1.0 </font></h1>


  <font color="#ADD8E6">
  <b>Author:</b> Pedro Jorge De Los Santos <br>
  <b>E-mail:</b> jdelossantos@upgto.edu.mx <br>
  <b>License:</b> MIT (<a href="https://opensource.org/licenses/MIT">See license</a>) <br>
  </font>
  
  </center>
</body>
</html>
"""

class HTMLWindow(html.HtmlWindow):
    def __init__(self,parent,**kwargs):
        html.HtmlWindow.__init__(self,parent=parent,**kwargs)
    
    def OnLinkClicked(self, link):
        webbrowser.open(link.GetHref())
        


class App(wx.App):
    """
    Override OnInit
    """
    def OnInit(self):
        frame = wxTruss(None)
        return True

def run():
    """
    Entry point for wxTruss
    """
    REDIRECT = False
    LOG_FILE = "truss.log"
    app = App(REDIRECT)
    app.MainLoop()


if __name__=='__main__':
    run() # Run app
