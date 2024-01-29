import datetime

from spade.agent            import Agent
from spade.behaviour        import CyclicBehaviour, PeriodicBehaviour
from pv_forecasting_ml      import PVPredict

class SolarAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def on_start(self):
            print("[SOLAR] Receiving behavior running...")

        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                print("[SOLAR] Message received with content: {}".format(msg.body))
            else:
                print("[SOLAR] Did not receive any messages after 15 seconds...")
                print("[SOLAR] Waiting...")
        
        async def on_end(self):
            print("[SOLAR] Reciever behavior stopped.")
            await self.agent.stop()

    class ForecastBehav(PeriodicBehaviour):
        async def run(self):
            print("[SOLAR] Forecasting behavior running...")
            pred = PVPredict()
            await pred.run()

        async def on_end(self):
            print("[SOLAR] Forcasting behavior stopped.")

    async def setup(self):
        print("[SOLAR] SolarAgent started!")
        rbehav = self.RecvBehav()
        start = datetime.datetime.now() + datetime.timedelta(seconds=15)
        fbehav = self.ForecastBehav(period=60, start_at=start)
        self.add_behaviour(rbehav)
        self.add_behaviour(fbehav)