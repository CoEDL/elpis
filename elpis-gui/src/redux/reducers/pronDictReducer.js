import * as actionTypes from '../actionTypes/pronDictActionTypes';

const initState = {
    pronDictList: [],
    name: '',
    datasetName: '',
    date: null,
    l2s: '',
    lexicon: '',
    apiWaiting: {status: false, message: 'something'}
}

const pronDict = (state = initState, action) => {
    switch (action.type) {

        case actionTypes.PRON_DICT_NEW_SUCCESS:
            return {
                ...initState,
                name: action.payload.data.data.config.name
            }

        case actionTypes.PRON_DICT_LOAD_SUCCESS:
            var { config, datasetName, l2s, lexicon } = action.payload.data.data
            return {
                ...state,
                name: config.name,
                datasetName: config.dataset_name,
                l2s,
                lexicon
            }

        case actionTypes.PRON_DICT_LIST_SUCCESS:
            return {
                ...state,
                pronDictList: action.payload.data.data
            }


        case actionTypes.PRON_DICT_L2S_SUCCESS:
            return {
                ...state,
                l2s: action.payload.data
            }

        case actionTypes.PRON_DICT_BUILD_LEXICON_SUCCESS:
            return {
                ...state,
                lexicon: action.payload.data
            }

        case actionTypes.PRON_DICT_SAVE_LEXICON:
            return {
                ...state,
                lexicon: action.payload.data
            }

        case actionTypes.PRON_DICT_UPDATE_LEXICON:
            return {
                ...state,
                lexicon: action.data.lexicon
            }


        default:
            return state;
    }
}

export default pronDict;