import axios from 'axios'
import urls from 'urls'

console.log(window.location.host)
// 'http://0.0.0.0:5000'
const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://'+window.location.host

const getApi = (url, successFunction) => {
    return dispatch => {
        axios.get(url)
            .then((response) => {
                // If the API call went OK (HTTP status 200),
                // dispatch the success handler that came with the request
                dispatch(successHandler[successFunction](response))
            }).catch((error) => {
                // For HTTP 400 error responses, dispatch a generic error
                // or we could use a similar pattern as success for custom actions
                dispatch(errorHandler(error))
            })
    }
}

const postApi = (url, postData, successFunction, config=null) => {
    // console.log("postAPI doing", url, postData)
    return dispatch => {
        // console.log('postData', url, postData)
        axios.post(url, postData, config)
            .then((response) => {
                // console.log("api response", response)
                dispatch(successHandler[successFunction](response))
            }).catch((error) => {
                // console.log("api error", error)
                dispatch(errorHandler(error))
            })
    }
}


export const errorHandler = (error) => {
    return { type: 'ERROR', error }
}

var successHandler = {

    transcriptionNew: response => ({ type: 'TRANSCRIPTION_PREPARE', response }),
    transcriptionStatus: response => ({ type: 'TRANSCRIPTION_STATUS', response }),
    transcriptionTranscribe: response => ({ type: 'TRANSCRIPTION_TRANSCRIBE', response }),
    transcriptionTranscribeAlign: response => ({ type: 'TRANSCRIPTION_TRANSCRIBE_ALIGN', response }),
    transcriptionGetText: response => ({ type: 'TRANSCRIPTION_GET_TEXT', response }),
    transcriptionGetElan: response => ({ type: 'TRANSCRIPTION_GET_ELAN', response }),

    configReset: response => ({ type: 'CONFIG_RESET', response })
}


// * * * * * * * * * * TRANSCRIPTION * * * * * * * * * * * * * * *


export const transcriptionAudioFile = filename => {
    return ({ type: 'TRANSCRIPTION_AUDIO_FILE', filename })
}
export const transcriptionNew = postData => {
    const url = baseUrl + urls.api.transcription.new
    const headers = { headers: { 'content-type': 'multipart/form-data' } }
    return postApi(url, postData, 'transcriptionNew', headers)
}
export const transcriptionStatus = () => {
    const url = baseUrl + urls.api.transcription.status
    return postApi(url, null, 'transcriptionStatus')
}
export const transcriptionTranscribe = () => {
    const url = baseUrl + urls.api.transcription.transcribe
    return postApi(url, null, 'transcriptionTranscribe')
}
export const transcriptionTranscribeAlign = () => {
    const url = baseUrl + urls.api.transcription.transcribe_align
    return postApi(url, null, 'transcriptionTranscribeAlign')
}
export const transcriptionGetText = postData => {
    const url = baseUrl + urls.api.transcription.text
    return postApi(url, null, 'transcriptionGetText')
}
export const transcriptionGetElan = postData => {
    const url = baseUrl + urls.api.transcription.elan
    return postApi(url, null, 'transcriptionGetElan')
}
export const transcriptionStatusReset = status => ({ type: 'TRANSCRIPTION_STATUS_RESET', status })

