import * as actionTypes from "../actionTypes/modelActionTypes";

const initState = {
    modelList: [],
    name: "",
    datasetName: "",
    pronDictName: "",
    results: null,
    settings: {
        huggingface_model_name: "facebook/wav2vec2-large-xlsr-53",
    },
    status: "ready",
    stage_status: null,
    log: null,
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
            let log = action.response.data.data.log;

            // pron_dict_name could be null if not using pron dicts
            return {
                ...state,
                name,
                results,
                log,
                status: model_status,
                datasetName: dataset_name,
                engineName: engine_name,
                pronDictName: pron_dict_name,
                settings: settings,
            };
        }

        case actionTypes.MODEL_DELETE_SUCCESS: {
            return {
                ...state,
                modelList: action.response.data.data.list,
                name: action.response.data.data.name,
            };
        }

        case actionTypes.MODEL_LIST_SUCCESS:
            return {
                ...state,
                modelList: action.response.data.data.list,
            };

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
        
        case actionTypes.MODEL_STATUS_FAILURE:
        case actionTypes.MODEL_TRAIN_FAILURE:
            return {...state, status: "error"};
        
        case actionTypes.MODEL_GET_LOG_SUCCESS:
            ({data, status} = action.response.data);
            
            if (status === 200) {
                return {...state, log: data.log};
            }

            return {...state};

        default:
            return {...state};
    }
};

export default model;
