import {getFileExtension} from 'helpers'
import * as actionTypes from '../actionTypes/datasetActionTypes';

const initState = {
    name: "",
    importer_name: "",
    status: "",
    datasetList: [],
    audioFiles: [],
    transcriptionFiles: [],
    additionalTextFiles: [],
    settings: null,
    ui: null,
    punctuation_to_explode_by: "",
    punctuation_to_collapsed_by: "",
    wordlist: {}
}


const dataset = (state = initState, action) => {
    switch (action.type) {

        // Boilerplate for all...
        case actionTypes.DATASET_NEW_STARTED:
        case actionTypes.DATASET_NEW_FAILURE:
            return {...state}

        case actionTypes.DATASET_NEW_SUCCESS: {
            let dataset_state = action.response.data.data.state;

            let name = dataset_state.name;
            let punctuation_to_explode_by = dataset_state.punctuation_to_explode_by;

            let importer_name = null;
            let settings = null;
            let ui = null;
            
            if (dataset_state.importer !== null) {
                name =     dataset_state.importer.name;
                settings = dataset_state.importer.settings;
                ui =       dataset_state.importer.ui;
            }

            console.log("DATASET_NEW_SUCCESS name", name)
            return { ...initState,
                name,
                importer_name,
                settings,
                ui,
                punctuation_to_explode_by}
        }

        case actionTypes.DATASET_LOAD_SUCCESS: {
            // loading existing data set might have files and settings
            let dataset_state = action.response.data.data.state
            let {
                name,
                files,
                settings,
                ui,
                punctuation_to_explode_by
            } = dataset_state
            // action.data is an array of filenames. parse this, split into separate lists
            var audioFiles = files.filter(file => getFileExtension(file) === 'wav').sort()
            var additionalTextFiles = files.filter(file => getFileExtension(file) === 'txt').sort()
            var transcriptionFiles = files.filter(file => {
                return (getFileExtension(file) !== 'wav' && getFileExtension(file) !== 'txt')
            }).sort()
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
                settings,
                ui,
                punctuation_to_explode_by,
                wordlist: "",
            }
        }

        case actionTypes.DATASET_LIST_SUCCESS:
            return {
                ...state,
                datasetList: action.response.data.data.list
            }

        case actionTypes.DATASET_FILES_STARTED:
            return { ...state, status: "loading" }

        case actionTypes.DATASET_FILES_SUCCESS:
            // TODO, API should send a JSON wrapper
            var { data, status } = action.response.data
            if (status === 200) {
                // action.data is an array of filenames. parse this, split into separate lists
                var audioFiles = data.files.filter(file => getFileExtension(file) === 'wav').sort()
                var transcriptionFiles = data.files.filter(file => getFileExtension(file) === 'eaf').sort()
                var additionalTextFiles = data.files.filter(file => getFileExtension(file) === 'txt').sort()
                // remove duplicates
                audioFiles = [...(new Set(audioFiles))];
                return {
                    ...state,
                    status: "loaded",
                    audioFiles,
                    transcriptionFiles,
                    additionalTextFiles,
                    settings: data.settings,
                    ui: data.ui,
                    importer_name: data.importer_name
                }
            } else {
                console.log(data)
                return { ...state, status: 'ready' }
            }

        case actionTypes.DATASET_SETTINGS_SUCCESS:
            var { data, status } = action.response.data
            if (status === 200) {
                return {
                    ...state,
                    settings: { ...state.settings, ...data.settings }
                }
            } else {
                console.log(data)
                return { ...state }
            }
        
        case actionTypes.DATASET_UI_UPDATE_SUCCESS:
            var { data, status } = action.response.data
            if (status == 200) {
                return {
                    ...state,
                    ui: data.ui
                }
            }

        case actionTypes.DATASET_PREPARE_SUCCESS:
            var { data, status } = action.response.data
            if (status === 200) {
                // First decode the text we receive from the API
                const wordlistObj = JSON.parse(data.wordlist)
                const wordlist = Object.keys(wordlistObj).map( key => {
                    return ({ name: key, frequency: wordlistObj[key] })
                })
                if (wordlist.length > 0) return { ...state, wordlist }
                else return { ...state }
            } else {
                // Errors are formatted as { status: code, data: message }
                console.log( data )
                return { ...state }
            }

        default:
            return { ...state }
    }
}

export default dataset;