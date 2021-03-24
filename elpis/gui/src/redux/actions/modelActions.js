import axios from "axios";
import urls from "urls";
import * as actionTypes from "../actionTypes/modelActionTypes";

const baseUrl = (process.env.REACT_APP_BASEURL) ?
    process.env.REACT_APP_BASEURL :
    "http://" + window.location.host;


/* * * * * * * * * * * *  NEW * * * * * * * * * * *  */

export function modelNew(postData) {
    const url = baseUrl + urls.api.model.new;
    var responseData;

    return async dispatch => {
        dispatch(modelNewStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(modelNewSuccess(response));
            })
            .catch(error => {
                dispatch(modelNewFailure(error));
                throw error;
            });

        return responseData;
    };
}

const modelNewStarted = () => ({
    type: actionTypes.MODEL_NEW_STARTED,
});
const modelNewSuccess = response => ({
    type: actionTypes.MODEL_NEW_SUCCESS,
    response: {...response},
});
const modelNewFailure = error => ({
    type: actionTypes.MODEL_NEW_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  LOAD * * * * * * * * * * *  */

export function modelLoad(postData) {
    const url = baseUrl + urls.api.model.load;
    var responseData;

    return async dispatch => {
        dispatch(modelLoadStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(modelLoadSuccess(response));
            })
            .catch(error => {
                dispatch(modelLoadFailure(error));
                throw error;
            });

        return responseData;
    };
}

const modelLoadStarted = () => ({
    type: actionTypes.MODEL_LOAD_STARTED,
});
const modelLoadSuccess = response => ({
    type: actionTypes.MODEL_LOAD_SUCCESS,
    response: {...response},
});
const modelLoadFailure = error => ({
    type: actionTypes.MODEL_LOAD_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  LIST * * * * * * * * * * *  */

export function modelList() {
    const url = baseUrl + urls.api.model.list;
    var responseData;

    return async dispatch => {
        dispatch(modelListStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(modelListSuccess(response));
            })
            .catch(error => {
                dispatch(modelListFailure(error));
                throw error;
            });

        return responseData;
    };
}

const modelListStarted = () => ({
    type: actionTypes.MODEL_LIST_STARTED,
});
const modelListSuccess = response => ({
    type: actionTypes.MODEL_LIST_SUCCESS,
    response: {...response},
});
const modelListFailure = error => ({
    type: actionTypes.MODEL_LIST_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  SETTINGS * * * * * * * * * * *  */

export function modelSettings(postData) {
    const url = baseUrl + urls.api.model.settings;
    var responseData;

    return async dispatch => {
        dispatch(modelSettingsStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(modelSettingsSuccess(response));
            })
            .catch(error => {
                dispatch(modelSettingsFailure(error));
                throw error;
            });

        return responseData;
    };
}

const modelSettingsStarted = () => ({
    type: actionTypes.MODEL_SETTINGS_STARTED,
});
const modelSettingsSuccess = response => ({
    type: actionTypes.MODEL_SETTINGS_SUCCESS,
    response: {...response},
});
const modelSettingsFailure = error => ({
    type: actionTypes.MODEL_SETTINGS_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  TRAIN * * * * * * * * * * *  */

export function modelTrain() {
    const url = baseUrl + urls.api.model.train;
    var responseData;

    return async dispatch => {
        dispatch(modelTrainStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(modelTrainSuccess(response));
            })
            .catch(error => {
                dispatch(modelTrainFailure(error));
                throw error;
            });

        return responseData;
    };
}

const modelTrainStarted = () => ({
    type: actionTypes.MODEL_TRAIN_STARTED,
});
const modelTrainSuccess = response => ({
    type: actionTypes.MODEL_TRAIN_SUCCESS,
    response: {...response},
});
const modelTrainFailure = error => ({
    type: actionTypes.MODEL_TRAIN_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  STATUS * * * * * * * * * * *  */

export function modelStatus() {
    const url = baseUrl + urls.api.model.status;
    var responseData;

    return async dispatch => {
        dispatch(modelStatusStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(modelStatusSuccess(response));
            })
            .catch(error => {
                dispatch(modelStatusFailure(error));
                throw error;
            });

        return responseData;
    };
}

const modelStatusStarted = () => ({
    type: actionTypes.MODEL_STATUS_STARTED,
});
const modelStatusSuccess = response => ({
    type: actionTypes.MODEL_STATUS_SUCCESS,
    response: {...response},
});
const modelStatusFailure = error => ({
    type: actionTypes.MODEL_STATUS_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  RESULTS * * * * * * * * * * *  */

export function modelResults() {
    const url = baseUrl + urls.api.model.results;
    var responseData;

    return async dispatch => {
        dispatch(modelResultsStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(modelResultsSuccess(response));
            })
            .catch(error => {
                dispatch(modelResultsFailure(error));
                throw error;
            });

        return responseData;
    };
}

const modelResultsStarted = () => ({
    type: actionTypes.MODEL_RESULTS_STARTED,
});
const modelResultsSuccess = response => ({
    type: actionTypes.MODEL_RESULTS_SUCCESS,
    response: {...response},
});
const modelResultsFailure = error => ({
    type: actionTypes.MODEL_RESULTS_FAILURE,
    response: {error},
});
