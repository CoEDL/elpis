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
            var { config, results } = action.response.data.data
            return { ...initState, name: config.name }

        case actionTypes.MODEL_LOAD_SUCCESS:
            var { config } = action.response.data.data
            return {
                ...state,
                name: config.name,
                datasetName: config.dataset_name,
                pronDictName: config.pron_dict_name,
                results,
                settings: {...state.settings, ngram: config.ngram},
                status: 'ready'
            }

        case actionTypes.MODEL_LIST_SUCCESS:
            var { list } = action.response.data.data
            return { ...state, modelList: list }

        case actionTypes.MODEL_SETTINGS_SUCCESS:
            var { data, status } = action.response.data
            if (status == 200) {
                return { ...state, settings:data.settings }
            } else {
                console.log(data)
                return { ...state }
            }

        // crazy, there will be three layers of objects with status properties here!
        case actionTypes.MODEL_TRAIN_SUCCESS:
        case actionTypes.MODEL_STATUS_SUCCESS:
            var { data, status } = action.response.data
            if (status == 200) {
                return { ...state, status: data.status }
            } else {
                console.log(data)
                return { ...state }
            }

        case actionTypes.MODEL_RESULTS_SUCCESS:
            var { data, status } = action.response.data
            if (status == 200) {
                return { ...state, results:data.results }
            } else {
                console.log(data)
                return { ...state }
            }

        default:
            return { ...state }
    }
}

export default model;