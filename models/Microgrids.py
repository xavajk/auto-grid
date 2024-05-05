import numpy as np

from pymgrid import Microgrid
from pymgrid.modules import BatteryModule, LoadModule, RenewableModule, GridModule

class SimpleSCU():
    random_ts = { 'load': 100 + 100 * np.random.rand(24*60), 'wind': 200 * np.random.rand(24*60), 'solar': 200 * np.random.rand(24*60) }
    def __init__(self, days=60, load_ts=random_ts['load'], wind_ts=random_ts['wind'], solar_ts=random_ts['solar']) -> None:
        self._battery = BatteryModule(min_capacity=25, max_capacity=500, max_charge=100, max_discharge=100, efficiency=0.9, init_soc=0.2)
        self._load = LoadModule(load_ts)
        self._solar = RenewableModule(solar_ts)
        self._wind = RenewableModule(wind_ts)
        self._grid = GridModule(max_import=50, max_export=50, time_series=np.tile(np.array([[0.2, 0.1, 0.5, 1]]), (24 * days, 1)))
        self._mg = Microgrid([('ess', self._battery), ('load', self._load), ('pv', self._solar), ('wind', self._wind), ('grid', self._grid)])

    def get_state(self):
        return self._mg.dump()