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
    "model1",
    "model2",
    "model3",
    "model4",
    "model5",
  ],
}

let newFileList = []

const rootReducer = (state = initialState, action) => {

  switch(action.type) {
    
    case 'SET_MODEL_NAME':
      return {...state, model: {...state.model, name: action.name}}

    case 'ADD_TRANSCRIPTION_FILE':
      newFileList = state.model.transcriptionFiles.slice();
      newFileList.push(action.filename);
      return {
        model: {
          transcriptionFiles: newFileList,
          ...state.model
        },
        ...state
      }

    case 'ADD_AUDIO_FILE':
      newFileList = state.model.audioFiles.slice();
      newFileList.push(action.filename);
      return {
        model: {
          audioFiles: newFileList,
          ...state.model
        },
        ...state
      }

    case 'ADD_ADDITIONAL_TEXT_FILE':
      // newFileList = state.model.additionalTextFiles.slice();
      // newFileList.push(action.filename);

      newFileList = [...state.model.additionalTextFiles, action.filename ]

      console.log("reducer got file", action, newFileList)
      return {
        ...state,
        model: {
          ...state.model,
          additionalTextFiles: newFileList
        }
        
      }


    default:
      return state
  }
}

export default rootReducer
