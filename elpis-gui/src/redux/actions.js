import axios from 'axios'

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://127.0.0.1:5000'

const getApi = (url, successFunction) => {
    return dispatch => {
        axios.get(url)
            .then((response) => {
                // If the API call went OK (HTTP status 200),
                // dispatch the success handler that came with the request
                dispatch(successHandler[successFunction](response))
            }).catch((error) => {
                // For HTTP 400 error responses, dipatch a generic error
                // or we could use a similar pattern as success for custom actions
                dispatch(errorHandler(error))
            })
    }
}

const postApi = (url, postData, successFunction, config=null) => {
    return dispatch => {
        axios.post(url, postData, config)
            .then((response) => {
                console.log('success')
                dispatch(successHandler[successFunction](response))
            }).catch((error) => {
                console.log('error')
                dispatch(errorHandler(error))
            })
    }
}


export const errorHandler = (error) => {
    return { type: 'ERROR', error }
}

var successHandler = {
    dataBundleNew: response => ({ type: 'DATA_BUNDLE_NEW', response }),
    dataBundleName: response => ({ type: 'DATA_BUNDLE_NAME', response }),
    dataBundleFiles: response => ({ type: 'DATA_BUNDLE_FILES', response }),
    dataBundleSettings: response => ({ type: 'DATA_BUNDLE_SETTINGS', response }),

    modelNew: response => ({ type: 'MODEL_NEW', response }),
    modelName: response => ({ type: 'MODEL_NAME', response }),
    modelDate: response => ({ type: 'MODEL_DATE', response }),
    modelSettings: response => ({ type: 'MODEL_SETTINGS', response }),
    modelPronunciationFile: response => ({ type: 'MODEL_PRONUNCIATION_FILE', response }),

    newTranscriptionFile: response => ({ type: 'NEW_TRANSCRIPTION_FILE', response })
}

// * * * * * * * * * * DATA BUNDLES * * * * * * * * * * * * * * *

export const dataBundleNew = () => {
    const url = baseUrl + '/api/data-bundle/new';
    return postApi(url, null, 'dataBundleNew');
}

export const dataBundleName = postData => {
    console.log("ACTION data bundle name", postData)
    const url = baseUrl + '/api/data-bundle/name';
    return postApi(url, postData, 'dataBundleName');
}

export const dataBundleDate = postData => {
    const url = baseUrl + '/api/data-bundle/date';
    return postApi(url, postData, 'dataBundleDate');
}

// TODO: change url to /api/data-bundle/files
export const dataBundleFiles = postData => {
    const url = baseUrl + '/api/model/transcription-files';
    const headers = {headers: {'content-type': 'multipart/form-data'}}
    return postApi(url, postData, 'dataBundleFiles', headers);
}

export const dataBundleSettings = postData => {
    const url = baseUrl + '/api/data-bundle/settings';
    return postApi(url, postData, 'dataBundleSettings');
}


// should this be GET or POST some kind of trigger and return response?
export const dataBundleClean = () => {
    const url = baseUrl + '/api/data-bundle/clean';
    return getApi(url, 'dataBundleClean');
}
// GET_CLEANED_DATA_BUNDLE




// * * * * * * * * * * MODEL * * * * * * * * * * * * * * *

export const modelNew = () => {
    const url = baseUrl + '/api/model/new';
    return postApi(url, null, 'modelNew');
}

export const modelName = postData => {
    const url = baseUrl + '/api/model/name';
    return postApi(url, postData, 'modelName');
}

export const modelDate = postData => {
    const url = baseUrl + '/api/model/date';
    return postApi(url, postData, 'modelDate');
}

export const modelPronunciation = postData => {
    const url = baseUrl + '/api/model/pronunciation';
    const headers = {headers: {'content-type': 'multipart/form-data'}}
    return postApi(url, postData, 'modelPronunciation', headers);
}

export const modelLexicon = () => {
    const url = baseUrl + '/api/model/lexicon';
    return getApi(url, 'modelLexicon');
}
// GET_MODEL_LEXICON

export const modelSettings = postData => {
    const url = baseUrl + '/api/model/settings';
    return postApi(url, postData, 'modelSettings');
}

// get or post?
export const modelTraining = () => {
    const url = baseUrl + '/api/model/train';
    return postApi(url, 'modelTraining');
}

// need a model id?
export const modelTrainingResults = () => {
    const url = baseUrl + '/api/model/results';
    return postApi(url, 'modelTrainingResults');
}




// * * * * * * * * * * TRANSCRIPTION * * * * * * * * * * * * * * *

export const transcriptionNew = postData => {
    // const url = "http://httpbin.org/post"
    const url = baseUrl + '/api/transcription/audio';
    const headers = {headers: {'content-type': 'multipart/form-data'}}
    return postApi(url, postData, 'transcriptionNew', headers);
}

// TODO: action to download Elan file

// TODO: action to download PRAAT file


// * * * * * * * * * * GENERAL * * * * * * * * * * * * * * *

export const setCurrentStep = (url) => ({ type: 'SET_CURRENT_STEP', url })

export const replaceFiles = (status) => ({ type: 'REPLACE_FILES', status })

export const triggerApiWaiting = (message) => ({ type: 'TRIGGER_API_WAITING', message })
