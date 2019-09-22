import {getFileExtension} from 'helpers'
import {
    DATASET_NEW_STARTED,
    DATASET_NEW_SUCCESS,
    DATASET_NEW_FAILURE,
    DATASET_LOAD_SUCCESS,
    DATASET_LIST_SUCCESS,
    DATASET_FILES_STARTED,
    DATASET_FILES_SUCCESS,
} from '../types/datasetActionTypes';


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
        case DATASET_NEW_STARTED:
            return {...state}

        case DATASET_NEW_FAILURE:
            return {...state}

        case DATASET_NEW_SUCCESS:
            // all we should need at this stage is the name
            console.log("reducer got ds new success", action)
            var { name, tier, files } = action.payload.data.data
            return { ...state, name }

        case DATASET_LOAD_SUCCESS:
            // loading existing data set might have files and settings
            var { name, tier, files } = action.payload.data.data
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
                audioFiles,
                transcriptionFiles,
                additionalTextFiles,
                settings: { ...state.settings, tier }
            }

        case DATASET_LIST_SUCCESS:
            return {
                ...state,
                datasetList: action.payload.data.data
            }

        case DATASET_FILES_STARTED:
            return { ...state, status: "loading" }


        case DATASET_FILES_SUCCESS:
            var { data } = action.payload
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

        case 'DATASET_SETTINGS':
            var { tier } = action.response.data.data
            return {
                ...state,
                settings: {...state.settings, tier}
            }

        case 'DATASET_PREPARE':
            // TODO do this in the backend
            var data = action.response.data
            let wordlist = Object.keys(data).map(function (key) {
                return ({name:key, frequency: data[key]})
            })
            return {
                ...state,
                wordlist
            }

        default:
            return state;
    }
}

export default dataset;