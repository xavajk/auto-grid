import os
import spade

from dotenv import load_dotenv
from SolarAgent import SolarAgent

load_dotenv()

async def start_solar():
    solar_jid = os.environ.get("SOLAR_JID")
    solar_pass = os.environ.get("SOLAR_PWD")
    solar = SolarAgent(solar_jid, solar_pass)
    await solar.start(auto_register=True)
    solar.web.start(hostname="localhost", port=7000)

async def main():
    # Start SolarAgent
    await start_solar();

if __name__ == '__main__':
    spade.run(main())