import os
import spade

from dotenv         import load_dotenv
from SolarAgent     import SolarAgent
from WindAgent      import WindAgent

load_dotenv()

async def start_solar():
    solar_jid = os.environ.get("SOLAR_JID")
    solar_pass = os.environ.get("SOLAR_PWD")
    solar = SolarAgent(solar_jid, solar_pass)
    await solar.start(auto_register=False)
    solar.web.start("localhost", 3000)

async def start_wind():
    wind_jid = os.environ.get("WIND_JID")
    wind_pass = os.environ.get("WIND_PWD")
    wind = WindAgent(wind_jid, wind_pass)
    await wind.start(auto_register=False)
    wind.web.start("localhost", 4000)

async def main():
    # start agents
    await start_solar()
    await start_wind()

if __name__ == '__main__':
    spade.run(main())