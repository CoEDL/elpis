const initialState={
  foo: 'bar',
  incrementingThing: 0,
  myName: '',
  // above will need to be removed.
  // Below is the state the front end is aware of.
  model: {
    name: null,
    audioFiles: [],
    transcriptionFiles: [],
    additionalTextFiles: [],
    pronunciationDictionary: {},
    settings: {},
    date: null
  },
  transcription: {
    name: null,
    modelName: null,
    results: {},
    audioFiles: [],
    date: null
  }
}

const rootReducer = (state = initialState, action) => {

  switch(action.type) {

    case 'CHANGE_FOO':
      const newValue = action.foo
      return {...state, foo: newValue}

    case 'INCREMENT_SOMETHING':
      const i = state.incrementingThing + 1
      return {...state, incrementingThing: i}

    case 'UPDATE_MY_NAME':
      return {...state, myName: action.myName}
    
    
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
      newFileList = state.model.additionalTextFiles.slice();
      newFileList.push(action.filename);
      return {
        model: {
          additionalTextFiles: newFileList,
          ...state.model
        },
        ...state
      }


    default:
      return state
  }
}

export default rootReducer
