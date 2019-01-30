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
  return { type: 'ADD_ADDITIONAL_TEXT_FILE', filename };
}

