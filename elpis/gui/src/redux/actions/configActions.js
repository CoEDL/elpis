import axios from 'axios'
import urls from 'urls'

import * as actionTypes from '../actionTypes/appActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://' + window.location.host


/* * * * * * * * * * * *  RESET * * * * * * * * * * *  */

export const configReset = () => {
    const url = baseUrl + urls.api.config.reset
    var responseData
    return async (dispatch ) => {
        await axios.post(url)
            .then(response => {
                responseData = response.data
                dispatch(configResetSuccess(response))
            })
            .catch(error => {
                throw error
            })
        return responseData
    }
}

// reducer for this is in store.js
const configResetSuccess = response => ({
    type: actionTypes.APP_CONFIG_RESET,
    response: { ...response }
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


/* * * * * * * * * * * *  Get CONFIG * * * * * * * * * * *  */

// This loads config values that were set when starting the Flask app
// Also, get the engine list here

export function listAppConfig() {
    console.log("listAppConfig")
    const url = baseUrl + urls.api.config.list
    var responseData
    return async dispatch => {
        dispatch(listAppConfigStarted())
        await axios.get(url)
            .then(response => {
                responseData = response.data
                console.log("responseData", responseData)
                dispatch(listAppConfigSuccess(response))
                dispatch(engineListSuccess(response))
            })
            .catch(error => {
                dispatch(listAppConfigFailure(error))
                throw error
        })
        return responseData
    }
}

const listAppConfigStarted = () => ({
    type: actionTypes.LIST_APP_CONFIG_STARTED
})
const listAppConfigSuccess = response => ({
    type: actionTypes.LIST_APP_CONFIG_SUCCESS,
    response: { ...response }
})
const listAppConfigFailure = error => ({
    type: actionTypes.LIST_APP_CONFIG_FAILURE,
    response: { error }
})

const engineListSuccess = response => ({
    type: actionTypes.ENGINE_LIST_SUCCESS,
    response: { ...response }
})
