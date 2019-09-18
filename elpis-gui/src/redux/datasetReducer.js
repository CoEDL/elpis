import {getFileExtension} from 'helpers'

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

        // When we change models, we need to reset the current dataset
        case 'MODEL_LOAD':
        case 'MODEL_NEW':
            console.log("data set reducer got MODEL_LOAD", action.response.data.data.config.dataset_name)
            return {
                ...state,
                name: action.response.data.data.config.dataset_name
            }

        case 'DATASET_LIST':
            return {
                ...state,
                datasetList: action.response.data.data
            }

        case 'DATASET_LOAD':
        case 'DATASET_NEW':
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
            // console.log("wordlist", action.response.data)
            // change the format of wordlist for better UI display
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