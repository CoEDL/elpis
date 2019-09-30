from elpis.transformer import DataTransformer

elan = DataTransformer('Elan')


elan.set_importing_exts(['eaf', 'wav'])
elan.set_exporting_ext('eaf')

DEFAULT_TIER = 'Phrase'
GRAPHIC_RESOURCE_NAME = 'elan.png'

elan.context = {
    'tier': DEFAULT_TIER,
    'graphic': GRAPHIC_RESOURCE_NAME
}


@elan.importer
def importer(paths):
    """
    :param paths: List of file paths
    """
    # handle each file given in the paths individually
    pass

@elan.importer_for('wav', 'eaf')
def importer_for_wav_eaf(wav_paths, eaf_paths):
    """
    Import handler for processing all .wav and .eaf files.

    :param wav_paths: List of string paths to Wave files.
    :param eaf_paths: List of string paths to Elan files.
    """

    # handle only files that are specified (audio should have a hidden handler)
    pass


@elan.exporter
def exporter(audio_file_paths):
    """
    :param files: list of tuples representing
    """
    pass # TODO: 
    return (name, content)

@elan.add_setting('textbox', label='Tier', default=DEFAULT_TIER)
def change_tier(text):
    elan.context['tier'] = text
