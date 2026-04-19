import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Constants

h_cubits    = 652.5          # Mountain height in cubits
cubit_to_km = 4.752e-4       # Hashimi cubit in km
h_km        = h_cubits * cubit_to_km   # Height in km
R_modern    = 6371.0         # Modern mean Earth radius (km)


# Angle array: 30 to 40 arcminutes

delta_arcmin = np.linspace(30, 40, 2000)
delta_rad    = delta_arcmin * (np.pi / (180.0 * 60.0))


# Al-Biruni's formula:  R = h * cos(d) / (1 - cos(d))

cos_delta = np.cos(delta_rad)
R_km_arr  = h_km * cos_delta / (1.0 - cos_delta)


# Al-Biruni's observed angle: 34 arcminutes

d_b_arcmin  = 34.0
d_b_rad     = d_b_arcmin * (np.pi / (180.0 * 60.0))
cos_b       = np.cos(d_b_rad)
R_b_cubits  = h_cubits * cos_b / (1.0 - cos_b)
R_b_km      = R_b_cubits * cubit_to_km
err_pct     = abs(R_b_km - R_modern) / R_modern * 100.0

# Numerical sensitivity: dR/d(delta) at 34' (finite difference, 1-arcmin window)

idx_lo = np.searchsorted(delta_arcmin, 33.5)
idx_hi = np.searchsorted(delta_arcmin, 34.5)
dR_dd  = (R_km_arr[idx_hi] - R_km_arr[idx_lo]) / (delta_arcmin[idx_hi] - delta_arcmin[idx_lo])


# Print summary

print("=" * 58)
print("  AL-BIRUNI MOUNTAIN-DIP SIMULATION — SUMMARY")
print("=" * 58)
print(f"  Mountain height        : {h_cubits} cubits")
print(f"                         : {h_km*1000:.1f} m  ({h_km:.5f} km)")
print(f"  Cubit conversion used  : {cubit_to_km*1e4:.3f} cm/cubit (hashimi)")
print(f"  Observed dip angle     : {d_b_arcmin}' = {np.degrees(d_b_rad):.4f} deg")
print(f"  Computed radius        : {R_b_cubits:,.0f} cubits")
print(f"  Computed radius        : {R_b_km:,.1f} km")
print(f"  Modern mean radius     : {R_modern:,.1f} km")
print(f"  Absolute error         : {abs(R_b_km - R_modern):.1f} km")
print(f"  Percentage error       : {err_pct:.2f}%")
print(f"  Accuracy               : {100 - err_pct:.2f}%")
print(f"  Sensitivity dR/dd      : {dR_dd:.0f} km per arcminute")
print("=" * 58)

# Table: every integer arcminute 30..40
print("\n  Table: Dip Angle vs Computed Earth Radius")
print(f"  {'Angle (arcmin)':>15}  {'Angle (deg)':>12}  {'R (km)':>10}  {'Error (km)':>12}  {'Err %':>7}")
print("  " + "-"*62)
for d_am in range(30, 41):
    d_r   = d_am * np.pi / (180 * 60)
    c     = np.cos(d_r)
    R_row = h_km * c / (1 - c)
    err_r = R_row - R_modern
    ep    = err_r / R_modern * 100
    marker = " <-- al-Biruni" if d_am == 34 else ""
    print(f"  {d_am:>15}  {np.degrees(d_r):>12.4f}  {R_row:>10.1f}  {err_r:>+12.1f}  {ep:>+7.2f}%{marker}")

print()


# Plot

fig, ax = plt.subplots(figsize=(9, 5.5))

ax.plot(delta_arcmin, R_km_arr, color='steelblue', linewidth=2.2,
        label='Computed $R$ (al-Biruni formula)', zorder=3)

ax.axhline(y=R_modern, color='forestgreen', linestyle='--', linewidth=1.6,
           label=f'Modern mean radius ({R_modern:.0f} km)', zorder=2)

ax.axvline(x=34, color='firebrick', linestyle='--', linewidth=1.5,
           label=f"Al-Biruni's angle ($\\delta = 34'$)", zorder=2)

ax.scatter([34], [R_b_km], color='firebrick', s=90, zorder=5,
           label=f"Al-Biruni's result ({R_b_km:.0f} km, {err_pct:.2f}\\% error)")

# Shade the region between 33' and 35' to visualise ±1' uncertainty
idx_33 = np.searchsorted(delta_arcmin, 33)
idx_35 = np.searchsorted(delta_arcmin, 35)
ax.fill_between(delta_arcmin[idx_33:idx_35+1], R_km_arr[idx_33:idx_35+1],
                alpha=0.12, color='firebrick', label='±1\' measurement band')

ax.set_xlabel(r"Dip Angle $\delta$ (arcminutes)", fontsize=12)
ax.set_ylabel("Computed Earth Radius (km)", fontsize=12)
ax.set_title("Sensitivity of Al-Biruni's Earth Radius Estimate\nto Variation in Measured Dip Angle",
             fontsize=13, pad=10)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9.5, loc='upper right')
ax.set_xlim(30, 40)

plt.tight_layout()
print("Plot saved to biruni_sensitivity.pdf / .png")