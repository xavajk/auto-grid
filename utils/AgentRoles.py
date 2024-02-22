from abc import abstractmethod
from typing import List, NamedTuple
from spade.agent import Agent, AgentType
from dataclasses import dataclass, field
from collections import namedtuple

'''
Util Functions
'''
def _create_jid(jid: str, pwd: str):
    return JID(jid, pwd)

'''
Classes
'''
JID = namedtuple(typename='JID', field_names=['jid', 'pwd'])

@dataclass
class Role:
    jid: str
    __password: str
    __agents: List[AgentType]
    __identity: NamedTuple = field(default_factory=_create_jid(jid=jid, pwd=__password), metadata={'desc': 'Jabber (XMPP) ID (e.g., agent@xmpp.net)'})

    def __post_init__(self):
        self.__agents = 

    @abstractmethod
    def 