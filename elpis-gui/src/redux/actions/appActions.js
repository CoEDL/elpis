import axios from 'axios'
import urls from 'urls'

import * as actionTypes from '../actionTypes/appActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://' + window.location.host

export const setCurrentStep = url => ({
    type: actionTypes.APP_SET_CURRENT_STEP,
    url
})


export const configReset = () => {
    console.log("actions configReset")
    const url = baseUrl + urls.api.config.reset
    return async dispatch => {
        await axios.post(url)
            .then(response => {
                dispatch(datasetResetSuccess(response))
            })
            .catch(error => {
                throw error
            })
        return "Reset OK"
    }
}

const datasetResetSuccess = response => ({
    type: actionTypes.APP_CONFIG_RESET,
    response: { ...response }
})