import axios from 'axios'
import urls from 'urls'

import * as actionTypes from '../actionTypes/appActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://' + window.location.host

export const setCurrentStep = url => ({
    type: actionTypes.APP_SET_CURRENT_STEP,
    url
})

export const configReset = () => {
    const url = baseUrl + urls.api.config.reset
    var responseData
    return async (dispatch ) => {
        await axios.post(url)
            .then(response => {
                responseData = response.data
                dispatch(datasetResetSuccess(response))
            })
            .catch(error => {
                throw error
            })
        return responseData
    }
}

// reducer for this is in store.js
const datasetResetSuccess = response => ({
    type: actionTypes.APP_CONFIG_RESET,
    response: { ...response }
})

/* * * * * * * * * * * *  LOAD * * * * * * * * * * *  */

export const engineLoad = (postData) => {
    const url = baseUrl + urls.api.engine.load;
    let responseData;
    return async dispatch => {
        dispatch(engineLoadStarted())
        await axios.post(url, postData)
            .then( response => {
                responseData = response.data
                dispatch(engineLoadSuccess(response))
            })
            .catch( error => {
                dispatch(engineLoadFailure(error))
                throw error
            })
        return responseData
    }

}

const engineLoadStarted = () => ({
    type: actionTypes.ENGINE_LOAD_STARTED
})
const engineLoadSuccess = response => ({
    type: actionTypes.ENGINE_LOAD_SUCCESS,
    response: { ...response }
})
const engineLoadFailure = error => ({
    type: actionTypes.ENGINE_LOAD_FAILURE,
    response: { error }
})

/* * * * * * * * * * * *  ENGINE LIST * * * * * * * * * * *  */

export function engineList() {
    const url = baseUrl + urls.api.engine.list
    var responseData
    return async dispatch => {
        dispatch(engineListStarted())
        await axios.get(url)
            .then(response => {
                responseData = response.data
                dispatch(engineListSuccess(response))
            })
            .catch(error => {
                dispatch(engineListFailure(error))
                throw error
        })
        return responseData
    }
}

const engineListStarted = () => ({
    type: actionTypes.ENGINE_LIST_STARTED
})
const engineListSuccess = response => ({
    type: actionTypes.ENGINE_LIST_SUCCESS,
    response: { ...response }
})
const engineListFailure = error => ({
    type: actionTypes.ENGINE_LIST_FAILURE,
    response: { error }
})


/* * * * * * * * * * * *  INTERFACE * * * * * * * * * * *  */

// this loads all the names of datasets, pron_dicts, models that have been made

export function interfaceObjectNames() {
    const url = baseUrl + urls.api.interface.objectNames
    var responseData
    return async dispatch => {
        dispatch(interfaceObjectNamesStarted())
        await axios.get(url)
            .then(response => {
                responseData = response.data
                dispatch(interfaceObjectNamesSuccess(response))
            })
            .catch(error => {
                dispatch(interfaceObjectNamesFailure(error))
                throw error
        })
        return responseData
    }
}

const interfaceObjectNamesStarted = () => ({
    type: actionTypes.CONFIG_OBJECT_NAMES_STARTED
})
const interfaceObjectNamesSuccess = response => ({
    type: actionTypes.CONFIG_OBJECT_NAMES_SUCCESS,
    response: { ...response }
})
const interfaceObjectNamesFailure = error => ({
    type: actionTypes.CONFIG_OBJECT_NAMES_FAILURE,
    response: { error }
})

