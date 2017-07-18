import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, IntSlider, widget, FloatText, FloatSlider, fixed





########################################
#           WIDGETS
########################################


def PrimaryWidget():

    i = interact(GPRWidget_zero_offset,
            logsig = IntSlider( min=-5, max=-3, value=-4, step=1 ),
            epsr = IntSlider( min=1, max=16, value=1, step=3 ),
            fc = FloatSlider( min=2e7, max=1e8, value=4e7, step=2e7 ),
            x1 = IntSlider( min=-30, max=30, value=-10, step=1 ),
            x2 = IntSlider( min=-30, max=30, value=10, step=1 ),
            d1 = IntSlider( min=5, max=40, value=10, step=1 ),
            d2 = IntSlider( min=5, max=40, value=10, step=1 ),
            R1 = FloatSlider( min=-0.5, max=10, value=1, step=0.5 ),
            R2 = FloatSlider( min=-0.5, max=10, value=1, step=0.5 )

    return i




########################################
#           FUNCTIONS
########################################


def GPRWidget_zero_offset(epsr,logsig,fc,x1,d1,x2,d2,R1,R2):

	# Compute Time and Offset Range
	v = fcnComputeVelocity(epsr,logsig,fc)
	a = fcnComputeAlpha(epsr,logsig,fc)

	xmin,xmax,nx = -30, 30, 31
	xrx = np.reshape(np.linspace(xmin,xmax,nx),(1,nx))
	
	tmax = (4/a)/v
	nt = 501
	t = np.reshape(np.linspace(0,tmax,nt),(nt,1))

	p = np.ones((1,nx))
	q = np.ones((nt,1))

	T = np.kron(t,p)
	XRX = np.kron(q,xrx)
	Attn = np.exp(-a*v*T)

	# Create Radargram Data
	dx = (xmax-xmin)/(nx-1)

	for ii in range(0,2):
	    
	    tii = fcnComputePointTravelTime(xp[ii],dp[ii],R[ii],epsr,logsig,fc,xrx)
	    Aii = (0.6*dx*(Attn*fcnGetRicker(fc,T-np.kron(tii,q)) + 0.01*np.random.normal(0,1,(nt,nx)))/Attn)
	    XRX = XRX + Aii

	# Plotting
	FS = 18
	dlim = 50

	fig1 = plt.figure(figsize=(14,6))

	Ax1 = fig1.add_axes([0.03,0,0.44,1])
	ptArray = np.array([[xmin,0],[xmax,0.],[xmax,dlim],[xmin,dlim]])
	poly1 = plt.Polygon(ptArray,closed=True,facecolor=((0.7,0.7,0.5)),edgecolor=((0.2,0.2,0.2)),lw=2.5)
	Ax1.add_patch(poly1)
	ptArray = np.array([[xmin,0],[xmax,0.],[xmax,-0.2*dlim],[xmin,-0.2*dlim]])
	poly2 = plt.Polygon(ptArray,closed=True,facecolor=((0.8,1,1)),edgecolor=((0.2,0.2,0.2)),lw=2.5)
	Ax1.add_patch(poly2)

	phi = np.linspace(0,2*np.pi,31)

	for ii in range(0,2):
	    xs = xp[ii] + R[ii]*np.cos(phi)
	    ds = dp[ii] + R[ii]*np.sin(phi)
	    polyTemp = plt.Polygon(np.c_[xs,ds],closed=True,facecolor=((0.5,0.5,0.5)),edgecolor=((0.2,0.2,0.2)),lw=2.5)
	    Ax1.add_patch(polyTemp)

	Ax1.set_xlim(xmin,xmax)
	Ax1.set_ylim(dlim,-0.2*dlim)
	plt.xticks(fontsize=FS)
	plt.yticks(fontsize=FS)
	plt.xlabel('X [m]',fontsize=FS+4)
	plt.ylabel('Depth [m]',fontsize=FS+4)

	Ax2 = fig1.add_axes([0.56,0,0.44,1])
	Ax2.plot(XRX,1e9*T,'k')
	Ax2.set_xlim(xmin-dx,xmax+dx)
	Ax2.set_ylim(1e9*np.max(t),0)
	plt.xticks(fontsize=FS)
	plt.yticks(fontsize=FS)
	plt.xlabel('X [m]',fontsize=FS+4)
	plt.ylabel('t [ns]',fontsize=FS+4)

	plt.show(fig1)



def fcnGetRicker(fc,t):
    """Compute Ricker wavelet for central operating frequency fc"""
    
    A = (1 - 2*(np.pi*fc*t)**2)*np.exp(-(np.pi*fc*t)**2)
    
    return A

def fcnComputePointTravelTime(xp,dp,R,epsr,logsig,fc,xrx):
    """Compute travel times for all zero-offset positions"""
    
    # Compute Velocity
    eps = epsr*8.854e-12
    sig = 10**logsig
    mu = 4*np.pi*1e-7
    
    v = np.sqrt(2/(mu*eps))/np.sqrt(np.sqrt(1 + (sig/(2*np.pi*fc*eps))**2) + 1)
    
    # Compute Travel Time
    t = 2*(np.sqrt((xrx-xp)**2 + dp**2)-R)/v
    
    return t

def fcnComputeVelocity(epsr,logsig,fc):
	"""Compute propagation velocity"""
    
    eps = epsr*8.854e-12
    sig = 10**logsig
    mu = 4*np.pi*1e-7
    w = 2*np.pi*fc
    
    v = np.sqrt(2/(mu*eps))/np.sqrt(np.sqrt(1 + (sig/(w*eps))**2) + 1)
    
    return v


def fcnComputeAlpha(epsr,logsig,fc):
	"""Compute attenuation factor"""
    
    eps = epsr*8.854e-12
    sig = 10**logsig
    mu = 4*np.pi*1e-7
    w = 2*np.pi*fc
    
    a = w*np.sqrt(mu*eps/2)*np.sqrt(np.sqrt(1 + (sig/(w*eps))**2) - 1)
    
    return a





########################################
#           PLOTS
########################################

