# 09 Regional Icesheet model

Regional scale model for Enceladus using topography. Topography model based on [Cadek et al., 2016]( https://doi.org/10.1002/2016GL068634). Geometric and volumetric models provided by [Dapre et al., 2024](https://doi.org/10.1029/2024JE008644).
uses colatitude of 60 degrees. includes ice, ocean, and upper crust. Models source as contractional Mw 3.2 at (0,0)

To generate the mesh run:
```
 python -m salvus_mesh_lite.interface AxiSEM --basic.model Enceladus.bm --basic.period 2 --spherical.min_radius 150 --chunk2D.max_colatitude 60 --output_file enceladus_2s_chunk.e
   ```

To run the solver run:
``` 
mpirun -np 6 ./axisem3d 
```
