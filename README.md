**[summary](#summary) | [contents](#contents) | [usage](#usage) | [running the notebooks](#running-the-notebooks) | [issues](#issues) | [citation](#citation) | [license](#license)**

# Open source software for simulations and inversions of airborne electromagnetic data

[![Build Status](https://travis-ci.org/simpeg-research/heagy-2018-AEM.svg?branch=master)](https://travis-ci.org/simpeg-research/heagy-2018-AEM)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/simpeg-research/heagy-2018-AEM/master)
[![Azure](https://notebooks.azure.com/launch.png)](https://notebooks.azure.com/import/gh/simpeg-research/heagy-2018-aem)
[![Zenodo](https://zenodo.org/badge/124603211.svg)](https://zenodo.org/badge/latestdoi/124603211)
[![License](https://img.shields.io/github/license/simpeg-research/heagy-2018-AEM.svg)](https://github.com/simpeg-research/heagy-2018-AEM/blob/master/LICENSE)
[![SimPEG](https://img.shields.io/badge/powered%20by-SimPEG-blue.svg)](http://simpeg.xyz)

Notebooks and python scripts to reproduce the figures shown in
"[Open source software for simulations and inversions of airborne electromagnetic data](/Heagy_etal_2018_aem_workshop.pdf),"
submitted to the AEM 2018 workshop.


<img src="figures/currents.png" width=40% align="middle">

## Summary

Inversions of airborne EM data are often an iterative process, not only requiring that the researcher be able to explore the impact of changing components such as the choice of regularization functional or model parameterization, but also often requiring that forward simulations be run and fields and fluxes visualized in order to build an understanding of the physical processes governing what we observe in the data. In the hope of facilitating this exploration and promoting reproducibility of geophysical simulations and inversions, we have developed the open source software package, SimPEG. The software has been designed to be modular and extensible with the goal of allowing researchers to interrogate all of the components and to facilitate the exploration of new inversion strategies. We present an overview of the software in its application to airborne EM and demonstrate its use for visualizing fields and fluxes in a forward simulation as well as its flexibility in formulating and solving the inverse problem. We invert a line of airborne TDEM data over a conductive vertical plate using a 1D voxel-inversion, a 2D voxel inversion and a parametric inversion, where all of the forward modelling is done on a 3D grid. The results in this paper can be reproduced  by using the provided Jupyter notebooks. The Python software can also be modified to allow users to experiment with parameters and explore the physics of the electromagnetics and intricacies of inversion.

## Contents

There are 4 notebooks in this repository:

- [1_TEM_VerticalConductor_2D_forward.ipynb](/notebooks/1_TEM_VerticalConductor_2D_forward.ipynb) : runs a forward simulation of an airborne electromagnetic simulation over a conductive plate. This notebook was used to generate figures 1-4 in the abstract
- [2_TEM_VerticalConductor_1D_stitched_inversion.ipynb](/notebooks/2_TEM_VerticalConductor_1D_stitched_inversion.ipynb) : Using the forward simulated data from the previous notebook, we run 1D inversions over the plate (Figure 5 in the abstract).
- [3_TEM_VerticalConductor_2D_inversion_load.ipynb](/notebooks/3_TEM_VerticalConductor_2D_inversion_load.ipynb) : This notebook loads the 2D inversion results over the plate (Figure 6 in the abstract). The 2D inversion was run using the script [2dinv_smooth.py](/notebooks/2d_inv_smooth/2dinv_smooth.py).
- [4_TEM_VerticalConductor_parametric_inversion_load.ipynb](/notebooks/4_TEM_VerticalConductor_parametric_inversion_load.ipynb) : This notebook loads the 2D parametric inversion inversion results (Figure 7 in the abstract). The 2D parametric inversion was run using the script [2dinv_parametric.py](/notebooks/2d_inv_parametric/2d_inv_parametric.py) .

In addition, there are two notebooks used for demos in the workshop [3D EM Modelling and Inversion with Open Source Resources](https://courses.geosci.xyz/aem2018):

- [TEM_VerticalConductor_2D_forward.ipynb](/demo_notebooks/TEM_VerticalConductor_2D_forward.ipynb) : runs a forward simulation of an airborne electromagnetic simulation over a conductive plate. Similar to that in the notebooks directory.
- [TDEM_1D_inversion.ipynb](/demo_notebooks/TDEM_1D_inversion.ipynb): In this notebook, we run a 1D inversion for a single airborne time domain EM sounding

## Usage

Dependencies are specified in [requirements.txt](/requirements.txt)

```
pip install -r requirements.txt
```

To run the notebooks locally, you will need to have python installed,
preferably through [anaconda](https://www.anaconda.com/download/) .

You can then clone this repository. From a command line, run

```
git clone https://github.com/simpeg-research/heagy-2018-AEM.git
```

Then `cd` into the `heagy-2018-AEM` directory:

```
cd heagy-2018-AEM
```

To setup your software environment, we recommend you use the provided conda environment

```
conda env create -f environment.yml
conda activate aem-environment
```


alternatively, you can install dependencies through pypi

```
pip install -r requirements.txt
```

You can then launch Jupyter

```
jupyter notebook
```

Jupyter will then launch in your web-browser.

## Running the notebooks

Each cell of code can be run with `shift + enter` or you can run the entire notebook by selecting `cell`, `Run All` in the toolbar.

<img src="https://raw.githubusercontent.com/simpeg-research/heagy-2018-emcyl/revisions/figures/cell_run_all.png" width=80% align="middle">

For more information on running Jupyter notebooks, see the [Jupyter Documentation](https://jupyter.readthedocs.io/en/latest/)

## Issues

Please [make an issue](https://github.com/simpeg-research/heagy_2018_AEM/issues) if you encounter any problems while trying to run the notebooks.

## Citation

If you build upon or use these examples in your work, please cite:

Heagy, L. J., Kang, S., Cockett, R., & Oldenburg, D. W. (2018). Open source software for simulations and inversions of airborne electromagnetic data. In 7th International Workshop on Airborne Electromagnetics (pp. 1–5).

```
@inproceedings{Heagy2018,
author = {Heagy, Lindsey J and Kang, Seogi and Cockett, Rowan and Oldenburg, Douglas W.},
booktitle = {7th International Workshop on Airborne Electromagnetics},
keywords = {finite volume,frequency domain,inversion,open source software,time domain},
pages = {1--5},
title = {{Open source software for simulations and inversions of airborne electromagnetic data}},
year = {2018}
}
```

## License
These notebooks are licensed under the [MIT License](/LICENSE) which allows academic and commercial re-use and adaptation of this work.
