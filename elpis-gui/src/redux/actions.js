export const changeFoo = foo => {
  return { type: 'CHANGE_FOO', foo }
}
export const incrementSomething = () => {
  return { type: 'INCREMENT_SOMETHING' }
}
export const updateMyName = myName => {
  return { type: 'UPDATE_MY_NAME', myName }
}


export const setModelName = name => {
  return { type: 'SET_MODEL_NAME', name };
}
export const addTranscriptionFile = filename => {
  return { type: 'ADD_TRANSCRIPTION_FILE', filename };
}
export const addAudioFile = filename => {
  return { type: 'ADD_AUDIO_FILE', filename };
}
export const addAdditionalTextFile = filename => {
  console.log("added text file", filename)
  return { type: 'ADD_ADDITIONAL_TEXT_FILE', filename };
}