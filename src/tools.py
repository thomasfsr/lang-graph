from langchain_core.tools import tool
from typing import List, Type
import random
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

## Schemas:

class HistInput(BaseModel):
    input_numbers:List[int] = Field(description='Should be a list of integer numbers to be plotted')
    bins:int = Field(description='interger number of the number of bins')

class RandomInput(BaseModel):
    n_numbers:int = Field(description='Should be the number of random numbers')

class LowerCaseInput(BaseModel):
    text:str = Field(description="A text that will be lower case")

## Tools:

class Histogram_Tool(BaseTool):
    name:str = 'hist_tool'
    description: str ="""When it is necessary to Plot the histogram of a given array and the number."""
    args_schema: Type[BaseModel] = HistInput

    def _run(self,
             input_numbers:List[int],
             bins: int
             ) -> List[int]:
        from matplotlib import pyplot as plt
        plt.hist(x=input_numbers, bins=bins)
        plt.show()
        return input_numbers

class RandomTool(BaseTool):
    name:str='random_tool'
    description:str="""Returns a list of random numbers between 0-100."""
    args_schema: Type[BaseModel] = RandomInput

    def _run(self, n_numbers:int = None, **kwargs) -> List[int]:
        if n_numbers:
            return [random.randint(0, 100) for _ in range(n_numbers)]
        else:
            return 'give me the number of random numbers you need'

class LowerCaseTool(BaseTool):
    name:str = 'lower_case_tool'
    description:str= 'Returns the input as all lower case.'
    args_schema: Type[BaseModel] = LowerCaseInput
    def _run(self,
             text:str
             ) -> str:
        return text.lower()