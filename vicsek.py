import sys,os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


nparticles = 10

np.random.seed(0)
config = np.random.random_sample((nparticles,2))
orient = np.random.random_sample((nparticles,))
speed = 0.01


def orient_to_vec(orient):
    angle = orient*np.pi*2
    vec = np.asarray((np.cos(angle),np.sin(angle))).T
    return vec


def translate(orient,config):
    config = np.modf(config + speed*orient_to_vec(orient)+2)[0]
    return config

def rotate(orient,config):
    for i in range(0,nparticles-1):
        neighbor_angle_av = orient[i]
        for j in range(i+1,nparticles):
            sep_vec = (config[i] - config[j])
            print(sep_vec)
            #if(sep_vec[0]*sep_vec[0] + sep_vec[1]*sep_vec[1] < dist_cut_squared):
             #   neighbor_angle_av += angle[j]
    orient = orient
    return orient




# set up figure and animation
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-0.1,1.1), ylim=(-0.1, 1.1))

# particles holds the locations of the particles
particles, = ax.plot([], [], 'bo', ms=1)

# rect is the box edge
bounds = [0,1,0,1]
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
    global rect, dt, ax, fig, config, orient

    config = translate(orient,config)
    orient = rotate(orient,config)
    ms = int(fig.dpi * 2 * 0.01 * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])
    
    # update pieces of the animation
    rect.set_edgecolor('k')
    particles.set_data(config[:, 0], config[:, 1])
    particles.set_markersize(ms)
    return particles, rect

ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)


# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#ani.save('particle_boxmp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
