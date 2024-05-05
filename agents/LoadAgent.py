import os
import sys
import datetime

from spade.agent            import Agent
from spade.message          import Message
from spade.template         import Template
from spade.behaviour        import CyclicBehaviour, PeriodicBehaviour


class LoadAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def on_start(self):
            print("[LOAD] Receiving behavior running...")

        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                print("[LOAD] Message received with content: {}".format(msg.body))
            else:
                print("[LOAD] Did not receive any messages after 15 seconds...")
                print("[LOAD] Waiting...")
        
        async def on_end(self):
            print("[LOAD] Reciever behavior stopped.")
            await self.agent.stop()

    async def setup(self):
        print("[LOAD] Load agent started!")
        rbehav = self.RecvBehav()
        self.add_behaviour(rbehav)
        