from pathlib import Path
from elpis.engines.common.input.resample import resample
from elpis.engines.common.objects.command import run
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
import subprocess
from typing import Callable, Dict
import os
import shutil
from distutils import dir_util, file_util
import wave
import contextlib
from subprocess import CalledProcessError
import librosa


class KaldiTranscription(BaseTranscription):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_file_path = self.path.joinpath('audio.wav')
        self.audio_duration = None

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.audio_file_path = self.path.joinpath('audio.wav')
        return self

    def _build_spk2utt_file(self, spk_id: str, utt_id: str):
        spk2utt_path = Path(self.path).joinpath('spk2utt')
        with spk2utt_path.open(mode='w') as fout:
                fout.write(f'{spk_id} {utt_id}\n')

    def _build_utt2spk_file(self, utt_id: str, spk_id: str):
        utt2spk_path = Path(self.path).joinpath('utt2spk')
        with utt2spk_path.open(mode='w') as fout:
                fout.write(f'{utt_id} {spk_id}\n')

    def _build_segments_file(self, utt_id: str, rec_id: str, start_ms: float, stop_ms: float):
        segments_path = Path(self.path).joinpath('segments')
        with segments_path.open(mode='w') as fout:
                fout.write(f'{utt_id} {rec_id} {start_ms} {stop_ms}\n')

    def _build_wav_scp_file(self, rec_id: str, rel_audio_file_path: Path):
        wav_scp_path = Path(self.path).joinpath('wav.scp')
        with wav_scp_path.open(mode='w') as fout:
                fout.write(f'{rec_id} {rel_audio_file_path}\n')

    def _process_audio_file(self, audio):
        # TODO: maintain original audio filename
        # copy audio to the tmp folder for resampling
        tmp_path = Path(f'/tmp/{self.hash}')
        tmp_path.mkdir(parents=True, exist_ok=True)
        tmp_file_path = tmp_path.joinpath('original.wav')
        with tmp_file_path.open(mode='wb') as fout:
            fout.write(audio.read())
        # resample the audio file
        resample(tmp_file_path, self.path.joinpath('audio.wav'))
        self.audio_duration = librosa.get_duration(filename=tmp_file_path)
        print("audio duration", self.audio_duration)

    # Prepare the files we need for inference, based on the audio we receive
    def _generate_inference_files(self):
        # _process_audio_file above a file named audio.wav
        audio_file_name = 'audio.wav'
        # Get the speaker id from the model > kaldi/data/test/spk2utt file. it's the first "word".
        model_spk2utt_path = Path(self.model.path).joinpath(
            'kaldi/data/test/spk2utt')
        with model_spk2utt_path.open(mode='r') as fin:
            spk_id = fin.read().split()[0]
        # Arbitrary id for each utterance. assuming one utterance for now
        utt_id = spk_id + '-utterance0'
        # Expecting to start at 0 time. Could benefit from VAD here?
        start_ms = 0.00
        # Duration of the audio
        abs_audio_file_path = Path(self.path).joinpath(audio_file_name)
        with contextlib.closing(wave.open(str(abs_audio_file_path), 'r')) as fin:
            frames = fin.getnframes()
            rate = fin.getframerate()
            stop_ms = frames / float(rate)
        # Rec id is arbitrary, use anything you like here
        rec_id = 'decode'
        # Path to the audio, relative to kaldi working dir
        rel_audio_file_path = os.path.join('data', 'infer', audio_file_name)
        # Generate the files
        self._build_spk2utt_file(spk_id, utt_id)
        self._build_utt2spk_file(utt_id, spk_id)
        self._build_segments_file(utt_id, rec_id, start_ms, stop_ms)
        self._build_wav_scp_file(rec_id, rel_audio_file_path)

    def transcribe(self, on_complete: Callable = None):
        # TODO move templates templates into transcription state dir, not model
        self.status = "transcribing"
        local_kaldi_path = self.model.path.joinpath('kaldi')
        kaldi_infer_path = self.model.path.joinpath('kaldi', 'data', 'infer')
        print("========= reset exp dir")
        # wipe previous dir to avoid file_exists errors
        exp_path = self.model.path.joinpath('kaldi','exp','tri1_online')
        if exp_path.exists():
            shutil.rmtree(f'{exp_path}')
            exp_path.mkdir(parents=True, exist_ok=True)

        print("========= reset templates dir")
        # TODO use gmm-decode for short audio and gmm-decode-online for long audio (gmm-decode is quicker)
        # Stage names (rh side) are used in the GUI for i18n
        if (self.audio_duration > 10):
            template_dir_path = 'gmm-decode-online-conf'
            stage_names = {
                "0_feature_vec.sh": "featureExtraction",
                "1_model_creation.sh": "modelCreation",
                "2_transcription_decode.sh": "transcriptionDecoding",
                "3_lattice_to_conf.sh": "ctmConversion",
                "4_ctm_output.sh": "ctmOutput"
            }
        else:
            template_dir_path = 'gmm-decode-conf'
            stage_names = {
                "gmm-decode-conf.sh": "transcribing"
            }
        # Move the relevant templates into the kaldi/data/infer dir.
        template_dir_abs_path = Path('/elpis/elpis/engines/kaldi/inference/').joinpath(template_dir_path)
        #  Build status for logging
        super().build_stage_status(stage_names)

        # Provide a helper script for both methods
        shutil.copy(Path('/elpis/elpis/engines/kaldi/templates').joinpath('make_split.sh'), f"{local_kaldi_path}")
        os.chmod(local_kaldi_path.joinpath('make_split.sh'), 0o774)

        # Prepare (dump, recreate) main transcription log file
        run_log_path = self.path.joinpath('transcription.log')
        if os.path.isfile(run_log_path):
            os.remove(run_log_path)
        run(f"touch {run_log_path};")

        # Organise stage logs in a dir
        transcription_log_dir = self.path.joinpath('transcription-logs')
        if os.path.exists(transcription_log_dir):
            shutil.rmtree(transcription_log_dir)
        os.mkdir(transcription_log_dir )

        stage_count = 0

        # Build stage scripts
        os.makedirs(f"{kaldi_infer_path}", exist_ok=True)
        dir_util.copy_tree(f'{self.path}', f"{kaldi_infer_path}")
        file_util.copy_file(f'{self.audio_file_path}', f"{self.model.path.joinpath('kaldi', 'audio.wav')}")
        # Copy parts of transcription process and chmod
        dir_util.copy_tree(f'{template_dir_abs_path}', f"{kaldi_infer_path.joinpath(template_dir_path)}")
        stages = os.listdir(kaldi_infer_path.joinpath(template_dir_path))
        for file in stages:
            os.chmod(kaldi_infer_path.joinpath(template_dir_path).joinpath(file), 0o774)
        for stage in sorted(stages):
            print(f"Stage {stage} starting")
            self.stage_status = (stage, 'in-progress', '')

            # Create log file
            stage_log_path = self.path.joinpath(os.path.join(transcription_log_dir, f'stage_{stage_count}.log'))
            with open(stage_log_path, 'w+') as file:
                print('starting log', file=file)
                pass

            # Run the command, log output. Also redirect Kaldi sterr output to log. These are often not errors :-(
            # These scripts must run from the kaldi dir (so set cwd)
            try:
                script_path = kaldi_infer_path.joinpath(template_dir_path, stage)
                print(script_path)
                stage_process = run(f"sh {script_path} >> {stage_log_path}", cwd=f"{local_kaldi_path}")
                with open(stage_log_path, 'a+') as file:
                    print('stdout', stage_process.stdout, file=file)
                    print('stderr', stage_process.stderr, file=file)
                    print('done', file=file)
                print(f"Stage {stage} complete")
                self.stage_status = (stage, 'complete', '')
                stage_count = stage_count + 1
            except CalledProcessError as error:
                with open(stage_log_path, 'a+') as file:
                    print('stderr', error.stderr, file=file)
                    print('failed', file=file)
                print(f"Stage {stage} failed")
                self.stage_status = (stage, 'failed', '')
                break

        # Concat all the files in the transcription-log dir
        log_filenames = os.listdir(transcription_log_dir)
        log_filenames.sort()
        with open(run_log_path, 'w') as outfile:
            for log_file in log_filenames:
                with open(os.path.join(transcription_log_dir, log_file)) as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")

        file_util.copy_file(f"{kaldi_infer_path.joinpath('one-best-hypothesis.txt')}", f'{self.path}/one-best-hypothesis.txt')
        file_util.copy_file(f"{kaldi_infer_path.joinpath('utterance-0.eaf')}", f'{self.path}/{self.hash}.eaf')

        self.status = "transcribed"

        if on_complete is not None:
            on_complete()

    def prepare_audio(self, audio, on_complete: Callable = None):
        self._process_audio_file(audio)
        self._generate_inference_files()
        if on_complete is not None:
            on_complete()

    def text(self):
        with open(f'{self.path}/one-best-hypothesis.txt', 'r') as fin:
            return fin.read()

    def elan(self):
        with open(f'{self.path}/{self.hash}.eaf', 'rb') as fin:
            return fin.read()