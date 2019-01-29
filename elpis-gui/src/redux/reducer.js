const initialState={
  foo: 'bar',
  incrementingThing: 0,
  myName: ''
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
