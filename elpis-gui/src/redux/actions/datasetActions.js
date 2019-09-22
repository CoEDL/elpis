import axios from 'axios'
import urls from 'urls'

import {
    DATASET_NEW_STARTED,
    DATASET_NEW_SUCCESS,
    DATASET_NEW_FAILURE,

    DATASET_LOAD_STARTED,
    DATASET_LOAD_SUCCESS,
    DATASET_LOAD_FAILURE
} from '../types/datasetActionTypes';

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
        return "OK"
    }
}

const datasetNewStarted = () => ({
    type: DATASET_NEW_STARTED
})

const datasetNewSuccess = response => ({
    type: DATASET_NEW_SUCCESS,
    payload: { ...response }
})

const datasetNewFailure = error => ({
    type: DATASET_NEW_FAILURE,
    payload: { error }
})



/* * * * * * * * * * * *  LOAD * * * * * * * * * * *  */


export function datasetLoad(postData) {
    console.log("ds actions load")
    const url = baseUrl + urls.api.dataset.load
    return async dispatch => {
        dispatch(datasetLoadStarted())
        await axios.post(url, postData)
            .then(response => {
                console.log("datasetLoad response", response)
                dispatch(datasetLoadSuccess(response))
            })
            .catch(error => {
                dispatch(datasetLoadFailure(error))
                throw error
            })
        return "OK"
    }
}


const datasetLoadStarted = () => ({
    type: DATASET_LOAD_STARTED
})

const datasetLoadSuccess = response => ({
    type: DATASET_LOAD_SUCCESS,
    payload: { ...response }
})

const datasetLoadFailure = error => ({
    type: DATASET_LOAD_FAILURE,
    payload: { error }
})

