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
    datasetFiles: response => ({ type: 'DATASET_FILES', response }),
    datasetSettings: response => ({ type: 'DATASET_SETTINGS', response }),
    datasetPrepare: response => ({ type: 'DATASET_PREPARE', response }),

    pronDictLoad: response => ({ type: 'PRON_DICT_LOAD', response }),
    pronDictList: response => ({ type: 'PRON_DICT_LIST', response }),
    pronDictNew: response => ({ type: 'PRON_DICT_NEW', response }),
    pronDictName: response => ({ type: 'PRON_DICT_NAME', response }),
    pronDictL2S: response => ({ type: 'PRON_DICT_L2S', response }),
    pronDictLexicon: response => ({ type: 'PRON_DICT_LEXICON', response }),
    pronDictGenerateLexicon: response => ({ type: 'PRON_DICT_LEXICON', response }),
    pronDictSaveLexicon: response => ({ type: 'PRON_DICT_SAVE_LEXICON', response }),

    modelLoad: response => ({ type: 'MODEL_LOAD', response }),
    modelList: response => ({ type: 'MODEL_LIST', response }),
    modelNew: response => ({ type: 'MODEL_NEW', response }),
    modelName: response => ({ type: 'MODEL_NAME', response }),
    modelSettings: response => ({ type: 'MODEL_SETTINGS', response }),
    modelTrain: response => ({ type: 'MODEL_TRAIN', response }),
    modelStatus: response => ({ type: 'MODEL_STATUS', response }),
    modelResults: response => ({ type: 'MODEL_RESULTS', response }),

    transcriptionPrepare: response => ({ type: 'TRANSCRIPTION_PREPARE', response }),
    transcriptionStatus: response => ({ type: 'TRANSCRIPTION_STATUS', response }),
    transcriptionTranscribe: response => ({ type: 'TRANSCRIPTION_TRANSCRIBE', response }),
    transcriptionTranscribeAlign: response => ({ type: 'TRANSCRIPTION_TRANSCRIBE_ALIGN', response }),
    transcriptionGetText: response => ({ type: 'TRANSCRIPTION_GET_TEXT', response }),
    transcriptionGetElan: response => ({ type: 'TRANSCRIPTION_GET_ELAN', response }),

    configReset: response => ({ type: 'CONFIG_RESET', response })
}

// * * * * * * * * * * DATA SETS * * * * * * * * * * * * * * *


export const datasetSettings = postData => {
    const url = baseUrl + urls.api.dataset.settings
    return postApi(url, postData, 'datasetSettings')
}
export const datasetPrepare = () => {
    const url = baseUrl + urls.api.dataset.prepare
    return postApi(url, null, 'datasetPrepare')
}


// * * * * * * * * * * PRON DICT * * * * * * * * * * * * * * *


export const pronDictLoad = postData => {
    const url = baseUrl + urls.api.pronDict.load
    return postApi(url, postData, 'pronDictLoad')
}
export const pronDictList = () => {
    const url = baseUrl + urls.api.pronDict.list
    return postApi(url, null, 'pronDictList')
}
export const pronDictNew = postData => {
    const url = baseUrl + urls.api.pronDict.new
    return postApi(url, postData, 'pronDictNew')
}
export const pronDictName = postData => {
    const url = baseUrl + urls.api.pronDict.name
    return postApi(url, postData, 'pronDictName')
}
export const pronDictL2S = postData => {
    const url = baseUrl + urls.api.pronDict.l2s
    const headers = { headers: { 'content-type': 'multipart/form-data' } }
    return postApi(url, postData, 'pronDictL2S', headers)
}
export const pronDictLexicon = () => {
    const url = baseUrl + urls.api.pronDict.lexicon
    return postApi(url, null, 'pronDictLexicon')
}
export const pronDictGenerateLexicon = () => {
    const url = baseUrl + urls.api.pronDict.generateLexicon
    return postApi(url, null, 'pronDictGenerateLexicon')
}
export const pronDictSaveLexicon = postData => {
    const url = baseUrl + urls.api.pronDict.saveLexicon
    return postApi(url, postData, 'pronDictSaveLexicon')
}
export const testUpdateLexicon = data => ({ type: 'TEST_UPDATE_LEXICON', data })

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
    const url = baseUrl + urls.api.model.name
    return postApi(url, postData, 'modelName')
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
    const url = baseUrl + urls.api.model.results
    return postApi(url, null, 'modelResults')
}



// * * * * * * * * * * TRANSCRIPTION * * * * * * * * * * * * * * *


export const transcriptionAudioFile = filename => {
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


// * * * * * * * * * * GENERAL * * * * * * * * * * * * * * *

export const setCurrentStep = url => ({ type: 'SET_CURRENT_STEP', url })

export const triggerApiWaiting = message => ({ type: 'TRIGGER_API_WAITING', message })

export const configReset = postData => {
    console.log("actions configReset")
    const url = baseUrl + urls.api.config.reset
    return postApi(url, null, 'configReset')
}
