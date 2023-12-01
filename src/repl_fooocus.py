from rich import pretty
pretty.install()

from sdutils.utils_prompt import expand, progress
from sdutils.utils_fooocus import fooocusClient
fooocusClient.list_sizes()
fooocusClient.lists_styles()
fc = fooocusClient()
fc.set_size("1472x704")
print(fc.info())
print(f"Loaded Fooocus client as 'fc'")
gen = fc.generate
print(f"use 'gen' alias for fc.generate")
