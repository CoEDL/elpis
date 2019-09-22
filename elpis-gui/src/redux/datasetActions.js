import axios from 'axios'
import urls from 'urls'

import {
  DATASET_NEW_UNSTARTED,
  DATASET_NEW_STARTED,
  DATASET_NEW_SUCCESS,
  DATASET_NEW_FAILURE
} from './datasetActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://'+window.location.host



// make new, then change url
export function datasetNew(postData, history) {
    const url = baseUrl + urls.api.dataset.new
    return async dispatch => {
        dispatch(datasetNewStarted())
        await axios.post(url, postData)
            .then( response => {
                dispatch(datasetNewSuccess(response))
                history.push(urls.gui.dataset.files)
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
