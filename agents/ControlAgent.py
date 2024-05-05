import asyncio
import aioxmpp
import datetime

from aioxmpp                import PresenceShow
from spade.agent            import Agent
from spade.behaviour        import CyclicBehaviour, PeriodicBehaviour, FSMBehaviour, State, OneShotBehaviour
from spade.template         import Template
from spade.message          import Message
from spade.presence         import ContactNotFound

class ControlAgent(Agent):
    class MicrogridInteractionProtocol(FSMBehaviour):
        async def on_start(self) -> None:
            print('[CONTROL] Beginning microgrid interaction protocol...')

    class Failure(State):
        async def run(self) -> None:
            print('---------------------- [CONTROL] IN FAILURE STATE ----------------------')
            await asyncio.sleep(5)

    class Initial(State):
        async def run(self) -> None:
            try:
                self.presence.subscribe('microgrid@localhost')
            except ContactNotFound:
                while len(self.presence.get_contacts()) == 0:
                    await asyncio.sleep(1)
                self.presence.subscribe('microgrid@localhost')
                print('[CONTROL] Subscribed to Microgrid agent.')

            if self.agent.mode == 3:
                self.set_next_state('fail')
            else:
                self.set_next_state('query-mg')

    class QueryMicrogridStructure(State):
        async def on_start(self) -> None:
            self.set_template(Template(sender='microgrid@localhost', metadata={'performative': 'inform', 'in-reply-to': 'mg'}))

        async def run(self) -> None:
            print(f'[CONTROL] Sending microgrid structure query to Microgrid...')
            msg = Message(to="microgrid@localhost", metadata={'performative': 'query', 'reply-with': 'mg'})
            await self.send(msg)

            reply = await self.receive(1)
            while not reply:
                reply = await self.receive(1)
            print(f'[CONTROL] Received microgrid structure from Microgrid...')
            self.agent.mg_states.append(reply.body)

        async def on_end(self) -> None:
            if self.agent.mode == 3:
                self.set_next_state('fail')
            elif self.agent.mode == 0 or self.agent.mode == 1:
                self.set_next_state('receive-state')

    class ReceiveState(State):
        async def on_start(self) -> None:
            print('[CONTROL] Waiting to receive state from Microgrid...')

        async def run(self) -> None:
            print('[CONTROL] Running optimization for current microgrid state...')
            await asyncio.sleep(3)

        async def on_end(self) -> None:
            if self.agent.mode == 3:
                self.set_next_state('fail')
            elif self.agent.mode == 0 or self.agent.mode == 1:
                self.set_next_state('inform-action')

    class InformAction(State):
        async def on_start(self) -> None:
            print('[CONTROL] Informing Microgrid of optimized action...')

        async def run(self) -> None:
            await asyncio.sleep(3)

        async def on_end(self) -> None:
            if self.agent.mode == 3:
                self.set_next_state('fail')
            elif self.agent.mode == 0 or self.agent.mode == 1:
                self.set_next_state('receive-state')

    async def setup(self):
        self.modes = { 'default': 0, 'sim': 1, 'test': 2, 'fail': 3 }
        self.mode = self.modes['default']
        
        # microgrid interaction protocol behavior
        self.mgip = self.MicrogridInteractionProtocol()
        self.mgip.add_state(name='init', state=self.Initial(), initial=True)
        self.mgip.add_state(name='query-mg', state=self.QueryMicrogridStructure())
        self.mgip.add_state(name='inform-action', state=self.InformAction())
        self.mgip.add_state(name='receive-state', state=self.ReceiveState())
        self.mgip.add_state(name='fail', state=self.Failure())
        self.mgip.add_transition(source='init', dest='query-mg')
        self.mgip.add_transition(source='query-mg', dest='receive-state')
        self.mgip.add_transition(source='receive-state', dest='inform-action')
        self.mgip.add_transition(source='inform-action', dest='receive-state')
        self.mgip.add_transition(source='init', dest='fail')
        self.mgip.add_transition(source='query-mg', dest='fail')
        self.mgip.add_transition(source='receive-state', dest='fail')
        self.mgip.add_transition(source='inform-action', dest='fail')
        self.add_behaviour(self.mgip)

        # initialize structures
        self.mg_states = []

        print("[CONTROL] Control agent started!")
