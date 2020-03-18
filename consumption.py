import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import matplotlib as mpl
import latex_style


brennwert = 11.475  # kWh / m^3
zustandszahl = 0.9524

mpl.rcParams.update(latex_style.with_latex)
data = np.genfromtxt('data.txt', skip_header=1).astype(int)
year, month, day, electricity, gas = data.T
datestr = [dates.datetime.date(y, m, d) for y, m, d in zip(year, month, day)]

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.xaxis.set_minor_locator(dates.MonthLocator())
ax1.xaxis.set_major_locator(dates.YearLocator())
ax1.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

ax1.plot_date(datestr, electricity-electricity[0], xdate=True, color='C0', ls='solid', label='electricity')
ax1.plot_date(datestr, (gas-gas[0])*brennwert*zustandszahl, xdate=True, color='C1', ls='solid', label='gas')
ax1.legend(loc=0)
ax1.set_xlabel('time')
ax1.set_ylabel('energy [kWh]', color='k')
ax1.grid(True)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot_date(datestr, gas-gas[0], xdate=True, color='C1')
ax2.set_ylabel(r'gas volume [m$^3$]', color='k')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('counter.png', bbox_inches='tight')
plt.close()

diff_date = np.diff(datestr)
elec_day = np.diff(electricity) / np.array([dt.total_seconds() / 3600 / 24 for dt in diff_date])
gas_day = np.diff(gas) / np.array([dt.total_seconds() / 3600 / 24 for dt in diff_date])

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.xaxis.set_minor_locator(dates.MonthLocator())
ax1.xaxis.set_major_locator(dates.YearLocator())
ax1.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

elec_day = np.append(np.append(0, np.repeat(elec_day, 2)), 0)
gas_day = np.append(np.append(0, np.repeat(gas_day, 2)), 0)
ax1.plot_date(np.repeat(datestr, 2), elec_day, xdate=True, color='C0', marker='', ls='solid', label='electricity')
ax1.plot_date(np.repeat(datestr, 2), gas_day*brennwert*zustandszahl/10., xdate=True, color='C1', marker='', ls='solid',
              label='gas [10 kWh]')
ax1.legend(loc=2)
ax1.set_xlabel('time')
ax1.set_ylabel('energy [kWh / day]', color='k')
max_kwh = 1.1 * max(np.max(gas_day), np.max(elec_day))
ax1.set_ylim([0, max_kwh])
ax1.grid(True)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot_date(np.repeat(datestr, 2), gas_day, xdate=True, color='C1', marker='', ls='solid')
ax2.set_ylabel(r'gas [m$^3$ / day]', color='k')
ax2.set_ylim([0, 10*max_kwh/brennwert/zustandszahl])

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('consumption.png', bbox_inches='tight')
plt.close()
