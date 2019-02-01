import axios from 'axios'

// Use beeceptor to test API endpoints
const baseUrl = 'https://elpis.free.beeceptor.com'
// const baseUrl = 'http://127.0.0.1:5000'

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
  return dispatch => {
    axios.post(url, postData)
      .then((response) => {
        dispatch(successHandler[successFunction](response))
      }).catch((error) => {
        dispatch(errorHandler(error))
      })
  }
}

const errorHandler = {}

var successHandler = {
    updateModelName:                response => ({ type: 'UPDATE_MODEL_NAME', response }),
    updateModelDate:                response => ({ type: 'UPDATE_MODEL_DATE', response }),
    updateModelSettings:            response => ({ type: 'UPDATE_MODEL_SETTINGS', response }),
    updateModelTranscriptionFiles:  response => ({ type: 'UPDATE_MODEL_TRANSCRIPTION_FILES', response }),
    updateModelAdditionalWordFiles: response => ({ type: 'UPDATE_MODEL_ADDITIONAL_WORD_FILES', response }),
    updateModelPronunciationFile:   response => ({ type: 'UPDATE_MODEL_PRONUNCIATION_FILE', response }),

}

export const updateModelName = postData => {
  const url = baseUrl + '/corpus/name';
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
  const url = baseUrl + '/files';
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
