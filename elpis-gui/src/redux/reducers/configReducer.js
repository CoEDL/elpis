import * as actionTypes from '../actionTypes/appActionTypes';

const initState = {
    datasetList: [],
    pronDictList: [],
    modelList: []
}
const config = (state = initState, action) => {
    switch (action.type) {

        case actionTypes.CONFIG_OBJECT_NAMES_STARTED:
        case actionTypes.CONFIG_OBJECT_NAMES_FAILURE:
            return {...state};

        case actionTypes.CONFIG_OBJECT_NAMES_SUCCESS:
            const { object_names } = action.response.data.data
            return {...state,
                datasetList:  object_names.datasets,
                pronDictList: object_names.pron_dicts,
                modelList:    object_names.models
            };

        default:
            return { ...state }
    }
}

export default config;