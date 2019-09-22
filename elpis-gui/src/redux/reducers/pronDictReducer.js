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




        case 'TRIGGER_API_WAITING':
            return {
                ...state,
                apiWaiting: {status: true, message: action.message}
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