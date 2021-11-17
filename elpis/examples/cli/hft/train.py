# Example code for using elpis from python.

# Must run from the docker contianer and the objects must not exist in the interface directory already ('ds', 'mx')

# python elpis/examples/cli/hft/train.py


from elpis.engines.common.objects.interface import Interface

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
elpis = Interface(path='/state', use_existing=True)

# Step 1
# ======
# Setup a dataset to to train data on.
ds = elpis.new_dataset('ds')
ds.add_directory('/datasets/abui/transcribed', extensions=['eaf', 'wav'])
ds.auto_select_importer()  # Selects Elan because of eaf file.
ds.importer.set_setting('tier_name', 'Phrase')
ds.process()

# Step 2
# ======
# Select Engine
from elpis.engines import ENGINES
engine_name = 'hftransformers'
engine = ENGINES[engine_name]
elpis.set_engine(engine)

# Step 3
# ======
# Build pronunciation dictionary
# if 'pd' not in elpis.list_pron_dicts():
#     pd = elpis.new_pron_dict('pd')
#     pd.link(ds)
#     pd.set_l2s_path('/recordings/letter_to_sound.txt')
#     pd.generate_lexicon()
# else:
#     pd = elpis.get_pron_dict('pd')

# Step 4
# ======
# Link dataset and pd to a new model, then train the model.
m = elpis.new_model('mx')
m.link_dataset(ds)
# m.link_pron_dict(pd)
# m.build_kaldi_structure()
m.train()  # may take a while
