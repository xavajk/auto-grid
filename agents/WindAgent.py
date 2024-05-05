import os
import sys
import datetime

from spade.agent            import Agent
from spade.behaviour        import CyclicBehaviour, PeriodicBehaviour
from spade.template         import Template
from spade.message          import Message
from tools.wind_forecasting       import WindPredict

class WindAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def on_start(self):
            print("[WIND] Receiving behavior running...")

        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                print("[WIND] Message received with content: {}".format(msg.body))
            else:
                print("[WIND] Did not receive any messages after 15 seconds...")
                print("[WIND] Waiting...")
        
        async def on_end(self):
            print("[WIND] Reciever behavior stopped.")

    # class ForecastBehav(PeriodicBehaviour):
    #     async def run(self):
    #         print("[WIND] Forecasting behavior running...")
    #         pred = WindPredict()
    #         await pred.run()
    #         msg = Message(to="control@blah.im")
    #         msg.set_metadata("performative", "inform")
    #         msg.body = "Successfully ran wind power forecasting..."
    #         await self.send(msg)

    #     async def on_end(self):
    #         print("[WIND] Forcasting behavior stopped.")

    async def setup(self):
        print("[WIND] Wind agent started!")
        rbehav = self.RecvBehav()
        self.add_behaviour(rbehav)