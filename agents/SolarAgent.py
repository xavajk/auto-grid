import os
import sys
import asyncio
import datetime

from aioxmpp                import PresenceShow, PresenceState

from spade.agent            import Agent
from spade.message          import Message
from spade.template         import Template
from spade.behaviour        import CyclicBehaviour, TimeoutBehaviour, OneShotBehaviour, FSMBehaviour, State

from tools.pv_forecasting   import PVPredict

class SolarAgent(Agent):
    class SpinupSolar(FSMBehaviour):
        async def on_start(self) -> None:
            print("[SOLAR] Beginning initialization...")
            self.exit_code = 'Initializing'

        async def on_end(self) -> None:
            print("[SOLAR] Agent initialized!")

    class WaitForControlState(State):
        async def run(self) -> None:
            print('[SOLAR] At state one')
            self.set_template(Template(sender='control@localhost', metadata={'performative': 'subscribe', 'protocol': 'pnp'}))
            msg = await self.receive(timeout=10)
            print(f"[SOLAR] Received message from control with body: ")
            self.set_template(Template(to='solar@localhost', sender='microgrid@localhost', metadata={'performative': 'inform', 'in-reply-to': 'state'}))
            self.set_next_state('PrepareAndSendState')

    class PrepareAndSendState(State):
        async def run(self) -> None:
            print('[SOLAR] At state two')
            msg = Message(to='microgrid@localhost',
                          sender='solar@localhost', 
                          metadata={'performative': 'query', 'reply-with': 'state'})
            await self.send(msg)
            state = await self.receive(timeout=60)
            print(f"[SOLAR] Received message from microgrid with body: {state.body}")
            msg = Message(to='control@localhost', 
                          sender='solar@localhost', 
                          body=state.body,
                          metadata={'performative': 'inform', 'in-reply-to': 'state'})

    async def setup(self):
        # initialization behavior
        self.init = self.SpinupSolar()
        self.init.add_state(name='WaitForControlState', state=self.WaitForControlState(), initial=True)
        self.init.add_state(name='PrepareAndSendState', state=self.PrepareAndSendState())
        self.init.add_transition(source='WaitForControlState', dest='PrepareAndSendState')
        self.add_behaviour(self.init)
        print("[SOLAR] Solar agent started!")