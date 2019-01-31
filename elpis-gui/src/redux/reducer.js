const initialState={
  // Below is the state the front end is aware of.
  model: {
    name: null,
    audioFiles: [],
    transcriptionFiles: [],
    additionalTextFiles: ['file1.txt'],
    pronunciationFile: null,
    settings: {
      frequency: null,
      mfcc: null,
      ngram: null,
      beam: null,
    },
    date: null
  },
  transcription: {
    name: null,
    modelName: null,
    results: {},
    audioFiles: [],
    date: null
  },
  modelList: [
  ],
}