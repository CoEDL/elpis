import axios from 'axios'
import urls from 'urls'

import * as actionTypes from '../actionTypes/datasetActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://'+window.location.host

/* * * * * * * * * * * *  NEW * * * * * * * * * * *  */

// make new dataset, then change url to add files page
export function datasetNew(postData) {
    const url = baseUrl + urls.api.dataset.new
    return async dispatch => {
        dispatch(datasetNewStarted())
        await axios.post(url, postData)
            .then( response => {
                dispatch(datasetNewSuccess(response))
            })
            .catch( error => {
                dispatch(datasetNewFailure(error))
                throw error
            })
        return "Made a new dataset OK"
    }
}

const datasetNewStarted = () => ({
    type: actionTypes.DATASET_NEW_STARTED
})
const datasetNewSuccess = response => ({
    type: actionTypes.DATASET_NEW_SUCCESS,
    payload: { ...response }
})
const datasetNewFailure = error => ({
    type: actionTypes.DATASET_NEW_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  LOAD * * * * * * * * * * *  */


export function datasetLoad(postData) {
    const url = baseUrl + urls.api.dataset.load
    return async dispatch => {
        dispatch(datasetLoadStarted())
        await axios.post(url, postData)
            .then(response => {
                dispatch(datasetLoadSuccess(response))
            })
            .catch(error => {
                dispatch(datasetLoadFailure(error))
                throw error
            })
        return "Loaded a dataset OK"
    }
}

const datasetLoadStarted = () => ({
    type: actionTypes.DATASET_LOAD_STARTED
})
const datasetLoadSuccess = response => ({
    type: actionTypes.DATASET_LOAD_SUCCESS,
    payload: { ...response }
})
const datasetLoadFailure = error => ({
    type: actionTypes.DATASET_LOAD_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  LIST * * * * * * * * * * *  */

export function datasetList() {
    const url = baseUrl + urls.api.dataset.list
    return async dispatch => {
        dispatch(datasetListStarted())
        await axios.post(url)
            .then(response => {
                dispatch(datasetListSuccess(response))
            })
            .catch(error => {
                dispatch(datasetListFailure(error))
                throw error
})
        return "Listed datasets OK"
    }
}

const datasetListStarted = () => ({
    type: actionTypes.DATASET_LIST_STARTED
})
const datasetListSuccess = response => ({
    type: actionTypes.DATASET_LIST_SUCCESS,
    payload: { ...response }
})
const datasetListFailure = error => ({
    type: actionTypes.DATASET_LIST_FAILURE,
    payload: { error }
})



/* * * * * * * * * * * *  FILES * * * * * * * * * * *  */

export function datasetFiles(postData) {
    const url = baseUrl + urls.api.dataset.files
    const config = { headers: { 'content-type': 'multipart/form-data' } }
    return async dispatch => {
        dispatch(datasetFilesStarted())
        await axios.post(url, postData, config)
            .then(response => {
                dispatch(datasetFilesSuccess(response))
            })
            .catch(error => {
                dispatch(datasetFilesFailure(error))
                throw error
            })
        return "Added files to a dataset OK"
    }
}

const datasetFilesStarted = () => ({
    type: actionTypes.DATASET_FILES_STARTED
})
const datasetFilesSuccess = response => ({
    type: actionTypes.DATASET_FILES_SUCCESS,
    payload: { ...response }
})
const datasetFilesFailure = error => ({
    type: actionTypes.DATASET_FILES_FAILURE,
    payload: { error }
})




/* * * * * * * * * * * *  SETTINGS * * * * * * * * * * *  */

export function datasetSettings(postData) {
    const url = baseUrl + urls.api.dataset.settings
    return async dispatch => {
        dispatch(datasetSettingsStarted())
        await axios.post(url, postData)
            .then(response => {
                dispatch(datasetSettingsSuccess(response))
            })
            .catch(error => {
                dispatch(datasetSettingsFailure(error))
                throw error
            })
        return "Added settings to a dataset OK"
    }
}

const datasetSettingsStarted = () => ({
    type: actionTypes.DATASET_SETTINGS_STARTED
})
const datasetSettingsSuccess = response => ({
    type: actionTypes.DATASET_SETTINGS_SUCCESS,
    payload: { ...response }
})
const datasetSettingsFailure = error => ({
    type: actionTypes.DATASET_SETTINGS_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  PREPARE * * * * * * * * * * *  */

export function datasetPrepare() {
    console.log("prepare")
    const url = baseUrl + urls.api.dataset.prepare
    return async dispatch => {
        dispatch(datasetPrepareStarted())
        await axios.post(url)
            .then(response => {
                console.log("datasetPrepare action got response", response)
                dispatch(datasetPrepareSuccess(response))
            })
            .catch(error => {
                dispatch(datasetPrepareFailure(error))
                throw error
            })
        return "Added prepare to a dataset OK"
    }
}

const datasetPrepareStarted = () => ({
    type: actionTypes.DATASET_PREPARE_STARTED
})
const datasetPrepareSuccess = response => ({
    type: actionTypes.DATASET_PREPARE_SUCCESS,
    payload: { ...response }
})
const datasetPrepareFailure = error => ({
    type: actionTypes.DATASET_PREPARE_FAILURE,
    payload: { error }
})


