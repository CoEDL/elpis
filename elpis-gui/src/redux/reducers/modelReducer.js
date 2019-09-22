import * as actionTypes from '../actionTypes/modelActionTypes';

const initState = {
    modelList: [],
    name: '',
    datasetName: '',
    pronDictName: '',
    date: null,
    l2s: '',
    lexicon: '',
    results: null,
    settings: {
        ngram: 1
    },
    status: 'ready',
    apiWaiting: {status: false, message: 'something'}
}

const model = (state = initState, action) => {
    switch (action.type) {

        case actionTypes.MODEL_NEW_SUCCESS:
            var { name } = action.payload.data.data.config
            return { ...initState, name }

        case actionTypes.MODEL_LOAD_SUCCESS:
            var { config, l2s } = action.payload.data.data
            return {
                ...state,
                name: config.name,
                l2s,
                status: 'ready',
                lexicon: 'No lexicon yet',
                datasetName: config.dataset_name,
                pronDictName: config.pron_dict_name,
                settings: {...state.settings, ngram: config.ngram}
            }

        case actionTypes.MODEL_LIST_SUCCESS:
            return {
                ...state,
                modelList: action.payload.data.data
            }

        case actionTypes.MODEL_SETTINGS_SUCCESS:
            return {
                ...state,
                settings: action.payload.data.data
            }

        case actionTypes.MODEL_TRAIN_SUCCESS:
            return {
                ...state,
                status: action.payload.data.data
            }


        case actionTypes.MODEL_STATUS_SUCCESS:
            return {
                ...state,
                status: action.payload.data.data
            }

        case 'MODEL_RESULTS':
            return {
                ...state,
                results: action.response.data.data
            }
        default:
            return state;
    }
}

export default model;