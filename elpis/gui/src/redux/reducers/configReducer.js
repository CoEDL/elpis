import * as actionTypes from "../actionTypes/appActionTypes";

const initState = {
    datasetList: [],
    pronDictList: [],
    modelList: [],
    app_config: { dev_mode: false },
};
const config = (state = initState, action) => {
    switch (action.type) {

        case actionTypes.CONFIG_OBJECT_NAMES_STARTED:
        case actionTypes.CONFIG_OBJECT_NAMES_FAILURE:
            return {...state};

        case actionTypes.CONFIG_OBJECT_NAMES_SUCCESS: {
            let {object_names} = action.response.data.data;
            return {
                ...state,
                datasetList: object_names.datasets,
                pronDictList: object_names.pron_dicts,
                modelList: object_names.models,
            };
        }

        case actionTypes.CONFIG_LIST_SUCCESS: {
            let {config} = action.response.data.data;
            return {...state, app_config: config};
        }

        default:
            return { ...state };
    }
};

export default config;
