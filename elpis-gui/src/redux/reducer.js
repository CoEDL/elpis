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
    additionalWordFiles: [],
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


    default:
      return state
  }
}

export default rootReducer
