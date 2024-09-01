import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

class LottoState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str