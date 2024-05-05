import os
import spade
import asyncio

from dotenv                 import load_dotenv

from agents.SolarAgent      import SolarAgent
from agents.WindAgent       import WindAgent
from agents.BatteryAgent    import BatteryAgent
from agents.LoadAgent       import LoadAgent
from agents.ControlAgent    import ControlAgent
from agents.MicrogridAgent  import MicrogridAgent

load_dotenv()

os.environ['SSL_CERT_FILE'] = '/Users/xava/certs/cert.pem'

async def start_solar():
    solar_jid = os.environ.get("SOLAR_JID")
    solar_pass = os.environ.get("SOLAR_PWD")
    solar = SolarAgent(solar_jid, solar_pass, verify_security=True)
    await solar.start(auto_register=False)
    solar.web.start("localhost", 10001)

async def start_wind():
    wind_jid = os.environ.get("WIND_JID")
    wind_pass = os.environ.get("WIND_PWD")
    wind = WindAgent(wind_jid, wind_pass, verify_security=True)
    await wind.start(auto_register=False)
    wind.web.start("localhost", 10002)

async def start_battery():
    battery_jid = os.environ.get("BATTERY_JID")
    battery_pass = os.environ.get("BATTERY_PWD")
    battery = BatteryAgent(battery_jid, battery_pass, verify_security=True)
    await battery.start(auto_register=False)
    battery.web.start("localhost", 10003)

async def start_load():
    load_jid = os.environ.get("LOAD_JID")
    load_pass = os.environ.get("LOAD_PWD")
    load = LoadAgent(load_jid, load_pass, verify_security=True)
    await load.start(auto_register=False)
    load.web.start("localhost", 10004)

async def start_control():
    control_jid = os.environ.get("CONTROL_JID")
    control_pass = os.environ.get("CONTROL_PWD")
    control = ControlAgent(control_jid, control_pass, verify_security=True)
    await control.start(auto_register=False)
    control.web.start("localhost", 10005)

async def start_microgrid():
    mg_jid = os.environ.get("MG_JID")
    mg_pass = os.environ.get("MG_PWD")
    mg = MicrogridAgent(mg_jid, mg_pass, verify_security=True)
    await mg.start(auto_register=False)
    mg.web.start("localhost", 10006)

async def main():
    # start agents
    await start_microgrid()
    await start_control()
    # await start_solar()
    # await start_wind()
    # await start_battery()
    # await start_load()

if __name__ == '__main__':
    spade.run(main())