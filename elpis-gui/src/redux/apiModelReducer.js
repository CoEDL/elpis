const initialModelState = {
    name: "",
    audioFiles: [],
    transcriptionFiles: [],
    additionalTextFiles: [],
    pronunciationFile: '',
    settings: {
        frequency: 44100,
        mfcc: 22050,
        ngram: 1,
        beam: 10
    },
    date: null,
    filesOverwrite: false,
    newTranscriptionFile: '',
    apiWaiting: {status: false, message: 'something'}
}

function getFileExtension(filename) {
    filename = filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2)
    return filename
}

const model = (state = initialModelState, action) => {
    switch (action.type) {

        case 'NEW_MODEL':
            // get an id back from response?
            // for now do nothing
            return {
                ...state
            }
        case 'UPDATE_MODEL_NAME':
            return {
                ...state, name: action.response.data.name
            }
        case 'UPDATE_MODEL_DATE':
            return {
                ...state
            }
        case 'UPDATE_MODEL_SETTINGS':
            console.log('UPDATE_MODEL_SETTINGS', action)

            return {
                ...state,
                settings: action.response.data
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

            // decide whether to add to existing, or overwrite
            console.log('audioFiles before', state.filesOverwrite, audioFiles, state.audioFiles)
            // combine received filenames with existing set if filesOverwrite is true
            if (state.filesOverwrite === false && state.audioFiles.length > 0) audioFiles = [...audioFiles, ...state.audioFiles]
            console.log('audioFiles after', audioFiles)
            // remove duplicates
            audioFiles = [...(new Set(audioFiles))];

            // console.log(audioFiles, transcriptionFiles, additionalTextFiles)

            return {
                ...state,
                audioFiles,
                transcriptionFiles,
                additionalTextFiles
            }

        case 'UPDATE_MODEL_PRONUNCIATION_FILE':
            let pronunciationFile = action.response.data
            return {
                ...state,
                pronunciationFile
            }

        case 'UPDATE_NEW_TRANSCRIPTION_FILE':
            console.log("reducer got", action)
            // TODO: will we put this into separate reducer ??
            let newTranscriptionFile = action.response.data
            return {
                ...state,
                newTranscriptionFile
            }

        case 'SET_FILES_OVERWRITE':
            console.log(state.filesOverwrite)
            return {
                ...state,
                filesOverwrite: ! state.filesOverwrite
            }
        default:
            return state;
    }
}

export default model;