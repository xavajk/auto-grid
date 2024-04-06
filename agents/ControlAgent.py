from spade.agent            import Agent
from spade.behaviour        import CyclicBehaviour, PeriodicBehaviour
from spade.template         import Template
from spade.message          import Message

class ControlAgent(Agent):
    class RecvForecastBehav(CyclicBehaviour):
        async def on_start(self):
            print("[CONTROL] Receiving behavior running...")

        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                print("[CONTROL] Message received with content: {}".format(msg.body))
                reply = Message(to=msg.sender, sender="control@blah.im")
                reply.body = "Forecast from {} received successfully...".format(msg.sender)
                await self.send(reply)
            else:
                print("[CONTROL] Did not receive any messages after 15 seconds...")
                print("[CONTROL] Waiting...")
        
        async def on_end(self):
            print("[CONTROL] Reciever behavior stopped.")

    async def setup(self):
        print("[CONTROL] ControlAgent started!")
        rbehav = self.RecvForecastBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        template.set_metadata("conversation-id", "forecast")
        self.add_behaviour(rbehav, template=template)