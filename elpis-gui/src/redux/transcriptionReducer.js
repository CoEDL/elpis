const initState = {
    transcriptionAudio: ''
}

const transcription = (state = initState, action) => {
    switch (action.type) {
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