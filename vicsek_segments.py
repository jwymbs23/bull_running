import sys,os
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import matplotlib.cm as cm
import streets_in_region

#https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

nparticles = 100

np.random.seed(12827)
config = np.random.random_sample((nparticles,2))
angle = np.random.random_sample((nparticles,))*2*np.pi
#angle = np.asarray([np.pi/4, np.pi - np.pi/4])
#print(np.mean(angle))
orient = np.asarray((np.cos(angle),np.sin(angle))).T
#print(angle, orient)
#print(np.sum(orient/np.sqrt(np.sum(orient*orient)),axis = 1))
box_bound = 1
speed = box_bound*0.0005
dist_cut = box_bound*0.01
road_width = box_bound*0.01
#config = np.asarray([(0.5,1)])
skip = 10
dist_cut_squared = dist_cut*dist_cut
noise = 0.1*np.ones((nparticles,))
const_noise = 0.3

segment_temp = streets_in_region.scaled
segment = []

for i in segment_temp:
    if (i[1][0] - i[0][0])**2 + (i[1][1] - i[0][1])**2 > 0.00000001:
        segment.append(i)


segment = [[[0,0.5],[1,0.5]],[[0.5,0],[0.5,1]]]


seg_angle = [[(i[1][0] - i[0][0])/np.sqrt((i[1][0] - i[0][0])**2 + (i[1][1] - i[0][1])**2),(i[1][1] - i[0][1])/np.sqrt((i[1][0] - i[0][0])**2 + (i[1][1] - i[0][1])**2), (i[1][0]*i[0][1] - i[1][1]*i[0][1])/np.sqrt((i[1][0] - i[0][0])**2 + (i[1][1] - i[0][1])**2), np.sqrt((i[1][0] - i[0][0])**2 + (i[1][1] - i[0][1])**2)]  for i in segment]


def point_to_line(point, seg):
    seg = np.asarray(seg)
    point = np.asarray(point)
    return norm(np.cross(seg[1]-seg[0], seg[1] - point))/norm(seg[1] - seg[0])



def translate(config, orient):
    config = np.modf(config + speed*orient + 2)[0]
    return config

def rotate(orient):
#    global orient,config
    neighbor_angle_av = orient
    for i in range(0,nparticles-1):
        for j in range(i+1,nparticles):
            sep_vec = (config[i] - config[j])
            sep_vec = sep_vec - np.rint(sep_vec / box_bound)*box_bound
            if(np.sum(sep_vec*sep_vec) < dist_cut_squared):
                neighbor_angle_av[i] +=  orient[j]
                neighbor_angle_av[j] +=  orient[i]
    neighbor_angle_av /= np.sqrt(np.sum(neighbor_angle_av*neighbor_angle_av,axis=1))[:,None]
    return neighbor_angle_av 

def add_noise(orient):
    #global orient
    noise_term = noise*(np.random.random_sample((nparticles,))-0.5)*2*np.pi
    sine = np.sin(noise_term)
    cosine = np.cos(noise_term)
    xarray = orient[0:,0]
    yarray = orient[0:,1]
    #rotation matrix
    return np.asarray((xarray*cosine - yarray*sine, xarray*sine + yarray*cosine)).T


def stay_on_road(config, orient):
    for i in range(nparticles):
        dist_min = 100
        for jc,j in enumerate(segment):
            distance = point_to_line(config[i], j)
            if(distance < dist_min):
                dist_min = distance
                closest_s_id = jc
        if dist_min > road_width:
            p_coord = config[i]
            c_seg = np.asarray(segment[closest_s_id])
            #two ways to do this:
            #1: turn particle back straight onto road (seems like there might be issues when there are neighbors)
            sign = np.sign(np.cross(p_coord - c_seg[0], c_seg[1] - p_coord))
            orient[i] = np.asarray([(-sign*seg_angle[closest_s_id][1], sign*seg_angle[closest_s_id][0])])
            noise[i] = 0
        else: 
            noise[i] = const_noise
    return orient



# set up figure and animation
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-0.1,1.1), ylim=(-0.1, 1.1))

# particles holds the locations of the particles
coolwarm = plt.get_cmap('coolwarm')

particles, = ax.plot([], [], 'bo', ms=1)#, c=noise)#, cmap='coolwarm')

# rect is the box edge
bounds = [0,box_bound,0,box_bound]
rect = plt.Rectangle(bounds[::2],
                     bounds[1] - bounds[0],
                     bounds[3] - bounds[2],
                     ec='none', lw=2, fc='none')
#roadmap = np.asarray(segment)
#road_plot = plt.plot(roadmap[:,:,0].T,roadmap[:,:,1].T, c='black')
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
    for f in range(skip):
        config = translate(config, orient)
        if(i > 10):
            orient = rotate(orient)
            orient = add_noise(orient)
        orient = stay_on_road(config, orient)
    
    ms = int(fig.dpi * 2 * 0.005 * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])
    
    # update pieces of the animation
    rect.set_edgecolor('k')
    particles.set_data(config[:, 0], config[:, 1])
    particles.set_markersize(ms)
#    plt.savefig(str(frame)+'.png', bbox_inches = tight)
    return particles,rect

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
#ani.save('vicsek.gif', writer='imagemagick', fps=15)
#ani.save('vicsek.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

#plt.show()
