const initState = {
    audioFilename: null,
    status: 'ready',
    text: null,
    elan: null
}

const transcription = (state = initState, action) => {

    switch (action.type) {

        // this just stores the audio filename
        case 'TRANSCRIPTION_AUDIO_FILE':
            return {
                ...state,
                audioFilename: action.filename
            }

        // after uploading the file
        case 'TRANSCRIPTION_PREPARE':
            return {
                ...state,
                status: action.response.data.data,
            }

        case 'TRANSCRIPTION_STATUS':
            return {
                ...state,
                status: action.response.data.data
            }

        case 'TRANSCRIPTION_STATUS_RESET':
            return {
                ...state,
                status: 'ready',
                text: null,
                elan: null
            }


        case 'TRANSCRIPTION_GET_TEXT':
            return {
                ...state,
                text: action.response.data
            }

        case 'TRANSCRIPTION_GET_ELAN':
            return {
                ...state,
                elan: action.response.data
            }

        default:
            return state;
    }
}

export default transcription;