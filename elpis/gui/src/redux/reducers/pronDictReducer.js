import * as actionTypes from "../actionTypes/pronDictActionTypes";

const initState = {
    pronDictList: [],
    name: "",
    datasetName: "",
    date: null,
    l2s: "",
    lexicon: "",
    apiWaiting: {status: false, message: "something"},
};
const pronDict = (state = initState, action) => {
    // If we want to check status code, use action.response.data
    // so then we need to access the properties at data.xyz etc
    let data, status;

    switch (action.type) {
        case actionTypes.PRON_DICT_NEW_SUCCESS:
            if (action.response.data.status === 500){
                return {...initState,
                    status: action.response.data.status,
                    error: action.response.data.error,
                };
            } else {
                var {name} = action.response.data.data.config;

                return {...initState, name};
            }

        case actionTypes.PRON_DICT_LOAD_SUCCESS:
            var {config, l2s, lexicon} = action.response.data.data;

            if (!config) {
                return {
                    ...state,
                    name: null,
                    datasetName: null,
                };
            }

            return {
                ...state,
                name: config.name,
                datasetName: config.dataset_name,
                l2s,
                lexicon,
            };

        case actionTypes.PRON_DICT_DELETE_SUCCESS:
            return {
                ...state,
                pronDictList: action.response.data.data.list,
                name: action.response.data.data.name,
            };

        case actionTypes.PRON_DICT_LIST_SUCCESS:
            return {
                ...state,
                pronDictList: action.response.data.data.list,
            };

        case actionTypes.PRON_DICT_L2S_SUCCESS:
            ({data, status} = action.response.data);

            if (status === 200) {
                return {...state, l2s: data.l2s};
            } else {
                console.log("some error with l2s");

                return {...state};
            }

        case actionTypes.PRON_DICT_BUILD_LEXICON_SUCCESS:
        case actionTypes.PRON_DICT_SAVE_LEXICON_SUCCESS:
            ({data, status} = action.response.data);

            if (status === 200){
                return {...state, lexicon: data.lexicon};
            } else {
                console.log("some error building or saving lexicon");

                return {...state};
            }

        // This doesn't use the API, just for the form
        // .. could probably use local state
        case actionTypes.PRON_DICT_UPDATE_LEXICON:
            return {...state, lexicon: action.data.lexicon};

        default:
            return {...state};
    }
};

export default pronDict;
