import * as actionTypes from "../actionTypes/modelActionTypes";

const initState = {
    modelList: [],
    name: "",
    datasetName: "",
    pronDictName: "",
    results: null,
    settings: {},
    status: "ready",
    stage_status: null,
};
const model = (state = initState, action) => {
    let data, status;

    switch (action.type) {
        case actionTypes.MODEL_NEW_SUCCESS:
            if (action.response.data.status === 500){
                return {...initState,
                    status: action.response.data.status,
                    error: action.response.data.error,
                };
            } else {
                const {name, dataset_name, pron_dict_name, settings} = action.response.data.data.config;

                console.log("model reducer new success");
                console.log(settings);

                // pron_dict_name could be null if not using pron dicts
                return {
                    ...initState,
                    name,
                    settings,
                    datasetName: dataset_name,
                    pronDictName: pron_dict_name,
                };
            }
        case actionTypes.MODEL_LOAD_SUCCESS: {
            var {name, dataset_name, engine_name, pron_dict_name, settings, results} = action.response.data.data.config;
            let model_status = action.response.data.data.config;

            console.log("model reducer load success");
            console.log(settings);

            // pron_dict_name could be null if not using pron dicts
            return {
                ...state,
                name,
                results,
                status: model_status,
                datasetName: dataset_name,
                engineName: engine_name,
                pronDictName: pron_dict_name,
                settings: settings,
            };
        }
        case actionTypes.MODEL_LIST_SUCCESS:
            var {list} = action.response.data.data;

            return {...state, modelList: list};
        case actionTypes.MODEL_SETTINGS_SUCCESS:
            ({data, status} = action.response.data);
            console.log("model reducer settings success");
            console.log(data, status);

            if (status === 200) {
                return {...state, settings: data.settings};
            } else {
                console.log(data);

                return {...state};
            }
        case actionTypes.MODEL_TRAIN_SUCCESS:
            ({data, status} = action.response.data);

            if (status === 200) {
                return {...state, status: data.status};
            } else {
                console.log(data);

                return {...state};
            }
        case actionTypes.MODEL_STATUS_SUCCESS:
            ({data, status} = action.response.data);

            if (status === 200) {
                return {...state, status: data.status, stage_status: data.stage_status};
            } else {
                console.log(data);

                return {...state};
            }
        case actionTypes.MODEL_RESULTS_SUCCESS:
            ({data, status} = action.response.data);
            console.log(data, status);

            if (status === 200) {
                return {...state, results: data.results};
            } else {
                console.log(data);

                return {...state};
            }
        default:
            return {...state};
    }
};

export default model;
