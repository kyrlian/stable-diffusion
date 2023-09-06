from rich import pretty
pretty.install()

from utils_prompt import expand, progress
from utils_fooocus import fooocusClient
fooocusClient.list_sizes()
fooocusClient.lists_styles()
fc = fooocusClient()
print(fc.info())
print(f"Loaded Fooocus client as 'fc'")