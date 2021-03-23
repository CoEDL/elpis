import {getFileExtension} from '../../helpers';
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
    wordlist: {},
    error: '',
};

let audioFiles = [];
let additionalTextFiles = [];
let transcriptionFiles = [];

const dataset = (state = initState, action) => {
    switch (action.type) {

        // Boilerplate for all...
        case actionTypes.DATASET_NEW_STARTED:
        case actionTypes.DATASET_NEW_FAILURE:
            return {...state};

        case actionTypes.DATASET_NEW_SUCCESS: {
            if (action.response.data.status==500){
                return { ...initState,
                    status: action.response.data.status,
                    error: action.response.data.error,
                };
            } else {
                let dataset_state = action.response.data.data.state;
                let name = dataset_state.name;
                return { ...initState, name };
            }
        }

        case actionTypes.DATASET_LOAD_SUCCESS: {
            // loading existing data set might have files and settings
            let {name, files, importer} = action.response.data.data.state;
            let wordlist = {};
            if (action.response.data.data.wordlist) {
                const wordlistObj = JSON.parse(action.response.data.data.wordlist);
                wordlist = Object.keys(wordlistObj).map( key => {
                    return ({ name: key, frequency: wordlistObj[key] });
                });
            }
           const status = wordlist.length > 0 ? 'wordlist-prepared' : '';
            // action.data is an array of filenames. parse this, split into separate lists
            audioFiles = files.filter(file => getFileExtension(file) === 'wav').sort();
            additionalTextFiles = files.filter(file => getFileExtension(file) === 'txt').sort();
            transcriptionFiles = files.filter(file => {
                return (getFileExtension(file) !== 'wav' && getFileExtension(file) !== 'txt');
            }).sort();
            // remove duplicates
            audioFiles = [...(new Set(audioFiles))];
            transcriptionFiles = [...(new Set(transcriptionFiles))];
            return {
                ...state,
                name,
                status,
                audioFiles,
                transcriptionFiles,
                additionalTextFiles,
                importer_name: importer.name,
                settings: importer.settings,
                ui: importer.ui,
                wordlist,
            };
        }

        case actionTypes.DATASET_LIST_SUCCESS:
            return {
                ...state,
                datasetList: action.response.data.data.list,
            };

        case actionTypes.DATASET_FILES_STARTED:
            return { ...state, status: "loading" };

        case actionTypes.DATASET_FILES_SUCCESS:
            // TODO, API should send a JSON wrapper
            var { data, status } = action.response.data;
            if (status === 200) {
                // action.data is an array of filenames. parse this, split into separate lists
                audioFiles = data.files.filter(file => getFileExtension(file) === 'wav').sort();
                transcriptionFiles = data.files.filter(file => getFileExtension(file) === 'eaf').sort();
                additionalTextFiles = data.files.filter(file => getFileExtension(file) === 'txt').sort();
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
                    importer_name: data.importer_name,
                };
            } else {
                return { ...state, status: 'ready' };
            }

        case actionTypes.DATASET_DELETE_SUCCESS:
            var { data, status } = action.response.data;
            if (status == 200) {
                // action.data is an array of filenames. parse this, split into separate lists
                audioFiles = data.files.filter(file => getFileExtension(file) === 'wav').sort();
                transcriptionFiles = data.files.filter(file => getFileExtension(file) === 'eaf').sort();
                additionalTextFiles = data.files.filter(file => getFileExtension(file) === 'txt').sort();
                return {
                    ...state,
                    audioFiles,
                    transcriptionFiles,
                    additionalTextFiles,
                };
            }

        case actionTypes.DATASET_SETTINGS_SUCCESS:
            var { data, status } = action.response.data;
            if (status === 200) {
                return {
                    ...state,
                    settings: { ...state.settings, ...data.settings },
                };
            } else {
                console.log(data);
                return { ...state };
            }

        case actionTypes.DATASET_UI_UPDATE_SUCCESS:
            var { data, status } = action.response.data;
            if (status == 200) {
                return {...state, ui: data.ui};
            }

        case actionTypes.DATASET_PREPARE_SUCCESS:
            var { data, status } = action.response.data;
            if (status === 200) {
                // First decode the text we receive from the API
                const wordlistObj = JSON.parse(data.wordlist);
                const wordlist = Object.keys(wordlistObj).map( key => {
                    return ({ name: key, frequency: wordlistObj[key] });
                });
                if (wordlist.length > 0) return { ...state, wordlist, status: "wordlist-prepared"};
                else return { ...state };
            } else {
                // Errors are formatted as { status: code, data: message }
                console.log( data );
                return { ...state };
            }



        default:
            return { ...state };
    }
};

export default dataset;
