const initialModelState = {
    name: "",
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
}

const apiModelReducer = (state = initialModelState, action) => {
    switch (action.type) {
        case 'UPDATE_MODEL_NAME':
            return {
                ...state, name: action.response.data.name
            }
        case 'UPDATE_MODEL_DATE':
            return {
                ...state
            }
        case 'UPDATE_MODEL_SETTINGS':
            return {
                ...state
            }
        case 'UPDATE_MODEL_TRANSCRIPTION_FILES':
            return {
                ...state
            }
        case 'UPDATE_MODEL_ADDITIONAL_WORD_FILES':
            return {
                ...state
            }
        case 'UPDATE_MODEL_PRONUNCIATION_FILE':
            return {
                ...state
            }
        default:
            return state;
    }
}

export default apiModelReducer;