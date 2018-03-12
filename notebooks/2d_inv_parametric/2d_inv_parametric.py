from SimPEG import EM, Mesh, Utils
import numpy as np
from scipy.constants import mu_0
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from pymatsolver import PardisoSolver
from SimPEG import Maps

from SimPEG import EM, Mesh, Utils
import numpy as np
from scipy.constants import mu_0
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from pymatsolver import PardisoSolver
from SimPEG import Maps

cs, ncx, ncy, ncz, = 50., 20, 1, 20
npad_x, npad_y, npad_z = 10, 10, 10
pad_rate = 1.3
hx = [(cs,npad_x,-pad_rate), (cs,ncx), (cs,npad_x,pad_rate)]
hy = [(cs,npad_y,-pad_rate), (cs,ncy), (cs,npad_y,pad_rate)]
hz = [(cs,npad_z,-pad_rate), (cs,ncz), (cs,npad_z,pad_rate)]
mesh_3d = Mesh.TensorMesh([hx,hy,hz], 'CCC')
mesh_2d = Mesh.TensorMesh([hx,hz], 'CC')
inds = mesh_2d.vectorCCy<0.
mesh_2d_inv = Mesh.TensorMesh([hx,mesh_2d.hy[inds]], 'CN')
actind = mesh_2d.gridCC[:,1]<0.
map_2Dto3D = Maps.Surject2Dto3D(mesh_3d)
parametric_block = Maps.ParametricBlock(mesh_2d_inv) #, slopeFact=1
expmap = Maps.ExpMap(mesh_2d)
actmap = Maps.InjectActiveCells(mesh_2d, indActive=actind, valInactive=np.log(1e-8))
mapping = map_2Dto3D* expmap * actmap *  parametric_block

x = mesh_3d.vectorCCx[np.logical_and(mesh_3d.vectorCCx>-450, mesh_3d.vectorCCx<450)]
time = np.logspace(np.log10(5e-5), np.log10(2.5e-3), 21)
srcList = []
ind_start=0
for xloc in x:
    location = np.array([[xloc, 0., 30.]])
    rx_z = EM.TDEM.Rx.Point_dbdt(location, time[ind_start:], 'z')
    rx_x = EM.TDEM.Rx.Point_dbdt(location, time[ind_start:], 'x')
    src = EM.TDEM.Src.CircularLoop([rx_z], orientation='z', loc=location)
    srcList.append(src)
prb = EM.TDEM.Problem3D_e(mesh_3d, sigmaMap=mapping, Solver=PardisoSolver, verbose=False)
survey = EM.TDEM.Survey(srcList)
prb.timeSteps = [(1e-05, 15), (5e-5, 10), (2e-4, 10)]
survey.pair(prb)
parametric_block.slope = 1.

dobs = np.load('../dobs.npy')
DOBS = dobs.reshape((survey.nSrc, 2, time.size))[:,:,ind_start:]
dobs_dbdtz = DOBS[:, 0, :].flatten()

from SimPEG import (EM, Mesh, Maps, SolverLU, DataMisfit, Regularization,
                    Optimization, InvProblem, Inversion, Directives, Utils)
survey.dobs = dobs_dbdtz
survey.std = 0.05
survey.eps = 1e-14
# val_background,val_block, block_x0, block_dx, block_y0, block_dy
m0 = np.r_[np.log(0.005), np.log(0.05), 0, 150, -150, 100]
mesh_1d = Mesh.TensorMesh([parametric_block.nP])
dmisfit = DataMisfit.l2_DataMisfit(survey)
reg = Regularization.Simple(mesh_1d, alpha_x=0.)
reg.mref = np.zeros_like(m0)
opt = Optimization.InexactGaussNewton(maxIter=20, LSshorten=0.5)
opt.remember('xc')
invProb = InvProblem.BaseInvProblem(dmisfit, reg, opt)
invProb.beta = 0.
save_model = Directives.SaveModelEveryIteration()
save = Directives.SaveOutputEveryIteration()
# Create an inversion object
target=Directives.TargetMisfit()
inv = Inversion.BaseInversion(invProb, directiveList=[target, save_model, save])
prb.counter = opt.counter = Utils.Counter()
mopt = inv.run(m0)
