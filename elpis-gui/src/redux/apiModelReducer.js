const initialModelState = {
    name: "",
    audioFiles: [],
    transcriptionFiles: [],
    additionalTextFiles: [],
    pronunciationFile: null,
    settings: {
        frequency: null,
        mfcc: null,
        ngram: null,
        beam: null,
    },
    date: null
}

function getFileExtension(filename) {
    filename = filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2)
    return filename
}

const model = (state = initialModelState, action) => {
    switch (action.type) {
        case 'UPDATE_MODEL_NAME':
            return {
                ...state, name: action.response.data.name
            }
        case 'UPDATE_MODEL_DATE':
            return {
                ...state
            }
        case 'UPDATE_MODEL_SETTINGS':
            return {
                ...state
            }
        case 'UPDATE_MODEL_TRANSCRIPTION_FILES':
            console.log('reducer UPDATE_MODEL_TRANSCRIPTION_FILES', action)
            // action.data is an array of filenames
            // parse this, split into separate lists
            let audioFiles = action.response.data.filter(file => getFileExtension(file) === 'wav')
            let transcriptionFiles = action.response.data.filter(file => getFileExtension(file) === 'eaf')
            let additionalTextFiles = action.response.data.filter(file => getFileExtension(file) === 'txt')

            audioFiles.sort()
            transcriptionFiles.sort()
            additionalTextFiles.sort()

            console.log(audioFiles, transcriptionFiles, additionalTextFiles)

            return {
                ...state,
                audioFiles,
                transcriptionFiles,
                additionalTextFiles
            }

        case 'UPDATE_MODEL_ADDITIONAL_WORD_FILES':
            return {
                ...state
            }
        case 'UPDATE_MODEL_PRONUNCIATION_FILE':
            return {
                ...state
            }
        default:
            return state;
    }
}

export default model;