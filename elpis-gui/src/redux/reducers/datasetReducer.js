import {getFileExtension} from 'helpers'
import * as actionTypes from '../actionTypes/datasetActionTypes';

const initState = {
    name: "",
    status: "",
    datasetList: [],
    audioFiles: [],
    transcriptionFiles: [],
    additionalTextFiles: [],
    settings: {
        tier: 'Phrase'
    },
    wordlist: {}
}


const dataset = (state = initState, action) => {
    switch (action.type) {

        // Boilerplate for all...
        case actionTypes.DATASET_NEW_STARTED:
            return {...state}

        case actionTypes.DATASET_NEW_FAILURE:
            return {...state}

        case actionTypes.DATASET_NEW_SUCCESS:
            var { name } = action.response.data.data
            return { ...initState, name }

        case actionTypes.DATASET_LOAD_SUCCESS:
            // loading existing data set might have files and settings
            var { name, tier, files } = action.response.data.data
            // action.data is an array of filenames. parse this, split into separate lists
            var audioFiles = files.filter(file => getFileExtension(file) === 'wav').sort()
            var transcriptionFiles = files.filter(file => getFileExtension(file) === 'eaf').sort()
            var additionalTextFiles = files.filter(file => getFileExtension(file) === 'txt').sort()
            // remove duplicates (should do this on the server though!)
            audioFiles = [...(new Set(audioFiles))];
            transcriptionFiles = [...(new Set(transcriptionFiles))];
            return {
                ...state,
                name,
                status: "",
                audioFiles,
                transcriptionFiles,
                additionalTextFiles,
                settings: { ...state.settings, tier },
                tier: "",
                wordlist: "",
            }


        case actionTypes.DATASET_LIST_SUCCESS:
            return {
                ...state,
                datasetList: action.response.data.data
            }

        case actionTypes.DATASET_FILES_STARTED:
            return { ...state, status: "loading" }

        case actionTypes.DATASET_FILES_SUCCESS:
            var { data } = action.response
            // action.data is an array of filenames. parse this, split into separate lists
            var audioFiles = data.filter(file => getFileExtension(file) === 'wav').sort()
            var transcriptionFiles = data.filter(file => getFileExtension(file) === 'eaf').sort()
            var additionalTextFiles = data.filter(file => getFileExtension(file) === 'txt').sort()
            // remove duplicates
            audioFiles = [...(new Set(audioFiles))];
            return {
                ...state,
                status: "done",
                audioFiles,
                transcriptionFiles,
                additionalTextFiles
            }

        case actionTypes.DATASET_SETTINGS:
            console.log(action.response)
            var { tier } = action.response.data.data
            return {
                ...state,
                settings: {...state.settings, tier}
            }

        case actionTypes.DATASET_PREPARE_SUCCESS:
            // TODO do this in the backend
            var data = action.response.data
            let wordlist = Object.keys(data).map(function (key) {
                return ({name:key, frequency: data[key]})
            })
            return { ...state, wordlist }

        default:
            return state;
    }
}

export default dataset;