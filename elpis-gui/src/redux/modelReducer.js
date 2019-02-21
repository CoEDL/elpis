import {getFileExtension} from 'helpers'

const initState = {
    name: "",
    modelNames: [],
    date: null,
    pronunciationFile: '',
    settings: {
        ngram: 1
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

        case 'MODEL_LIST':
        console.log("reducer got model names", action.response.data)
            return {
                ...state,
                modelNames: action.response.data.data
            }

        case 'MODEL_NEW':
            console.log("reducer got model new", action.response.data)
            return {
                ...state,
                name: action.response.data.data.name
            }

        case 'MODEL_NAME':
        console.log("reducer got model name", action.response.data)
        return {
                ...state,
                name: action.response.data.data.name
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