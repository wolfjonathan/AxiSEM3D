# Example 06: Kinematic finite-fault rupture (San Francisco Bay Area)

This example simulates ground motion from an earthquake in the San Francisco Bay
Area (SFBA) using a local 3D crustal velocity model with topography and a Moho
interface on a Cartesian (`AxiSEMCartesian`) mesh. A kinematic finite-fault
rupture can be approximated as a collection of point moment-tensor sources (one
Gaussian source-time function per subsource); the shipped `inparam.source.yaml`
uses a single representative moment-tensor source, and `input_setup.ipynb` shows
how to format a multi-subsource list. Surface ground motion is recorded on a
dense grid of stations for animating the wavefield and mapping peak ground
velocity.

## Contents
- `input/inparam.model.yaml` — 1D/3D model: references the Exodus mesh and the
  SFBA 3D velocity layers, topography and Moho undulation.
- `input/inparam.source.yaml` — time axis (`record_length: 30 s`) and the
  moment-tensor source; a Gaussian STF with `half_duration: 2 s` band-limited to
  the mesh.
- `input/inparam.nr.yaml` — azimuthal resolution Nr (POINTWISE, from
  `point_source_approx.nc`), with wavefield scanning enabled.
- `input/inparam.output.yaml` — station group `sfba_local` (reads
  `STATIONS_OUTPUT.txt`).
- `input/inparam.advanced.yaml` — advanced/solver settings.
- `input/AxiSEMCartesian_sfba_m500_2s.e` — the shipped coarse 2 s Exodus mesh.
- `input/sfba_2018_m500.bm` — polynomial background model used to build the mesh.
- `input/genmesh.sh` — command that generates the mesh from the `.bm` file.
- `input/STATIONS_OUTPUT.txt` — surface station grid for the recorded output.
- `input/example_input_source_list.txt` — example formatted subsource list
  produced by `input_setup.ipynb` (format template for a multi-subsource rupture).
- `input/point_source_approx.nc` — pointwise Nr field used by `inparam.nr.yaml`.
- `input/moho_smooth_24km.nc` — Moho undulation grid used by `inparam.model.yaml`.
- `input_setup.ipynb` — builds the source list and `STATIONS_OUTPUT.txt`.
- `make_figures.py` — generates the publication figures from `output/`.
- `post_processing.ipynb` — notebook that produces the surface-wavefield
  animation and figures from `output/`.

## Requirements

You need a built `axisem3d` solver and an MPI runtime. Either put the `axisem3d`
binary on your `PATH` or copy it into this directory as `./axisem3d`. The figure
script additionally needs Python with `numpy`, `pandas`, `xarray`, `netcdf4`,
`matplotlib` and `cartopy`.

## Reproduce

### 1. Mesh
The shipped mesh `input/AxiSEMCartesian_sfba_m500_2s.e` is a **2 s** Cartesian
`AxiSEMCartesian` mesh (910 elements), built from the polynomial background model
`input/sfba_2018_m500.bm`. It is already included, so you only need this step to
regenerate or refine it (lower `--basic.period` for a finer mesh). Run from
`input/`:
```
sh genmesh.sh
```
which executes:
```
python -m salvus_mesh_lite.interface AxiSEMCartesian \
    --basic.model sfba_2018_m500.bm --basic.period 2.0 \
    --attenuation.frequencies 0.01 10.0 \
    --cartesian2Daxisem.x 60.0 --cartesian2Daxisem.min_z 6326.1 \
    --output_file AxiSEMCartesian_sfba_m500_2s.e
```

### 2. Large data
The 3D velocity model referenced in `inparam.model.yaml` is too large to ship in
git and must be downloaded and copied into `input/`:
`SFBA_layer1_min500.nc`, `SFBA_layer2.nc`, `SFBA_layer3.nc`, `SFBA_layer4.nc`,
and `topo_smooth_100m_upsampled.nc`. Obtain them from Zenodo:
https://zenodo.org/records/20017355

### 3. Run
The shipped 2 s mesh has only 910 elements, so it runs comfortably on a single
machine. From this example directory, run the solver inline:
```
mpirun -np 16 axisem3d --input input --output output
```
(16 ranks leaves ~57 elements/rank; scale the count up if you refine the mesh.)
On a cluster, wrap the `mpirun` command in your scheduler's job script and load
your compiler, MPI, netCDF and HDF5 modules.

The run writes per-rank NetCDF station output to
`output/stations/sfba_local/axisem3d_synthetics.nc.rank*`.

### 4. Figures
Once `output/` exists, generate the publication figures:
```
python make_figures.py
```
`make_figures.py` reads the per-rank station NetCDF directly from
`output/stations/sfba_local/` (the `INPUT` variable at the top of the script,
defaulting to `./output`) and `input/STATIONS_OUTPUT.txt`. It differentiates the
recorded displacement in time to velocity, then writes three figures (PDF + PNG)
to `figures/`:

- `figures/ex06_wavefield_snapshots.{pdf,png}` — 4-panel map snapshot at
  t ≈ 60 % of the record: vertical (Z), east (E) and north (N) velocity
  (RdBu_r, ±0.1 m/s) plus a running peak-ground-velocity panel (YlOrRd), in a
  UTM zone 11 projection over the SFBA.
- `figures/ex06_pgv_map.{pdf,png}` — peak ground velocity (max of the velocity
  norm over the full record) at every station, YlOrRd, same SFBA extent.
- `figures/ex06_velocity_seismograms.{pdf,png}` — three-component (E/N/Z)
  velocity seismograms at 5 high-PGV stations, each labeled with its (x, y)
  location in km.

The maps use coarse coastlines only (Cartopy `resolution='50m'`, no state or
country borders) on a white background. The figure script imports the shared
`pub_style.py` helper from the parent `examples/` directory (colorblind-safe
palette, SI units); if the simulation output is absent it prints a notice and
exits cleanly. `post_processing.ipynb` is a notebook alternative that also builds
the surface-wavefield animation.

## Notes
Prepared/updated by Jonathan Wolf.
