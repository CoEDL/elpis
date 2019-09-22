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

        case 'TRIGGER_API_WAITING':
            return {
                ...state,
                apiWaiting: {status: true, message: action.message}
            }

        case 'PRON_DICT_LIST':
            return {
                ...state,
                pronDictList: action.response.data.data
            }


        case 'PRON_DICT_LOAD':
            return {
                ...state,
                name: action.response.data.data.config.name,
                datasetName: action.response.data.data.config.dataset_name,
                l2s: action.response.data.data.l2s,
                lexicon: action.response.data.data.lexicon,
            }

        case 'PRON_DICT_L2S':
            return {
                ...state,
                l2s: action.response.data
            }

        case 'PRON_DICT_LEXICON':
            return {
                ...state,
                lexicon: action.response.data
            }

        case 'PRON_DICT_SAVE_LEXICON':
            return {
                ...state,
                lexicon: action.response.data
            }
        case 'TEST_UPDATE_LEXICON':
            return {
                ...state,
                lexicon: action.data.lexicon
            }

        default:
            return state;
    }
}

export default pronDict;