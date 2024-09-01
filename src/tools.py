from langchain_core.tools import tool
from typing import List, Type
import random
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

## Schemas:

class HistInput(BaseModel):
    input_number:List[int] = Field(description='Should be a list of integer numbers')
    bins:int = Field(description='interger number of the number of bins')

class LowerCaseInput(BaseModel):
    text:str = Field(description="A text that will be lower case")

## Tools:

class HistTool(BaseTool):
    name = 'hist_tool'
    description="""Plot the histogram of a given array and the number. For instance: 1,2,3"""
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
    name='random_tool'
    description="""Returns a random number between 0-100. input the word 'random'"""

    def _run(self) -> int:
        return random.randint(0, 100)

class LowerCaseTool(BaseTool):
    name = 'lower_case_tool'
    description= 'Returns the input as all lower case.'
    args_schema: Type[BaseModel] = LowerCaseInput
    def _run(self,
             text:str
             ) -> str:
        return text.lower()