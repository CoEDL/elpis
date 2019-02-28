const initState = {
    audioFile: '',
    elan: null,
    status: 'ready'
}

const transcription = (state = initState, action) => {

    switch (action.type) {
        case 'TRANSCRIPTION_NEW':
            console.log("transcription reducer got", action.response)
            return {
                ...state,
                status: action.response.data.data,
            }

        case 'TRANSCRIPTION_ELAN':
            return {
                ...state,
                elan: action.response.data
            }

        case 'TRANSCRIPTION_AUDIO':
            console.log("TRANSCRIPTION_AUDIO action", action)
            return {
                ...state,
                audioFile: action.audioFile,
                status: 'ready'
            }

        case 'TRANSCRIPTION_STATUS':
            console.log("TRANSCRIPTION_STATUS", action.response.data.data)
            return {
                ...state,
                status: action.response.data.data
            }
        default:
            return state;
    }
}

export default transcription;