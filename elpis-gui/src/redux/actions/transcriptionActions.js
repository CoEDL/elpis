import axios from 'axios'
import urls from 'urls'

import * as actionTypes from '../actionTypes/transcriptionActionTypes';

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://'+window.location.host

/* * * * * * * * * * * *  NEW * * * * * * * * * * *  */

export function transcriptionNew(postData) {
    const url = baseUrl + urls.api.transcription.new
    const config = { headers: { 'content-type': 'multipart/form-data' } }
    return async dispatch => {
        dispatch(transcriptionNewStarted())
        await axios.post(url, postData, config)
            .then( response => {
                console.log("transcriptionNew action response", response)
                dispatch(transcriptionNewSuccess(response))
            })
            .catch( error => {
                dispatch(transcriptionNewFailure(error))
                throw error
            })
        return "Made a new transcription OK"
    }
}

const transcriptionNewStarted = () => ({
    type: actionTypes.TRANSCRIPTION_NEW_STARTED
})
const transcriptionNewSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_NEW_SUCCESS,
    payload: { ...response }
})
const transcriptionNewFailure = error => ({
    type: actionTypes.TRANSCRIPTION_NEW_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  STATUS * * * * * * * * * * *  */

export function transcriptionStatus() {
    console.log("action transcribe status")
    const url = baseUrl + urls.api.transcription.status
    return async dispatch => {
        dispatch(transcriptionStatusStarted())
        await axios.post(url)
            .then(response => {
                dispatch(transcriptionStatusSuccess(response))
            })
            .catch(error => {
                dispatch(transcriptionStatusFailure(error))
                throw error
            })
        return "Got status for transcriptions OK"
    }
}

const transcriptionStatusStarted = () => ({
    type: actionTypes.TRANSCRIPTION_STATUS_STARTED
})
const transcriptionStatusSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_STATUS_SUCCESS,
    payload: { ...response }
})
const transcriptionStatusFailure = error => ({
    type: actionTypes.TRANSCRIPTION_STATUS_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  TRANSCRIBE * * * * * * * * * * *  */

export function transcriptionTranscribe() {
    console.log("action transcribe")
    const url = baseUrl + urls.api.transcription.transcribe
    return async dispatch => {
        dispatch(transcriptionTranscribeStarted())
        await axios.post(url)
            .then(response => {
                // this is a status value
                dispatch(transcriptionTranscribeSuccess(response))
            })
            .catch(error => {
                dispatch(transcriptionTranscribeFailure(error))
                throw error
            })
        return "Got transcribe for transcription OK"
    }
}

const transcriptionTranscribeStarted = () => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_STARTED
})
const transcriptionTranscribeSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_SUCCESS,
    payload: { ...response }
})
const transcriptionTranscribeFailure = error => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  TRANSCRIBE ALIGN * * * * * * * * * * *  */

export function transcriptionTranscribeAlign() {
    console.log("action transcribe align")
    const url = baseUrl + urls.api.transcription.transcribe_align
    return async dispatch => {
        dispatch(transcriptionTranscribeAlignStarted())
        await axios.post(url)
            .then(response => {
                console.log("transcribe align got a response", response)
                dispatch(transcriptionTranscribeAlignSuccess(response))
            })
            .catch(error => {
                dispatch(transcriptionTranscribeAlignFailure(error))
                throw error
            })
        return "Got transcribe align for transcription OK"
    }
}

const transcriptionTranscribeAlignStarted = () => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_ALIGN_STARTED
})
const transcriptionTranscribeAlignSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_ALIGN_SUCCESS,
    payload: { ...response }
})
const transcriptionTranscribeAlignFailure = error => ({
    type: actionTypes.TRANSCRIPTION_TRANSCRIBE_ALIGN_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  TEXT * * * * * * * * * * *  */

export function transcriptionGetText() {
    console.log("action transcribe get text")
    const url = baseUrl + urls.api.transcription.text
    return async dispatch => {
        dispatch(transcriptionGetTextStarted())
        await axios.post(url)
            .then(response => {
                console.log("get text action got response", response)
                dispatch(transcriptionGetTextSuccess(response))
            })
            .catch(error => {
                dispatch(transcriptionGetTextFailure(error))
                throw error
            })
        return "Got text for transcriptions OK"
    }
}

const transcriptionGetTextStarted = () => ({
    type: actionTypes.TRANSCRIPTION_GET_TEXT_STARTED
})
const transcriptionGetTextSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_GET_TEXT_SUCCESS,
    payload: { ...response }
})
const transcriptionGetTextFailure = error => ({
    type: actionTypes.TRANSCRIPTION_GET_TEXT_FAILURE,
    payload: { error }
})


/* * * * * * * * * * * *  ELAN * * * * * * * * * * *  */

export function transcriptionGetElan() {
    console.log("action transcribe get elan")
    const url = baseUrl + urls.api.transcription.elan
    return async dispatch => {
        dispatch(transcriptionGetElanStarted())
        await axios.post(url)
            .then(response => {
                console.log("get elan action got response", response)
                dispatch(transcriptionGetElanSuccess(response))
            })
            .catch(error => {
                dispatch(transcriptionGetElanFailure(error))
                throw error
            })
        return "Got elan for transcriptions OK"
    }
}

const transcriptionGetElanStarted = () => ({
    type: actionTypes.TRANSCRIPTION_GET_ELAN_STARTED
})
const transcriptionGetElanSuccess = response => ({
    type: actionTypes.TRANSCRIPTION_GET_ELAN_SUCCESS,
    payload: { ...response }
})
const transcriptionGetElanFailure = error => ({
    type: actionTypes.TRANSCRIPTION_GET_ELAN_FAILURE,
    payload: { error }
})

