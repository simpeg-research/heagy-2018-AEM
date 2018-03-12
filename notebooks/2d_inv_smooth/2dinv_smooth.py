from SimPEG import EM, Mesh, Utils
import numpy as np
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
actind = mesh_2d.gridCC[:,1]<0.
map_2Dto3D = Maps.Surject2Dto3D(mesh_3d)
expmap = Maps.ExpMap(mesh_2d)
actmap = Maps.InjectActiveCells(mesh_2d, indActive=actind, valInactive=np.log(1e-8))
mapping = map_2Dto3D * expmap * actmap

x = mesh_3d.vectorCCx[np.logical_and(mesh_3d.vectorCCx>-450, mesh_3d.vectorCCx<450)]
time = np.logspace(np.log10(5e-5), np.log10(2.5e-3), 21)
srcList = []
for xloc in x:
    location = np.array([[xloc, 0., 30.]])
    rx_z = EM.TDEM.Rx.Point_dbdt(location, time, 'z')
    rx_x = EM.TDEM.Rx.Point_dbdt(location, time, 'x')
    src = EM.TDEM.Src.CircularLoop([rx_z], orientation='z', loc=location)
    srcList.append(src)
prb = EM.TDEM.Problem3D_e(mesh_3d, sigmaMap=mapping, Solver=PardisoSolver, verbose=False)
survey = EM.TDEM.Survey(srcList)
prb.timeSteps = [(1e-05, 15), (5e-5, 10), (2e-4, 10)]

#prb.timeSteps = [(2e-4, 14)]
survey.pair(prb)    
dobs = np.load('../dobs.npy')
DOBS = dobs.reshape((survey.nSrc, 2, time.size))
dobs_dbdtz = DOBS[:, 0, :].flatten()
dobs_dbdtx = DOBS[:, 1, :].flatten()

#%%

# put the omdel on the mesh 
blk1 = Utils.ModelBuilder.getIndicesBlock(
    np.r_[-100, 0],
    np.r_[100, -1000], 
    mesh_2d.gridCC
)
sig0 = 1e-3
mref = np.log(sig0)*np.ones(actmap.nP)
m0 = mref.copy()
#sigma0 = np.ones(mesh_2d.nC) * 1e-3
#sigma0[blk1] = 1.
#m0 = np.log(sigma0[actind])

from SimPEG import (EM, Mesh, Maps, DataMisfit, Regularization,
                    Optimization, InvProblem, Inversion, Directives, Utils)
survey.dobs = dobs_dbdtz
survey.std = 0.05
survey.eps = 1e-14
dmisfit = DataMisfit.l2_DataMisfit(survey)
reg = Regularization.Tikhonov(
    mesh_2d, alpha_s=1./mesh_2d.hx.min()**2, alpha_x=1., alpha_y=1.,
    indActive=actind
)
opt = Optimization.InexactGaussNewton(maxIter=20, LSshorten=0.5)
opt.remember('xc')
invProb = InvProblem.BaseInvProblem(dmisfit, reg, opt)
# Create an inversion object
beta = Directives.BetaSchedule(coolingFactor=5, coolingRate=3)
betaest = Directives.BetaEstimate_ByEig(beta0_ratio=1.)
target=Directives.TargetMisfit()
save_model = Directives.SaveModelEveryIteration()
save = Directives.SaveOutputEveryIteration()

inv = Inversion.BaseInversion(invProb, directiveList=[beta, betaest, target, save_model, save])
prb.counter = opt.counter = Utils.Counter()
reg.mref = mref
mopt = inv.run(m0)

np.save('mopt', mopt)
np.save('dpred', invProb.dpred)