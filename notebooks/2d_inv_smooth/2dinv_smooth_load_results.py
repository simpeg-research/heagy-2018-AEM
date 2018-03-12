from SimPEG import EM, Mesh, Utils
import numpy as np
from pymatsolver import PardisoSolver
from SimPEG import Maps
import os
cur_dir = "D:/Seogi/Dropbox/Researches/AEM_workshow_2018_simpeg/2d_inv_warm_start"
os.chdir(cur_dir)
cs, ncx, ncy, ncz, = 50., 20, 1, 20
npad_x, npad_y, npad_z = 10, 10, 10
pad_rate = 1.3
hx = [(cs,npad_x,-pad_rate), (cs,ncx), (cs,npad_x,pad_rate)]
hy = [(cs,npad_y,-pad_rate), (cs,ncy), (cs,npad_y,pad_rate)]
hz = [(cs,npad_z,-pad_rate), (cs,ncz), (cs,npad_z,pad_rate)]
mesh_3d = Mesh.TensorMesh([hx,hy,hz], 'CCC')
mesh_2d = Mesh.TensorMesh([hx,hz], 'CC')
actind = mesh_2d.gridCC[:,1]<0.
map_2Dto3D = Maps.Surject2Dto3D(mesh_3d)
expmap = Maps.ExpMap(mesh_2d)
actmap = Maps.InjectActiveCells(mesh_2d, indActive=actind, valInactive=np.log(1e-8))
mapping = map_2Dto3D * expmap * actmap

x = mesh_3d.vectorCCx[np.logical_and(mesh_3d.vectorCCx>-450, mesh_3d.vectorCCx<450)]
time = np.logspace(np.log10(5e-5), np.log10(2.5e-3), 21)
ind_start=19
dobs = np.load('../dobs.npy')
DOBS = dobs.reshape((x.size, 2, time.size))[:,:,ind_start:]
dobs_dbdtz = DOBS[:, 0, :].flatten()
dobs_dbdtx = DOBS[:, 1, :].flatten()
#%%
import os
model = []
for File in os.listdir("."):
    if File.endswith(".npy"):
        model.append(np.load(File))        
#%%
import matplotlib.pyplot as plt
iteration = 5
blk1 = Utils.ModelBuilder.getIndicesBlock(
    np.r_[-100, 0],
    np.r_[100, -1000], 
    mesh_2d.gridCC
)
sig0 = 1
sigma0 = np.ones(mesh_2d.nC) * 1e-3
sigma0[blk1] = 1.
m0 = np.log(sigma0[actind])

temp =  expmap * actmap * model[iteration]

mesh_2d.plotImage(np.log10(temp), clim=(-3, -1))
plt.xlim(-2000, 2000)
plt.ylim(-2000, 0)