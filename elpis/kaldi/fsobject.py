import hashlib
import os
import shutil
import time
from . import KaldiError


class FileSystemObject(object):
    """
    Base class for objects that need their states reflected in a working
    directory and kaldi.
    """
    def __init__(self, working_path, save_path, kaldi_path):
        super().__init__()
        self._save_path = save_path
        self._working_path = working_path
        self._kaldi_path = kaldi_path

    def new(self, name):
        """
        Clears the current "working" object and creates a new "working" object.

        Before running this command, the {working_location}/ directory could be in any
        state. On running this command, the contents is deleted so that a new 
        object can take its place.

        The filesystem state after running this command is:
        {working_location}/
            name.txt
            date.txt
            hash.txt

        :raise KaldiError: if there is an attempts to create a object that already
        exists or if the name is invalid.
        """
        self._check_name(name)
        if os.path.exists(self._working_path):
            shutil.rmtree(self._working_path)
        os.mkdir(self._working_path)
        # write state files
        date = time.time()
        with open(f'{self._working_path}/name.txt', 'w') as fout:
            fout.write(name)
        with open(f'{self._working_path}/date.txt', 'w') as fout:
            fout.write(str(date))
        with open(f'{self._working_path}/hash.txt', 'w') as fout:
            hashname = hashlib.md5(bytes(str(date), 'utf-8')).hexdigest()
            fout.write(hashname)
        self.sync_to_kaldi()

    def get_name(self):
        return self._get_helper('name')

    def change_name(self, name):
        if os.path.exists(f'{self._working_path}/name.txt'):
            _check_name(name)
            with open(f'{self._working_path}/name.txt', 'w') as fout:
                fout.write(name)
            # Below I am breaking the rule about only making changes to one
            # location, then running a sync function, however, syncing may take
            # too long if we are updating the name everytime the user types. So
            # just here I break the rule ;)
            saved_path = f'{self._save_path}/{self.get_hash()}/name.txt'
            if os.path.exists(saved_path):
                with open(saved_path, 'w') as fout:
                    fout.write(name)
        else:
            raise KaldiError('need to create a model before changing the name')

    def get_date(self):
        return float(self._get_helper('date'))

    def get_hash(self):
        return self._get_helper('hash')

    def get_list(self):
        """Returns the list of object names that have been saved. Objects are saved
        in the `save_path` directory.
        """
        names = []
        for obj_dir in os.listdir(self._save_path):
            with open(f'{self._save_path}/{obj_dir}/name.txt', 'r') as fin:
                names.append(fin.read())
        return names

    def save(self):
        src = f'{self._working_path}/{self.get_hash()}'
        dst = f'{self._save_path}/{self.get_hash()}'
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        shutil.copytree(src, dst)

    def load(self, name):
        hash = self._get_hash_from_name(name)
        src = f'{self._save_path}/{hash}'
        dst = f'{self._working_path}/{hash}'
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
        shutil.copytree(src, dst)

    def sync_to_kaldi(self):
        if os.path.exists(self._kaldi_path):
            shutil.rmtree(self._kaldi_path)
        shutil.copytree(self._working_path, self._kaldi_path)

    def sync_to_working(self):
        if os.path.exists(self._working_path):
            shutil.rmtree(self._working_path)
        shutil.copytree(self._kaldi_path, self._working_path)

    def _get_helper(self, attr):
        if os.path.exists(f'{self._working_path}/{attr}.txt'):
            with open(f'{self._working_path}/{attr}.txt', 'r') as fin:
                return fin.read()
        raise KaldiError(
            f'tried to access {attr}, but no model has been created yet')

    def _check_name(self, name):
        if name in self.get_list():
            raise KaldiError(f'model already exists with the name: \'{name}\'')
        if name == '':
            raise KaldiError('invalid model name: \'\'')
        return

    def _get_hash_from_name(self, name):
        for model_dir in os.listdir(self._save_path):
            path = f'{self._save_path}/{model_dir}'
            with open(f'{path}/name.txt', 'r') as fin:
                if fin.read() == name:
                    with open(f'{path}/hash.txt', 'r') as fhash:
                        return fhash.read()
        KaldiError(f'cannot find object with name "{name}"')
