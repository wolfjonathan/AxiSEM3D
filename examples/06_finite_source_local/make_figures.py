#!/usr/bin/env python3
"""
Example 06: Finite Source Local (San Francisco Bay Area) — publication figures.
  Fig 1: Velocity wavefield snapshots (4-panel: Vertical, East, North, PGV)
  Fig 2: Peak ground velocity map
  Fig 3: Three-component velocity seismograms at selected locations
Requires: output/stations/sfba_local
"""
import sys, os
import numpy as np
import pandas as pd

# Resolve everything relative to this file so the example is location-independent.
HERE = os.path.dirname(os.path.abspath(__file__))
# Make the shared pub_style helper (staged at examples/pub_style.py) importable.
sys.path.insert(0, os.path.dirname(HERE))
from pub_style import apply_style, save_fig, COLORS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

apply_style()

# INPUT: the AxiSEM3D run output produced by this example (mpirun ... --output output).
# The displacement seismograms live in the station group 'sfba_local'.
INPUT = os.path.join(HERE, 'output')

FIG_DIR = os.path.join(HERE, 'figures')
DATA_DIR = os.path.join(INPUT, 'stations', 'sfba_local')

if not os.path.isdir(DATA_DIR):
    print('Ex06: Simulation output not yet available. Run the simulation first '
          f'(expected per-rank NetCDF under {DATA_DIR}).')
    sys.exit(0)

try:
    import xarray as xr
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except ImportError as e:
    print(f'Ex06: Missing dependency: {e}')
    sys.exit(1)

# Load data
data = xr.open_mfdataset(
    os.path.join(DATA_DIR, 'axisem3d_synthetics.nc.*'),
    engine='netcdf4', data_vars='different',
    concat_dim='dim_station', combine='nested')

stations = pd.read_csv(
    os.path.join(HERE, 'input', 'STATIONS_OUTPUT.txt'),
    sep=r'\s+', header=2,
    names=['name', 'network', 'x', 'y', 'useless', 'depth'])

stations['name_network'] = [
    f'{net}.{nam:04d}' for nam, net in zip(stations['name'], stations['network'])]

station_names_decoded = np.array(
    [ls.decode('utf-8') if isinstance(ls, bytes) else str(ls)
     for ls in data['list_station'].values])
permutation_vector = np.array(
    [(nn == station_names_decoded).argmax() for nn in stations['name_network']])
stations['permutation'] = permutation_vector

# UTM coordinates
lat_pole, lon_pole = 37.7, -122.1
x_utm_origin, y_utm_origin = ccrs.UTM(zone=11).transform_point(
    lon_pole, lat_pole, src_crs=ccrs.Geodetic())
stations['x_utm'] = stations['x'] + x_utm_origin
stations['y_utm'] = stations['y'] + y_utm_origin

# Extract arrays
x_coords = stations['x_utm'].values
y_coords = stations['y_utm'].values
t_coords = data['data_time'].values
displacement_data = data['data_wave'].values[stations['permutation'], :, :]

# Convert displacement to velocity
dt = t_coords[1] - t_coords[0]
velocity_data = np.gradient(displacement_data, dt, axis=2)

# PGV
velocity_norm = np.sqrt(np.sum(velocity_data**2, axis=1))
pgv_final = np.max(velocity_norm, axis=1)

# ============================================================
# Figure 1: Wavefield snapshots at selected time
# ============================================================
print('Ex06 Fig 1: Velocity wavefield snapshots')

t_frac = 0.6
tstep = int(t_frac * len(t_coords))
tstep = min(tstep, len(t_coords) - 1)

proj = ccrs.UTM(zone=11)
vel_max = 0.1

fig, axes = plt.subplots(2, 2, figsize=(8, 8), dpi=150,
                          subplot_kw={'projection': proj})
titles = ['Vertical (Z)', 'East (E)', 'North (N)', 'PGV to time']
channels = [2, 0, 1, None]
cmaps = ['RdBu_r', 'RdBu_r', 'RdBu_r', 'YlOrRd']

pgv_running = np.max(velocity_norm[:, :tstep + 1], axis=1)

for idx, ax in enumerate(axes.flat):
    ax.set_extent((-122.7, -121.5, 37.2, 38.2), crs=ccrs.Geodetic())
    try:
        ax.coastlines(resolution='50m', linewidth=0.5, color='0.3')
    except Exception:
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor='0.3')
    ax.set_title(titles[idx], fontsize=10)

    if idx < 3:
        sc = ax.scatter(x_coords, y_coords, s=0.3,
                        c=velocity_data[:, channels[idx], tstep],
                        vmin=-vel_max, vmax=vel_max,
                        cmap=cmaps[idx], rasterized=True, transform=proj)
    else:
        sc = ax.scatter(x_coords, y_coords, s=0.3,
                        c=pgv_running, vmin=0, vmax=vel_max,
                        cmap=cmaps[idx], rasterized=True, transform=proj)

cbar_vel = fig.colorbar(
    plt.cm.ScalarMappable(norm=plt.Normalize(-vel_max, vel_max), cmap='RdBu_r'),
    ax=axes[0, :].tolist(), shrink=0.6, pad=0.02, orientation='horizontal',
    location='top')
cbar_vel.set_label('Velocity (m/s)', fontsize=9)

cbar_pgv = fig.colorbar(
    plt.cm.ScalarMappable(norm=plt.Normalize(0, vel_max), cmap='YlOrRd'),
    ax=axes[1, 1], shrink=0.7, pad=0.02, orientation='horizontal',
    location='bottom')
cbar_pgv.set_label('PGV (m/s)', fontsize=9)

fig.suptitle(f'SFBA Finite Fault — t = {t_coords[tstep]:.1f} s', fontsize=12, y=0.98)
save_fig(fig, os.path.join(FIG_DIR, 'ex06_wavefield_snapshots'))

# ============================================================
# Figure 2: Final PGV map
# ============================================================
print('Ex06 Fig 2: Peak ground velocity map')

fig, ax = plt.subplots(figsize=(6, 5), dpi=150,
                        subplot_kw={'projection': proj})
ax.set_extent((-122.7, -121.5, 37.2, 38.2), crs=ccrs.Geodetic())
try:
    ax.coastlines(resolution='50m', linewidth=0.6, color='0.2')
except Exception:
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6, edgecolor='0.2')

sc = ax.scatter(x_coords, y_coords, s=1, c=pgv_final,
                vmin=0, vmax=vel_max, cmap='YlOrRd', rasterized=True,
                transform=proj)
cbar = fig.colorbar(sc, ax=ax, shrink=0.7, pad=0.03)
cbar.set_label('Peak Ground Velocity (m/s)', fontsize=10)
ax.set_title('SFBA Finite Fault — PGV', fontsize=11)
save_fig(fig, os.path.join(FIG_DIR, 'ex06_pgv_map'))

# ============================================================
# Figure 3: Velocity seismograms at selected stations
# ============================================================
print('Ex06 Fig 3: Velocity seismograms')

n_sel = 5
np.random.seed(42)
high_pgv_idx = np.argsort(pgv_final)[-50:]
sel_indices = np.sort(np.random.choice(high_pgv_idx, n_sel, replace=False))

fig, axes = plt.subplots(n_sel, 1, figsize=(8, 2 * n_sel), sharex=True)
ch_labels = ['E', 'N', 'Z']
ch_colors = [COLORS['primary'], COLORS['accent'], COLORS['secondary']]

for i, si in enumerate(sel_indices):
    ax = axes[i]
    for ch in range(3):
        ax.plot(t_coords, velocity_data[si, ch, :],
                color=ch_colors[ch], lw=0.7, label=ch_labels[ch],
                alpha=0.85)
    ax.set_ylabel('Vel. (m/s)', fontsize=8)
    sx, sy = stations.iloc[si]['x'] / 1e3, stations.iloc[si]['y'] / 1e3
    ax.text(0.02, 0.92, f'({sx:.0f}, {sy:.0f}) km',
            transform=ax.transAxes, fontsize=7, va='top',
            bbox=dict(boxstyle='round,pad=0.2', fc='wheat', alpha=0.7))
    if i == 0:
        ax.legend(loc='upper right', fontsize=7, ncol=3)

axes[-1].set_xlabel('Time (s)')
axes[0].set_title('SFBA Finite Fault — Velocity at high-PGV stations', fontsize=11)
plt.tight_layout()
save_fig(fig, os.path.join(FIG_DIR, 'ex06_velocity_seismograms'))

print('Ex06 figures complete.')
