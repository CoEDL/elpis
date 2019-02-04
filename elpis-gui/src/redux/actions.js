import axios from 'axios'

const baseUrl = (process.env.REACT_APP_BASEURL) ? process.env.REACT_APP_BASEURL : 'http://127.0.0.1:5000'

console.log('process.env.REACT_APP_BASEURL', process.env.REACT_APP_BASEURL)

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


const postApi = (url, postData, successFunction) => {
    const config = {headers: {'content-type': 'multipart/form-data'}}
    return dispatch => {
        axios.post(url, postData, config)
            .then((response) => {
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
    updateModelName: response => ({ type: 'UPDATE_MODEL_NAME', response }),
    updateModelDate: response => ({ type: 'UPDATE_MODEL_DATE', response }),
    updateModelSettings: response => ({ type: 'UPDATE_MODEL_SETTINGS', response }),
    updateModelTranscriptionFiles: response => ({ type: 'UPDATE_MODEL_TRANSCRIPTION_FILES', response }),
    updateModelAdditionalWordFiles: response => ({ type: 'UPDATE_MODEL_ADDITIONAL_WORD_FILES', response }),
    updateModelPronunciationFile: response => ({ type: 'UPDATE_MODEL_PRONUNCIATION_FILE', response })
}

export const updateModelName = postData => {
    const url = baseUrl + '/api/model/name';
    return postApi(url, postData, 'updateModelName');
}

export const updateModelDate = postData => {
    const url = baseUrl + '/date';
    return postApi(url, postData, 'updateModelDate');
}

export const updateModelSettings = postData => {
    const url = baseUrl + '/settings';
    return postApi(url, postData, 'updateModelSettings');
}

export const updateModelTranscriptionFiles = postData => {
    const url = baseUrl + '/api/model/transcription-files';
    return postApi(url, postData, 'updateModelTranscriptionFiles');
}

export const updateModelAdditionalWordFiles = postData => {
    const url = baseUrl + '/additional_words';
    return postApi(url, postData, 'updateModelAdditionalWordFiles');
}

export const updateModelPronunciationFile = postData => {
    const url = baseUrl + '/pronunciation';
    return postApi(url, postData, 'updateModelPronunciationFile');
}



export const setCurrentStep = (urlParams) => ({ type: 'SET_CURRENT_STEP', urlParams })
