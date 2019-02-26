const initState = {
    transcriptionAudio: '',
    status: '',
    elan: null
}

const transcription = (state = initState, action) => {

    switch (action.type) {
        case 'TRANSCRIPTION_NEW':
            return {
                ...state,
                status: action.response.data.data
            }

        case 'TRANSCRIPTION_ELAN':
            return {
                ...state,
                elan: action.response.data
            }

        case 'TRANSCRIPTION_AUDIO':
            return {
                ...state,
                transcriptionAudio: action.response.data
            }

        default:
            return state;
    }
}

export default transcription;