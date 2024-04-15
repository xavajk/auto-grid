import os
import sys
import datetime

from spade.agent            import Agent
from spade.message          import Message
from spade.template         import Template
from spade.behaviour        import CyclicBehaviour, PeriodicBehaviour

class MicrogridAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def on_start(self):
            print("[MG] Receiving behavior running...")

        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                print("[MG] Message received with content: {}".format(msg.body))
            else:
                print("[MG] Did not receive any messages after 15 seconds...")
                print("[MG] Waiting...")
        
        async def on_end(self):
            print("[MG] Reciever behavior stopped.")
            await self.agent.stop()

    async def setup(self):
        print("[MG] Microgrid agent interface started!")
        rbehav = self.RecvBehav()
        self.add_behaviour(rbehav)
        