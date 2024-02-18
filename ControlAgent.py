import os
import sys
import datetime

from spade.agent            import Agent
from spade.behaviour        import CyclicBehaviour, PeriodicBehaviour
from spade.template         import Template
from spade.message          import Message
from wind_forecasting       import WindPredict

class ControlAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def on_start(self):
            print("[CONTROL] Receiving behavior running...")

        async def run():
            pass

    async def setup():
        pass