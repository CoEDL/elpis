#
#      =================================================================
#      =                  The Kaldi-Python interface                   =
#      =================================================================
#                                                                            
#                                                                            
#                             `.-://++ooo+++//:-.`                           
#                        `-/oyyyyysoo++++++oosyyyyyo/-`                      
#                     ./syhso/-.               `.-/oyyyo:`                   
#                  `:syyo:.                          ./oyyo-                 
#                `/yhs:`                                `/sys:               
#              `/yho.                                     `:yyo.             
#             .shs-                                         `+hy:            
#            :yh+`                                            :yy+           
#           +yy:                                               .yh+          
#          /hy-                                                 -yh/         
#         /hy-                                                   :hy-        
#        .yh/                  `.-::::-. .--...`                  ohs        
#        ohs               `-+osssssssss//sssssoo/.               .hh-       
#       :hy.             `:osssssssssssss-osssssssso-              oho       
#       sho             -osssssssssssssss//ssssssssss+.            :hy`      
#      .hh-            :sssssssssssssssss+:ssssssssssss-           `hh:      
#      /hy            :sssssssssssssssssso:sssssssssssss:           yh/      
#      ohs           .ssssssssssssssssssso:ssssssssssssss`          sh+      
#      sh+           ossssssssssssssssssso:ssssssssssssss.          sho      
#      yh/   `-+os: .sssssssssssssssssssso:ssssssssssssss-          sho      
#      yh/  .syhhh/ /sssssssssssssssssssso/ssssssssssssss-  ``      sh+      
#      yh/ .yhhhhh/ ossssssssssssssssssss+ossssssssssssss. :yso-    yh/      
#      sh+`shhhhhh: sssssssssssssssssssss:sssssssssssssss` shhhh+  .hh-      
#      ohyshhhhhhh: sssssssssssssssssssss:sssssssssssssso `yhhhhh/ :hh`      
#      +hy/yhhhhhh: ssssssssssssssssssss++ssssssssssssss+ /hhhhhhs`ohs       
#      `/- :hhhhhh- ssssssssssssssssssss:sssssssssssssss- shhhhhhhyhh/       
#           /yhhhh- ossssssssssssssssss/osssssssssssssss`-hhhhhhh++yy`       
#            ./ssy. +sssssssssssssssss++sssssssssssssss: ohhhhhhs` .`        
#                `  :sssssssssssssssss/ssssssssssssssso``yhhhhys.            
#                   `ssssssssssssssss/ssssssssssssssss- .syyso-              
#                    /sssssssssssssss/sssssssssssssss/    ``                 
#                    `ossssssssssssss+ssssssssssssss+                        
#                     .ssssssssssssss+sssssssssssss+                         
#                      .ossssssssssss+ssssssssssss/                          
#                       .osssssssssssosssssssssso-                           
#                         :ssssssssssssssssssso:`                            
#                          `/ssssssssssssssso:`                              
#                            `-/osssssssso/.                                 
#                                 `.--..`                                    
                                                                    

import os
import shlex
import subprocess

from shutil import copytree

# from elpis.paths import CURRENT_MODEL_DIR, CURRENT_TRANSCRIPTION_DIR, ELPIS_ROOT_DIR
CURRENT_MODEL_DIR, CURRENT_TRANSCRIPTION_DIR, ELPIS_ROOT_DIR = (
    '/elpis/current_model',
    '/elpis/current_transcription',
    '/elpis'
)

class Bridge(object):
    @classmethod
    def log(cls, content: str):
        log_path = os.path.join(ELPIS_ROOT_DIR, 'log.txt')
        with open(log_path, 'a') as fout:
            fout.write(content)

    @classmethod
    def run_to_log(cls, cmd: str, **kwargs) -> str:
        """Captures stdout/stderr and writes it to a log file, then returns the
        CompleteProcess result object"""
        args = shlex.split(cmd)
        if 'cwd' not in kwargs:
            kwargs['cwd'] = '/kaldi-helpers'
        process = subprocess.run(
            args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            **kwargs
        )
        cls.log(process.stdout.decode("utf-8"))
        return process

    @classmethod
    def file_replace_line_containing(cls, path, match, line):
        cls.run_to_log(f"sed -i '/{match}/c\{line}' {path}")

    @classmethod
    def ensure_exists(cls, dir: str):
        if os.path.exists(dir):
            return
        cls.run_to_log(f'mkdir -p { dir }')

    @classmethod
    def task(cls, taskname, **kwargs): 
        return cls.run_to_log(f'task {taskname}', **kwargs)

def run_elan():
    return Bridge.task('_run-elan')

def train():
    return Bridge.task('_train-test')

def transcribe():
    KALDI_OUTPUT_PATH = f"{CURRENT_MODEL_DIR}/output"
    Bridge.run_to_log(f'rm -rf { KALDI_OUTPUT_PATH }/kaldi/data/infer')
    copytree(f'{ KALDI_OUTPUT_PATH }/kaldi/data/test/',
             f'{ KALDI_OUTPUT_PATH }/kaldi/data/infer')
    return Bridge.task('infer')

def transcribe_align():
    return Bridge.task('infer-align')


Bridge.patch_kaldi_helpers()


# class KaldiModel(object):
#     @classmethod
#     def new(path: str) -> KaldiModel:

#         return None
#     def __init__(path):
#         super()