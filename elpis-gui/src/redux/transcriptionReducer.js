const initState = {
    newTranscriptionFile: ''
}

const transcription = (state = initState, action) => {
    switch (action.type) {
        case 'UPDATE_NEW_TRANSCRIPTION_FILE':
            console.log("reducer got", action)
            // TODO: will we put this into separate reducer ??
            let newTranscriptionFile = action.response.data
            return {
                ...state,
                newTranscriptionFile
            }

        default:
            return state;
    }
}

export default transcription;