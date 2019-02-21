import axios from 'axios'
import urls from 'urls'

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://0.0.0.0:5000'

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
        console.log('postData', postData)
        axios.post(url, postData, config)
            .then((response) => {
                console.log("api response", response)
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
    dataBundleList: response => ({ type: 'DATA_BUNDLE_LIST', response }),
    dataBundleNew: response => ({ type: 'DATA_BUNDLE_NEW', response }),
    dataBundleName: response => ({ type: 'DATA_BUNDLE_NAME', response }),
    dataBundleFiles: response => ({ type: 'DATA_BUNDLE_FILES', response }),
    dataBundleSettings: response => ({ type: 'DATA_BUNDLE_SETTINGS', response }),
    dataBundlePrepare: response => ({ type: 'DATA_BUNDLE_PREPARE', response }),

    modelList: response => ({ type: 'MODEL_LIST', response }),
    modelNew: response => ({ type: 'MODEL_NEW', response }),
    modelName: response => ({ type: 'MODEL_NAME', response }),
    modelDate: response => ({ type: 'MODEL_DATE', response }),
    modelSettings: response => ({ type: 'MODEL_SETTINGS', response }),
    modelPronunciation: response => ({ type: 'MODEL_PRONUNCIATION', response }),

    newTranscriptionFile: response => ({ type: 'NEW_TRANSCRIPTION_FILE', response })
}

// * * * * * * * * * * DATA BUNDLES * * * * * * * * * * * * * * *

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

export const dataBundlePrepare = () => {
    console.log("action do dataBundlePrepare")
    const url = baseUrl + urls.api.dataBundle.prepare
    return postApi(url, null, 'dataBundlePrepare')
}


// * * * * * * * * * * MODEL * * * * * * * * * * * * * * *

export const modelList = () => {
    const url = baseUrl + urls.api.model.list
    return postApi(url, null, 'modelList')
}

export const modelNew = postData => {
    console.log("action modelNew", postData)
    const url = baseUrl + urls.api.model.new
    return postApi(url, postData, 'modelNew')
}

export const modelName = postData => {
    const url = baseUrl + '/api/model/name'
    return postApi(url, postData, 'modelName')
}

export const modelPronunciation = postData => {
    const url = baseUrl + '/api/model/pronunciation'
    const headers = {headers: {'content-type': 'multipart/form-data'}}
    return postApi(url, postData, 'modelPronunciation', headers)
}

export const modelLexicon = () => {
    const url = baseUrl + '/api/model/lexicon'
    return getApi(url, 'modelLexicon')
}
// GET_MODEL_LEXICON

export const modelSettings = postData => {
    const url = baseUrl + '/api/model/settings'
    return postApi(url, postData, 'modelSettings')
}

// get or post?
export const modelTraining = () => {
    const url = baseUrl + '/api/model/train'
    return postApi(url, 'modelTraining')
}

// need a model id?
export const modelTrainingResults = () => {
    const url = baseUrl + '/api/model/results'
    return postApi(url, 'modelTrainingResults')
}




// * * * * * * * * * * TRANSCRIPTION * * * * * * * * * * * * * * *

export const transcriptionNew = postData => {
    // const url = "http://httpbin.org/post"
    const url = baseUrl + '/api/transcription/audio'
    const headers = {headers: {'content-type': 'multipart/form-data'}}
    return postApi(url, postData, 'transcriptionNew', headers)
}

// TODO: action to download Elan file

// TODO: action to download PRAAT file


// * * * * * * * * * * GENERAL * * * * * * * * * * * * * * *

export const setCurrentStep = (url) => ({ type: 'SET_CURRENT_STEP', url })

export const replaceFiles = (status) => ({ type: 'REPLACE_FILES', status })

export const triggerApiWaiting = (message) => ({ type: 'TRIGGER_API_WAITING', message })
