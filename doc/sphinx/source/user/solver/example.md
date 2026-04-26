# Example

For this example, we will use the files from the AxiSEM3D repository [examples folder](https://github.com/AxiSEMunity/AxiSEM3D/tree/master/examples).


Run AxiSEM3D.

```bash
./build/axisem3D --input ./examples/00_global_1D/input
```

In this example AxiSEM3D uses as input, files from the `./examples/00_global_1D/input` directory.  If you did not specify `--input`, AxiSEM3D would look for a directory called `./input` and exit with a `Missing input directory` warning if not found.

The outputs are written to the default directory `./output`. Alternatively, you may specify an output directory by using the `--output` flag.

Upon execution AxiSEM3D will report back your parameters and execution detail:

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

      A            |i .|'''.|'||''''E'||    ||'  ____'||''|.
     |||   ... ...... ||..  ' ||  .   |||  |||   ` // ||   ||
    |  ||   '|..'  ||  ''|||. ||''|   |'|..'||    //  ||    ||
   .''''|.   .x.   ||      '||||      | 'M' ||    \\  ||    ||
  .|.  .||..|  ||..||.|'...|S.||....|.|. | .||.    3' D|...|'
  .............................................   //
                                                 /' v 1.1.0-pre

  Copyright (c) 2026 AxiSEM3D developers, MIT License
  Source, docs, and issues: github.com/AxiSEMunity/AxiSEM3D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


********************* WARNING FROM AxiSEM3D ********************
FROM: io::verifyDirectories
WHAT: Output directory exists; old output renamed to
      output__backup@2026-03-30T14:18:46
TIME: 2026-03-30T14:18:46
****************************************************************


========================== Exodus Mesh =========================

 ...

================================================================


============================ Geodesy ===========================

...

================================================================


====================== Absorbing Boundary ======================
user-specified boundaries  =  [RIGHT, BOTTOM]
* The mesh contains none of these boundaries.
================================================================


============================ Nr(s,z) ===========================
type   =  CONSTANT
value  =  5
================================================================


====================== Computed Nr on Mesh =====================
min Nr  =  5
max Nr  =  5
ave Nr  =  5
sum Nr  =  32945
* Nr has been limited by inplane resolution.
* Nr has been rounded up to FFTW lucky numbers.
================================================================


=========================== 3D Models ==========================
* No 3D models in this simulation.
================================================================


=========================== Time Step ==========================
Δt determined by mesh  =  0.2387
   Courant number      =  1
   location (r,θ)      =  [6.35118e+06, 0.16567]
Δt enforced by user    =  NONE
Δt to be used          =  0.2387
================================================================


========================== Attenuation =========================
frequency range      =  [0.001, 1]
reference frequency  =  1
# std linear solids  =  5
using CG4 mode       =  true
================================================================


===================== Computational Domain =====================

...

================================================================


============================ Sources ===========================

...

================================================================


======================== Simulation Time =======================
Δt of simulation          =  0.2387
t0 determined by sources  =  -125
t1 specified by user      =  1800
[t0, t1] used by solver   =  [-125.079, 1800.04]
# time steps              =  8066
================================================================


======================== Station groups ========================

...

================================================================


======================== Element groups ========================
* No element groups in this simulation.
================================================================



TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTTTTT NEWMARK TIME LOOP STARTS TTTTTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT


  wave propagation time / sec  =  113.382
  time step / num total steps  =  1000 / 8066 (12%)
  elapsed wall-clock time / h  =  0.00561265
  est. remaining w-c time / h  =  0.039659
  est. aggregate w-c time / h  =  0.0452716

  ...

```




See [Tools for Pre- and Post-processing](../processing/index.md) to visualize these results.

Next, let's look at the yaml files. Note that the yaml files are self describing. Here, for brevity, the comments have been removed.
