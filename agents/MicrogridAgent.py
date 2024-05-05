import os
import sys
import asyncio
import aioxmpp
import pandas as pd

from spade.agent            import Agent
from spade.message          import Message
from spade.template         import Template
from spade.presence         import ContactNotFound
from spade.behaviour        import FSMBehaviour, State

from models.Microgrids      import SimpleSCU

class MicrogridAgent(Agent):
    class ControlInteractionProtocol(FSMBehaviour):
        async def on_start(self) -> None:
            print('[MICROGRID] Beginning control interaction protocol...')

    class Failure(State):
        async def run(self) -> None:
            print('---------------------- [MICROGRID] IN FAILURE STATE ----------------------')
            await asyncio.sleep(5)

    class Initial(State):
        async def run(self) -> None:
            try:
                self.presence.subscribe('control@localhost')
            except ContactNotFound:
                while len(self.presence.get_contacts()) == 0:
                    await asyncio.sleep(1)
                self.presence.subscribe('control@localhost')
                print('[MICROGRID] Subscribed to Control agent.')

        async def on_end(self) -> None:
            if self.agent.mode == 3:
                self.set_next_state('fail')
            else:
                self.set_next_state('send-mg')

    class InformMicrogridStructure(State):
        async def on_start(self) -> None:
            self.set_template(Template(sender='control@localhost', metadata={'performative': 'query', 'reply-with': 'mg'}))
            
        async def run(self) -> None:
            msg = await self.receive(1)
            while not msg:
                msg = await self.receive(1)
            print('[MICROGRID] Received microgrid structure query from Control...')

            msg = Message(to='control@localhost', metadata={'performative': 'inform', 'in-reply-to': 'mg'})
            msg.body = self.agent.mg.get_state()
            print(f'[MICROGRID] Sending microgrid structure to Control...')
            await self.send(msg)

        async def on_end(self) -> None:
            if self.agent.mode == 3:
                self.set_next_state('fail')
            elif self.agent.mode == 0 or self.agent.mode == 1:
                self.set_next_state('receive-action')

    class ReceiveAction(State):
        async def on_start(self) -> None:
            print('[MICROGRID] Waiting to receive action from Control...')

        async def run(self) -> None:
            await asyncio.sleep(3)

        async def on_end(self) -> None:
            print('[MICROGRID] Performing optimized action from Control...')
            if self.agent.mode == 3:
                self.set_next_state('fail')
            elif self.agent.mode == 0 or self.agent.mode == 1:
                self.set_next_state('inform-state')

    class InformState(State):
        async def on_start(self) -> None:
            print('[MICROGRID] Informing Control of updated state...')

        async def run(self) -> None:
            await asyncio.sleep(3)

        async def on_end(self) -> None:
            if self.agent.mode == 3:
                self.set_next_state('fail')
            elif self.agent.mode == 0 or self.agent.mode == 1:
                self.set_next_state('receive-action')

    async def setup(self):
        self.modes = { 'default': 0, 'sim': 1, 'test': 2, 'fail': 3 }
        self.mode = self.modes['default']

        # initialize behaviors
        self.cip = self.ControlInteractionProtocol()
        self.cip.add_state(name='init', state=self.Initial(), initial=True)
        self.cip.add_state(name='send-mg', state=self.InformMicrogridStructure())
        self.cip.add_state(name='receive-action', state=self.ReceiveAction())
        self.cip.add_state(name='inform-state', state=self.InformState())
        self.cip.add_state(name='fail', state=self.InformState())
        self.cip.add_transition(source='init', dest='send-mg')
        self.cip.add_transition(source='send-mg', dest='receive-action')
        self.cip.add_transition(source='receive-action', dest='inform-state')
        self.cip.add_transition(source='inform-state', dest='receive-action')
        self.cip.add_transition(source='init', dest='fail')
        self.cip.add_transition(source='send-mg', dest='fail')
        self.cip.add_transition(source='receive-action', dest='fail')
        self.cip.add_transition(source='inform-state', dest='fail')
        self.add_behaviour(self.cip)

        # set up microgrid model
        self.mg = SimpleSCU()

        print("[MICROGRID] Microgrid agent started!")