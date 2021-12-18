import axios from "axios";
import urls from "urls";
import * as actionTypes from "../actionTypes/datasetActionTypes";

const baseUrl = (process.env.REACT_APP_BASEURL) ?
    process.env.REACT_APP_BASEURL :
    "http://" + window.location.host;


/* * * * * * * * * * * *  NEW * * * * * * * * * * *  */

export function datasetNew(postData) {
    const url = baseUrl + urls.api.dataset.new;
    var responseData;

    return async dispatch => {
        dispatch(datasetNewStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(datasetNewSuccess(response));
            })
            .catch(error => {
                dispatch(datasetNewFailure(error));
                throw error;
            });

        return responseData;
    };
}

const datasetNewStarted = () => ({
    type: actionTypes.DATASET_NEW_STARTED,
});
const datasetNewSuccess = response => ({
    type: actionTypes.DATASET_NEW_SUCCESS,
    response: {...response},
});
const datasetNewFailure = error => ({
    type: actionTypes.DATASET_NEW_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  LOAD * * * * * * * * * * *  */

export function datasetLoad(postData) {
    const url = baseUrl + urls.api.dataset.load;
    var responseData;

    return async dispatch => {
        dispatch(datasetLoadStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(datasetLoadSuccess(response));
            })
            .catch(error => {
                dispatch(datasetLoadFailure(error));
                throw error;
            });

        return responseData;
    };
}

const datasetLoadStarted = () => ({
    type: actionTypes.DATASET_LOAD_STARTED,
});
const datasetLoadSuccess = response => ({
    type: actionTypes.DATASET_LOAD_SUCCESS,
    response: {...response},
});
const datasetLoadFailure = error => ({
    type: actionTypes.DATASET_LOAD_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  LIST * * * * * * * * * * *  */

export function datasetList() {
    const url = baseUrl + urls.api.dataset.list;
    var responseData;

    return async dispatch => {
        dispatch(datasetListStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(datasetListSuccess(response));
            })
            .catch(error => {
                dispatch(datasetListFailure(error));
                throw error;
        });

        return responseData;
    };
}

const datasetListStarted = () => ({
    type: actionTypes.DATASET_LIST_STARTED,
});
const datasetListSuccess = response => ({
    type: actionTypes.DATASET_LIST_SUCCESS,
    response: {...response},
});
const datasetListFailure = error => ({
    type: actionTypes.DATASET_LIST_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  FILES * * * * * * * * * * *  */

export function datasetFiles(postData) {
    const url = baseUrl + urls.api.dataset.files;
    const config = {headers: {"content-type": "multipart/form-data"}};
    var responseData;

    return async dispatch => {
        dispatch(datasetFilesStarted());
        await axios.post(url, postData, config)
            .then(response => {
                responseData = response.data;
                dispatch(datasetFilesSuccess(response));
            })
            // .then((res) => {
            //     dispatch(datasetUIUpdate())
            // })
            .catch(error => {
                dispatch(datasetFilesFailure(error));
                throw error;
            });

        return responseData;
    };
}

const datasetFilesStarted = () => ({
    type: actionTypes.DATASET_FILES_STARTED,
});
const datasetFilesSuccess = response => ({
    type: actionTypes.DATASET_FILES_SUCCESS,
    response: {...response},
});
const datasetFilesFailure = error => ({
    type: actionTypes.DATASET_FILES_FAILURE,
    response: {error},
});

/* * * * * * * * * * * *  FILES DELETE * * * * * * * * * * *  */

export function datasetFilesDelete(postData) {
    const url = baseUrl + urls.api.dataset.filesDelete;
    const config = {headers: {"content-type": "multipart/form-data"}};
    var responseData;

    return async dispatch => {
        dispatch(datasetFilesDeleteStarted());
        await axios.post(url, postData, config)
            .then(response => {
                responseData = response.data;
                dispatch(datasetFilesDeleteSuccess(response));
            })
            .catch(error => {
                dispatch(datasetFilesDeleteFailure(error));
                throw error;
            });
        console.log(responseData["data"]);

        return responseData;
    };
}

const datasetFilesDeleteStarted = () => ({
    type: actionTypes.DATASET_DELETE_STARTED,
});
const datasetFilesDeleteSuccess = response => ({
    type: actionTypes.DATASET_DELETE_SUCCESS,
    response: {...response},
});
const datasetFilesDeleteFailure = error => ({
    type: actionTypes.DATASET_DELETE_FAILURE,
    response: {error},
});

/* * * * * * * * * * * *  SETTINGS * * * * * * * * * * *  */

export function datasetSettings(postData) {
    const url = baseUrl + urls.api.dataset.settings;
    var responseData;

    return async dispatch => {
        dispatch(datasetSettingsStarted());
        await axios.post(url, postData)
            .then(response => {
                responseData = response.data;
                dispatch(datasetSettingsSuccess(response));
            })
            .catch(error => {
                dispatch(datasetSettingsFailure(error));
                throw error;
            });

        return responseData;
    };
}

const datasetSettingsStarted = () => ({
    type: actionTypes.DATASET_SETTINGS_STARTED,
});
const datasetSettingsSuccess = response => ({
    type: actionTypes.DATASET_SETTINGS_SUCCESS,
    response: {...response},
});
const datasetSettingsFailure = error => ({
    type: actionTypes.DATASET_SETTINGS_FAILURE,
    response: {error},
});


/* * * * * * * * * * * *  PREPARE * * * * * * * * * * *  */

export function datasetPrepare() {
    const url = baseUrl + urls.api.dataset.prepare;
    var responseData;

    return async dispatch => {
        dispatch(datasetPrepareStarted());
        await axios.post(url)
            .then(response => {
                responseData = response.data;
                dispatch(datasetPrepareSuccess(response));
            })
            .catch(error => {
                dispatch(datasetPrepareFailure(error));
                throw error;
            });

        return responseData;
    };
}

const datasetPrepareStarted = () => ({
    type: actionTypes.DATASET_PREPARE_STARTED,
});
const datasetPrepareSuccess = response => ({
    type: actionTypes.DATASET_PREPARE_SUCCESS,
    response: {...response},
});
const datasetPrepareFailure = error => ({
    type: actionTypes.DATASET_PREPARE_FAILURE,
    response: {error},
});


/* * * * * * * * * * * * UI UPDATE  * * * * * * * * * *  */
export function datasetUIUpdate() {
    const url = baseUrl + urls.api.dataset.ui;
    var responseData;

    return async dispatch => {
        dispatch(datasetUIUpdateStarted());
        await axios.post(url)
            .then(response => {
                responseData = response.data;
                dispatch(datasetUIUpdateSuccess(response));
            })
            .catch(error => {
                dispatch(datasetUIUpdateFailure(error));
                throw error;
            });

        return responseData;
    };
}

const datasetUIUpdateStarted = () => ({
    type: actionTypes.DATASET_UI_UPDATE_STARTED,
});
const datasetUIUpdateSuccess = response => ({
    type: actionTypes.DATASET_UI_UPDATE_SUCCESS,
    response: {...response},
});
const datasetUIUpdateFailure = error => ({
    type: actionTypes.DATASET_UI_UPDATE_FAILURE,
    response: {error},
});
