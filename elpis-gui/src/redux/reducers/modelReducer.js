import * as actionTypes from '../actionTypes/modelActionTypes';

const initState = {
    modelList: [],
    name: '',
    datasetName: '',
    pronDictName: '',
    results: null,
    settings: {
        ngram: 1
    },
    status: 'ready'
}

const model = (state = initState, action) => {
    switch (action.type) {

        case actionTypes.MODEL_NEW_SUCCESS:
            var { name } = action.response.data.data.config
            return { ...initState, name }

        case actionTypes.MODEL_LOAD_SUCCESS:
            var { config } = action.response.data.data
            return {
                ...initState,
                name: config.name,
                datasetName: config.dataset_name,
                pronDictName: config.pron_dict_name,
                settings: {...state.settings, ngram: config.ngram},
                // TODO load the results too
            }

        case actionTypes.MODEL_LIST_SUCCESS:
            var { list } = action.response.data.data
            return { ...state, modelList: list }

        case actionTypes.MODEL_SETTINGS_SUCCESS:
            var { settings } = action.response.data.data
            return { ...state, settings }

        case actionTypes.MODEL_TRAIN_SUCCESS:
            var { status } = action.response.data.data
            return { ...state, status }

        case actionTypes.MODEL_STATUS_SUCCESS:
            var { status } = action.response.data.data
            return { ...state, status }

        case actionTypes.MODEL_RESULTS_SUCCESS:
            var { results } = action.response.data.data
            return { ...state, results }

        default:
            return { ...state }
    }
}

export default model;