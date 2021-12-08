import subprocess
from ..utilities.globals import SOX_PATH
from pathlib import Path


def resample(src_path: Path, dst_path: Path):
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    sox_arguments = [SOX_PATH, f'{src_path}', "-b", "16", "-c", "1", "-r", "16k", "-t", "wav",
                     f'{dst_path}']
    subprocess.call(sox_arguments)
