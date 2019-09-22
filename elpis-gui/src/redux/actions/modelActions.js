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


