import {getFileExtension} from 'helpers'

const initState = {
    name: "",
    date: null,
    pronunciationFile: '',
    settings: {
        frequency: 44100,
        mfcc: 22050,
        ngram: 1,
        beam: 10
    },
    apiWaiting: {status: false, message: 'something'}
}

const model = (state = initState, action) => {
    switch (action.type) {

        case 'TRIGGER_API_WAITING':
            return {
                ...state,
                apiWaiting: {status: true, message: action.message}
            }

        case 'MODEL_NEW':
            // get an id back from response?
            return {
                ...state,
            }

        case 'MODEL_NAME':
            return {
                ...state, name: action.response.data.name
            }

        case 'MODEL_DATE':
            // not done yet
            return {
                ...state
            }

        case 'MODEL_PRONUNCIATION_FILE':
            return {
                ...state,
                pronunciationFile: action.response.data
            }

        case 'MODEL_SETTINGS':
            return {
                ...state,
                settings: action.response.data
            }

        default:
            return state;
    }
}

export default model;