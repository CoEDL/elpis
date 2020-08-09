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
    status: 'ready',
    stage_status: null
}

const model = (state = initState, action) => {
    switch (action.type) {

        case actionTypes.MODEL_NEW_SUCCESS:
            if (action.response.data.status==500){
                return { ...initState,
                    status: action.response.data.status,
                    error: action.response.data.error
                }
            } else {
                const {name, dataset_name, pron_dict_name} = action.response.data.data.config
                return {
                    ...initState,
                    name,
                    datasetName: dataset_name,
                    pronDictName: pron_dict_name
                }
            }

        case actionTypes.MODEL_LOAD_SUCCESS:
            var { config } = action.response.data.data.config
            return {
                ...state,
                name: config.name,
                datasetName: config.dataset_name,
                pronDictName: config.pron_dict_name,
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
            var { data, status } = action.response.data
            if (status == 200) {
                return { ...state, status: data.status }
            } else {
                console.log(data)
                return { ...state }
            }

        case actionTypes.MODEL_STATUS_SUCCESS:
            var { data, status } = action.response.data
            if (status == 200) {
                return { ...state, status: data.status, stage_status: data.stage_status }
            } else {
                console.log(data)
                return { ...state }
            }

        case actionTypes.MODEL_RESULTS_SUCCESS:
            var { data, status } = action.response.data
            if (status == 200) {
                return { ...state, results: data.results }
            } else {
                console.log(data)
                return { ...state }
            }


        default:
            return { ...state }
    }
}

export default model;