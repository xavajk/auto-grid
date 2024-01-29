from spade.agent        import Agent
from spade.behaviour    import CyclicBehaviour, PeriodicBehaviour

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
            print("ForecastBehav running...")
            


    async def setup(self):
        print("[SOLAR] SolarAgent started!")
        rbehav = self.RecvBehav()
        self.add_behaviour(rbehav)