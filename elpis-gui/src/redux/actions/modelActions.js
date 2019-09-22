import axios from 'axios'
import urls from 'urls'

import * as actionTypes from '../actionTypes/modelActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://'+window.location.host

/* * * * * * * * * * * *  NEW * * * * * * * * * * *  */

// make new model, then change url to add files page
export function modelNew(postData) {
    const url = baseUrl + urls.api.model.new
    return async dispatch => {
        dispatch(modelNewStarted())
        await axios.post(url, postData)
            .then( response => {
                dispatch(modelNewSuccess(response))
            })
            .catch( error => {
                dispatch(modelNewFailure(error))
                throw error
            })
        return "Made a new model OK"
    }
}

const modelNewStarted = () => ({
    type: actionTypes.MODEL_NEW_STARTED
})
const modelNewSuccess = response => ({
    type: actionTypes.MODEL_NEW_SUCCESS,
    payload: { ...response }
})
const modelNewFailure = error => ({
    type: actionTypes.MODEL_NEW_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  LOAD * * * * * * * * * * *  */


export function modelLoad(postData) {
    const url = baseUrl + urls.api.model.load
    return async dispatch => {
        dispatch(modelLoadStarted())
        await axios.post(url, postData)
            .then(response => {
                dispatch(modelLoadSuccess(response))
            })
            .catch(error => {
                dispatch(modelLoadFailure(error))
                throw error
            })
        return "Loaded a model OK"
    }
}

const modelLoadStarted = () => ({
    type: actionTypes.MODEL_LOAD_STARTED
})
const modelLoadSuccess = response => ({
    type: actionTypes.MODEL_LOAD_SUCCESS,
    payload: { ...response }
})
const modelLoadFailure = error => ({
    type: actionTypes.MODEL_LOAD_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  LIST * * * * * * * * * * *  */

export function modelList() {
    const url = baseUrl + urls.api.model.list
    return async dispatch => {
        dispatch(modelListStarted())
        await axios.post(url)
            .then(response => {
                dispatch(modelListSuccess(response))
            })
            .catch(error => {
                dispatch(modelListFailure(error))
                throw error
            })
        return "Listed models OK"
    }
}

const modelListStarted = () => ({
    type: actionTypes.MODEL_LIST_STARTED
})
const modelListSuccess = response => ({
    type: actionTypes.MODEL_LIST_SUCCESS,
    payload: { ...response }
})
const modelListFailure = error => ({
    type: actionTypes.MODEL_LIST_FAILURE,
    payload: { error }
})




/* * * * * * * * * * * *  SETTINGS * * * * * * * * * * *  */

export function modelSettings(postData) {
    const url = baseUrl + urls.api.model.settings
    return async dispatch => {
        dispatch(modelSettingsStarted())
        await axios.post(url, postData)
            .then(response => {
                dispatch(modelSettingsSuccess(response))
            })
            .catch(error => {
                dispatch(modelSettingsFailure(error))
                throw error
            })
        return "Added settings to a model OK"
    }
}

const modelSettingsStarted = () => ({
    type: actionTypes.MODEL_SETTINGS_STARTED
})
const modelSettingsSuccess = response => ({
    type: actionTypes.MODEL_SETTINGS_SUCCESS,
    payload: { ...response }
})
const modelSettingsFailure = error => ({
    type: actionTypes.MODEL_SETTINGS_FAILURE,
    payload: { error }
})



/* * * * * * * * * * * *  TRAIN * * * * * * * * * * *  */

export function modelTrain() {
    const url = baseUrl + urls.api.model.train
    return async dispatch => {
        dispatch(modelTrainStarted())
        await axios.post(url)
            .then(response => {
                dispatch(modelTrainSuccess(response))
            })
            .catch(error => {
                dispatch(modelTrainFailure(error))
                throw error
            })
        return "Trained models OK"
    }
}

const modelTrainStarted = () => ({
    type: actionTypes.MODEL_TRAIN_STARTED
})
const modelTrainSuccess = response => ({
    type: actionTypes.MODEL_TRAIN_SUCCESS,
    payload: { ...response }
})
const modelTrainFailure = error => ({
    type: actionTypes.MODEL_TRAIN_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  STATUS * * * * * * * * * * *  */

export function modelStatus() {
    const url = baseUrl + urls.api.model.status
    return async dispatch => {
        dispatch(modelStatusStarted())
        await axios.post(url)
            .then(response => {
                dispatch(modelStatusSuccess(response))
            })
            .catch(error => {
                dispatch(modelStatusFailure(error))
                throw error
            })
        return "Statused models OK"
    }
}

const modelStatusStarted = () => ({
    type: actionTypes.MODEL_STATUS_STARTED
})
const modelStatusSuccess = response => ({
    type: actionTypes.MODEL_STATUS_SUCCESS,
    payload: { ...response }
})
const modelStatusFailure = error => ({
    type: actionTypes.MODEL_STATUS_FAILURE,
    payload: { error }
})

