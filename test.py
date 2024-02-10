from uagents import Model
class route(Model):
    source: str
    destination: str
class Active_count(Model):
    count: int
    d: route
class active_user(Model):
    mob: int
    d: route
class active_bus(Model):
    id: int
    d: route

from uagents import Agent
from uagents.setup import fund_agent_if_low
storage = Agent(
    name="storage",
    port=8001,
    seed="modify data",
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(storage.wallet.address())


active = {
    1: Active_count(count=0,d("GHN","RTK")),
    2: Active_count(0,("GHN","SNP")),
    3: Active_count(0,("GHN","CHD")),
    4: Active_count(0,("GHN","JND")),
    5: Active_count(0,("GHN","DL")),
    6: Active_count(0,("GHN","KKD")),
    7: Active_count(0,("GHN","BWN")),

    8: Active_count(0,("RTK","GHN")),
    9: Active_count(0,("SNP","GHN")),
    10: Active_count(0,("CHD","GHN")),
    11: Active_count(0,("JND","GHN")),
    12: Active_count(0,("DL","GHN")),
    13: Active_count(0,("KKD","GHN")),
    14: Active_count(0,("BWN","GHN"))
}

for (number, status) in active.items():
    active.storage.set(status.count(), status.d())

