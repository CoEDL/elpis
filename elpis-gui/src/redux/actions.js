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
    return dispatch => {
        // console.log('postData', url, postData)
        axios.post(url, postData, config)
            .then((response) => {
                // console.log("api response", response)
                dispatch(successHandler[successFunction](response))
            }).catch((error) => {
                dispatch(errorHandler(error))
            })
    }
}


export const errorHandler = (error) => {
    return { type: 'ERROR', error }
}

var successHandler = {
    dataBundleLoad: response => ({ type: 'DATA_BUNDLE_LOAD', response }),
    dataBundleList: response => ({ type: 'DATA_BUNDLE_LIST', response }),
    dataBundleNew: response => ({ type: 'DATA_BUNDLE_NEW', response }),
    dataBundleName: response => ({ type: 'DATA_BUNDLE_NAME', response }),
    dataBundleFiles: response => ({ type: 'DATA_BUNDLE_FILES', response }),
    dataBundleSettings: response => ({ type: 'DATA_BUNDLE_SETTINGS', response }),
    dataBundlePrepare: response => ({ type: 'DATA_BUNDLE_PREPARE', response }),

    modelLoad: response => ({ type: 'MODEL_LOAD', response }),
    modelList: response => ({ type: 'MODEL_LIST', response }),
    modelNew: response => ({ type: 'MODEL_NEW', response }),
    modelName: response => ({ type: 'MODEL_NAME', response }),
    modelL2S: response => ({ type: 'MODEL_L2S', response }),
    modelLexicon: response => ({ type: 'MODEL_LEXICON', response }),
    modelSettings: response => ({ type: 'MODEL_SETTINGS', response }),
    modelTrain: response => ({ type: 'MODEL_TRAIN', response }),
    modelStatus: response => ({ type: 'MODEL_STATUS', response }),
    modelResults: response => ({ type: 'MODEL_RESULTS', response }),

    transcriptionPrepare: response => ({ type: 'TRANSCRIPTION_PREPARE', response }),
    transcriptionStatus: response => ({ type: 'TRANSCRIPTION_STATUS', response }),
    transcriptionTranscribe: response => ({ type: 'TRANSCRIPTION_TRANSCRIBE', response }),
    transcriptionTranscribeAlign: response => ({ type: 'TRANSCRIPTION_TRANSCRIBE_ALIGN', response }),
    transcriptionGetText: response => ({ type: 'TRANSCRIPTION_GET_TEXT', response }),
    transcriptionGetElan: response => ({ type: 'TRANSCRIPTION_GET_ELAN', response })
}

// * * * * * * * * * * DATA BUNDLES * * * * * * * * * * * * * * *

export const dataBundleLoad = postData => {
    const url = baseUrl + urls.api.dataBundle.load
    return postApi(url, postData, 'dataBundleLoad')
}
export const dataBundleList = () => {
    const url = baseUrl + urls.api.dataBundle.list
    return postApi(url, null, 'dataBundleList')
}
export const dataBundleNew = postData => {
    const url = baseUrl + urls.api.dataBundle.new
    return postApi(url, postData, 'dataBundleNew')
}
export const dataBundleName = postData => {
    const url = baseUrl + urls.api.dataBundle.name
    return postApi(url, postData, 'dataBundleName')
}
export const dataBundleSettings = postData => {
    const url = baseUrl + urls.api.dataBundle.settings
    return postApi(url, postData, 'dataBundleSettings')
}
export const dataBundleFiles = postData => {
    const url = baseUrl + urls.api.dataBundle.files
    const headers = {headers: {'content-type': 'multipart/form-data'}}
    return postApi(url, postData, 'dataBundleFiles', headers)
}
export const dataBundleStatus = status => ({ type: 'DATA_BUNDLE_STATUS', status })
export const dataBundlePrepare = () => {
    const url = baseUrl + urls.api.dataBundle.prepare
    return postApi(url, null, 'dataBundlePrepare')
}


// * * * * * * * * * * MODEL * * * * * * * * * * * * * * *

export const modelLoad = postData => {
    const url = baseUrl + urls.api.model.load
    return postApi(url, postData, 'modelLoad')
}
export const modelList = () => {
    const url = baseUrl + urls.api.model.list
    return postApi(url, null, 'modelList')
}
export const modelNew = postData => {
    const url = baseUrl + urls.api.model.new
    return postApi(url, postData, 'modelNew')
}
export const modelName = postData => {
    const url = baseUrl + '/api/model/name'
    return postApi(url, postData, 'modelName')
}
export const modelL2S = postData => {
    const url = baseUrl + urls.api.model.l2s
    const headers = {headers: {'content-type': 'multipart/form-data'}}
    return postApi(url, postData, 'modelL2S', headers)
}
export const modelLexicon = () => {
    const url = baseUrl + urls.api.model.lexicon
    return postApi(url, null, 'modelLexicon')
}
export const modelSettings = postData => {
    const url = baseUrl + urls.api.model.settings
    return postApi(url, postData, 'modelSettings')
}
export const modelTrain = () => {
    const url = baseUrl + urls.api.model.train
    return postApi(url, null, 'modelTrain')
}
export const modelStatus = () => {
    const url = baseUrl + urls.api.model.status
    return postApi(url, null, 'modelStatus')
}
export const modelResults = () => {
    console.log("action to get results")
    const url = baseUrl + urls.api.model.results
    return postApi(url, null, 'modelResults')
}



// * * * * * * * * * * TRANSCRIPTION * * * * * * * * * * * * * * *


// export const transcriptionNew = postData => {
//     console.log("start a new transcription")
//     const url = baseUrl + urls.api.transcription.new
//     const headers = {headers: {'content-type': 'multipart/form-data'}}
//     return postApi(url, postData, 'transcriptionNew', headers)
// }
// export const transcriptionNewAlign = postData => {
//     console.log("start a new transcription align")
//     const url = baseUrl + urls.api.transcription.newAlign
//     console.log("url", url)
//     const headers = {headers: {'content-type': 'multipart/form-data'}}
//     return postApi(url, postData, 'transcriptionNewAlign', headers)
// }
// export const transcriptionGetText = postData => {
//     const url = baseUrl + urls.api.transcription.text
//     return postApi(url, null, 'transcriptionGetText')
// }

export const transcriptionAudioFile = filename => {
    console.log("action got file", filename)
    return ({ type: 'TRANSCRIPTION_AUDIO_FILE', filename })
}
export const transcriptionPrepare = postData => {
    const url = baseUrl + urls.api.transcription.new
    const headers = { headers: { 'content-type': 'multipart/form-data' } }
    return postApi(url, postData, 'transcriptionPrepare', headers)
}
export const transcriptionStatus = () => {
    const url = baseUrl + urls.api.transcription.status
    return postApi(url, null, 'transcriptionStatus')
}
export const transcriptionTranscribe = () => {
    const url = baseUrl + urls.api.transcription.transcribe
    console.log(url)
    return postApi(url, null, 'transcriptionTranscribe')
}
export const transcriptionTranscribeAlign = () => {
    const url = baseUrl + urls.api.transcription.transcribe_align
    console.log(url)
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


// * * * * * * * * * * GENERAL * * * * * * * * * * * * * * *

export const setCurrentStep = url => ({ type: 'SET_CURRENT_STEP', url })

export const triggerApiWaiting = message => ({ type: 'TRIGGER_API_WAITING', message })
