from elpis.engines.kaldi.objects.interface import KaldiInterface


ENGINES = {
    "kaldi": KaldiInterface
}

default_engine = "kaldi"  # Get runtime engine from GUI later

print(f"Engine used: {default_engine}")

Interface = ENGINES[default_engine]

print(f"Interface used: {Interface}")


