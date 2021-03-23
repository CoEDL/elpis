import axios from "axios";
import urls from "urls";

import * as actionTypes from "../actionTypes/transcriptionActionTypes";

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : "http://"+window.location.host;


/* * * * * * * * * * * *  NEW * * * * * * * * * * *  */

export function transcriptionNew(postData) {
    const url = baseUrl + urls.api.transcription.new;
    const config = { headers: { "content-type": "multipart/form-data" } };
    var responseData;
    return async dispatch => {
        dispatch(transcriptionNewStarted());
        await axios.post(url, postData, config)
            .then( response => {
                responseData = response.data;
                dispatch(transcriptionNewSuccess(response));
            })
            .catch( error => {
                dispatch(transcriptionNewFailure(error));
                throw error;
            });
        return responseData;
    };
}

const transcriptionNewStarted = () => ({
    type: actionTypes.TRANSCRIPTION_NEW_STARTED,
});
const transcriptionNewSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_NEW_SUCCESS,
    response: { ...response },
});
const transcriptionNewFailure = error => ({
    type: actionTypes.TRANSCRIPTION_NEW_FAILURE,
    response: { error },
});


/* * * * * * * * * * * *  TRANSCRIBE * * * * * * * * * * *  */

export function transcriptionTranscribe() {
    const url = baseUrl + urls.api.transcription.transcribe;
    var responseData;
    return async dispatch => {
        dispatch(transcriptionTranscribeStarted());
        await axios.get(url)
            .then(response => {
                // this is a status value
                responseData = response.data;
                dispatch(transcriptionTranscribeSuccess(response));
            })
            .catch(error => {
                dispatch(transcriptionTranscribeFailure(error));
                throw error;
            });
        return responseData;
    };
}

const transcriptionTranscribeStarted = () => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_STARTED,
});
const transcriptionTranscribeSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_SUCCESS,
    response: { ...response },
});
const transcriptionTranscribeFailure = error => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_FAILURE,
    response: { error },
});


/* * * * * * * * * * * *  STATUS * * * * * * * * * * *  */

export function transcriptionStatus() {
    const url = baseUrl + urls.api.transcription.status;
    var responseData;
    return async dispatch => {
        dispatch(transcriptionStatusStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(transcriptionStatusSuccess(response));
            })
            .catch(error => {
                dispatch(transcriptionStatusFailure(error));
                throw error;
            });
        return responseData;
    };
}

const transcriptionStatusStarted = () => ({
    type: actionTypes.TRANSCRIPTION_STATUS_STARTED,
});
const transcriptionStatusSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_STATUS_SUCCESS,
    response: { ...response },
});
const transcriptionStatusFailure = error => ({
    type: actionTypes.TRANSCRIPTION_STATUS_FAILURE,
    response: { error },
});


/* * * * * * * * * * * *  TEXT * * * * * * * * * * *  */

export function transcriptionGetText() {
    const url = baseUrl + urls.api.transcription.text;
    var responseData;
    return async dispatch => {
        dispatch(transcriptionGetTextStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(transcriptionGetTextSuccess(response));
            })
            .catch(error => {
                dispatch(transcriptionGetTextFailure(error));
                throw error;
            });
        return responseData;
    };
}

const transcriptionGetTextStarted = () => ({
    type: actionTypes.TRANSCRIPTION_GET_TEXT_STARTED,
});
const transcriptionGetTextSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_GET_TEXT_SUCCESS,
    response: { ...response },
});
const transcriptionGetTextFailure = error => ({
    type: actionTypes.TRANSCRIPTION_GET_TEXT_FAILURE,
    response: { error },
});


/* * * * * * * * * * * *  ELAN * * * * * * * * * * *  */

export function transcriptionGetElan() {
    const url = baseUrl + urls.api.transcription.elan;
    var responseData;
    return async dispatch => {
        dispatch(transcriptionGetElanStarted());
        await axios.get(url)
            .then(response => {
                responseData = response.data;
                dispatch(transcriptionGetElanSuccess(response));
            })
            .catch(error => {
                dispatch(transcriptionGetElanFailure(error));
                throw error;
            });
        return responseData;
    };
}

const transcriptionGetElanStarted = () => ({
    type: actionTypes.TRANSCRIPTION_GET_ELAN_STARTED,
});
const transcriptionGetElanSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_GET_ELAN_SUCCESS,
    response: { ...response },
});
const transcriptionGetElanFailure = error => ({
    type: actionTypes.TRANSCRIPTION_GET_ELAN_FAILURE,
    response: { error },
});
