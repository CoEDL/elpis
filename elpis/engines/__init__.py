import os
from pathlib import Path
from importlib import import_module

default_engine = "kaldi"  # We need later here an interaction with GUI to provide us the selected engine.
engine_list = {name: name for name in os.listdir("elpis/engines")}
engine = engine_list.get(default_engine, "kaldi")

print(f"Engine used: {engine}")

engine_path = Path(os.path.dirname(__file__)) / engine

module = import_module(f"elpis.engines.{engine}")
interface = import_module(f".objects.interface", module.__name__)
Interface = interface.interface_class

print(f"Interface used: {Interface}")


