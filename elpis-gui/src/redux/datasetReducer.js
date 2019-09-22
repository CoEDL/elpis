import {getFileExtension} from 'helpers'
import {
    DATASET_NEW_STARTED,
    DATASET_NEW_SUCCESS,
    DATASET_NEW_FAILURE
} from './datasetActionTypes';


let audioFiles
let transcriptionFiles
let additionalTextFiles

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




        case 'DATASET_LIST':
            return {
                ...state,
                datasetList: action.response.data.data
            }

        case DATASET_NEW_STARTED:
            console.log("reducer got ds new started")
            return {...state}

        case DATASET_NEW_SUCCESS:
            console.log("reducer got ds new success")
            return {...state}

        case DATASET_NEW_FAILURE:
            console.log("reducer got ds new fail")
            return {...state}

        case 'DATASET_LOAD':
        case 'DATASET_NEW':
            console.log("reducer got ds new")
            // action.data is an array of filenames. parse this, split into separate lists
            audioFiles = action.response.data.data.files.filter(file => getFileExtension(file) === 'wav')
            transcriptionFiles = action.response.data.data.files.filter(file => getFileExtension(file) === 'eaf')
            additionalTextFiles = action.response.data.data.files.filter(file => getFileExtension(file) === 'txt')
            audioFiles.sort()
            transcriptionFiles.sort()
            additionalTextFiles.sort()
            // remove duplicates
            audioFiles = [...(new Set(audioFiles))];
            transcriptionFiles = [...(new Set(transcriptionFiles))];
            return {
                ...state,
                audioFiles,
                transcriptionFiles,
                additionalTextFiles,
                name: action.response.data.data.name,
                settings: {...state.settings, tier: action.response.data.data.tier}
            }

        case 'DATASET_NAME':
            return {
                ...state,
                name: action.response.data.data.name
            }

        case 'DATASET_FILES':
            // action.data is an array of filenames. parse this, split into separate lists
            audioFiles = action.response.data.filter(file => getFileExtension(file) === 'wav')
            transcriptionFiles = action.response.data.filter(file => getFileExtension(file) === 'eaf')
            additionalTextFiles = action.response.data.filter(file => getFileExtension(file) === 'txt')
            audioFiles.sort()
            transcriptionFiles.sort()
            additionalTextFiles.sort()
            // remove duplicates
            audioFiles = [...(new Set(audioFiles))];

            return {
                ...state,
                status: "files loaded",
                audioFiles,
                transcriptionFiles,
                additionalTextFiles
            }

        case 'DATASET_SETTINGS':
            // watch out for response.data.data ...
            return {
                ...state,
                settings: {...state.settings, tier: action.response.data.data.tier}
            }

        case 'DATASET_PREPARE':
            // TODO do this in the backend
            const data = action.response.data
            const wordlist = Object.keys(data).map(function (key) {
                return ({name:key, frequency: data[key]})
            })
            return {
                ...state,
                wordlist
            }

        case 'DATASET_STATUS':
            return {
                ...state,
                status: action.status
            }
        default:
            return state;
    }
}

export default dataset;