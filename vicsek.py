import sys,os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import matplotlib.cm as cm


#https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

nparticles = 100

np.random.seed(127)
config = np.random.random_sample((nparticles,2))
angle = np.random.random_sample((nparticles,))*2*np.pi
#angle = np.asarray([np.pi/4, np.pi - np.pi/4])
#print(np.mean(angle))
orient = np.asarray((np.cos(angle),np.sin(angle))).T
#print(angle, orient)
#print(np.sum(orient/np.sqrt(np.sum(orient*orient)),axis = 1))
speed = 0.05
box_bound = 1
dist_cut = 0.1
dist_cut_squared = dist_cut*dist_cut
noise = 0.2*np.random.random_sample((nparticles,))

def translate():
    global orient,config
    config = np.modf(config + speed*orient + 2)[0]
    return

def rotate():
    global orient,config
    neighbor_angle_av = orient
    for i in range(0,nparticles-1):
        for j in range(i+1,nparticles):
            sep_vec = (config[i] - config[j])
            sep_vec = sep_vec - np.rint(sep_vec / box_bound)*box_bound
            if(np.sum(sep_vec*sep_vec) < dist_cut_squared):
                neighbor_angle_av[i] +=  orient[j]
                neighbor_angle_av[j] +=  orient[i]
    #print(neighbor_angle_av)
    neighbor_angle_av /= np.sqrt(np.sum(neighbor_angle_av*neighbor_angle_av,axis=1))[:,None]
    #print(neighbor_angle_av)
    #sys.exit()
    return neighbor_angle_av #+ np.asarray((np.cos(noise_term),np.sin(noise_term))).T


def add_noise():
    global orient
    noise_term = noise*(np.random.random_sample((nparticles,))-0.5)*2*np.pi
    sine = np.sin(noise_term)
    cosine = np.cos(noise_term)
    xarray = orient[0:,0]
    yarray = orient[0:,1]
    return np.asarray((xarray*cosine - yarray*sine, xarray*sine + yarray*cosine)).T
#    angle_shift = np.arctan2(orient[0:,1], orient[0:,0]) +noise_term
    #    print('after',np.asarray((np.cos(angle_shift),np.sin(angle_shift))).T, angle_shift)
#    return np.asarray((np.cos(angle_shift),np.sin(angle_shift))).T




# set up figure and animation
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-0.1,1.1), ylim=(-0.1, 1.1))

# particles holds the locations of the particles
coolwarm = plt.get_cmap('coolwarm')
print(coolwarm)
particles, = ax.plot([], [], 'bo', ms=1)#, c=noise)#, cmap='coolwarm')

# rect is the box edge
bounds = [0,box_bound,0,box_bound]
rect = plt.Rectangle(bounds[::2],
                     bounds[1] - bounds[0],
                     bounds[3] - bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(rect)

def init():
    """initialize animation"""
    global rect
    particles.set_data([], [])
    rect.set_edgecolor('none')
    return particles, rect

def animate(i):
    """perform animation step"""
    global rect, dt, ax, fig, config, orient, noise
    
    translate()
    orient = rotate()
    orient = add_noise()
    
    ms = int(fig.dpi * 2 * 0.01 * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])
    
    # update pieces of the animation
    rect.set_edgecolor('k')
    particles.set_data(config[:, 0], config[:, 1])
    particles.set_markersize(ms)
    return particles, rect

ani = animation.FuncAnimation(fig, animate, frames=500,
                              interval = 20, blit=True, init_func=init)


# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#Writer = animation.writers['ffmpeg']
#writer=animation.FFMpegWriter(bitrate=500)

#writer = Writer(fps=30, metadata=dict(artist='jhard'), bitrate=100)
#ani.save('vicsek.gif', writer='imagemagick', fps=30)
#ani.save('vicsek.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
