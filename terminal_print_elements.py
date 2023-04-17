# Rich text function to display list or dictionarys in panel form

from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
import json

# Test data with three columns 'Name' 'Age' 'City' and 10 persons

data = [["John Smith", 33, "New York"],
    ["Jane Doe", 32, "Paris"],
    ["Sam Doe", 35, "London"],
    ["Susan", 33, "New York"],
    ["John Smith", 33, "Sydney"],
    ["Jane Doe", 32, "Amsterdam"],
    ["Sam Doe", 35, "London"],
    ["Susan", 33, "New York"],
    ["John Smith", 33, "Sydney"]]

json_data = json.dumps(data)