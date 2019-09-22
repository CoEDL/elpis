const toyLexicon = `!SIL sil
<UNK> spn
di d I
kaai k a: I
amakaang a m a k a: ŋ
hada h a d a
muila m u I l a
`;

const initState = {
    modelList: [],
    name: '',
    datasetName: '',
    pronDictName: '',
    date: null,
    l2s: '',
    lexicon: '',
    results: null,
    settings: {
        ngram: 1
    },
    status: 'ready',
    apiWaiting: {status: false, message: 'something'}
}

const model = (state = initState, action) => {
    switch (action.type) {


        case 'MODEL_LIST':
            return {
                ...state,
                modelList: action.response.data.data
            }

        case 'MODEL_LOAD':
        case 'MODEL_NEW':
            return {
                ...state,
                name: action.response.data.data.config.name,
                l2s: action.response.data.data.l2s,
                status: 'ready',
                lexicon: 'No lexicon yet',
                datasetName: action.response.data.data.config.dataset_name,
                pronDictName: action.response.data.data.config.pron_dict_name,
                settings: {...state.settings, ngram: action.response.data.data.config.ngram}
            }

        case 'MODEL_NAME':
            return {
                    ...state,
                    name: action.response.data.data.name
                }

        case 'MODEL_L2S':
            return {
                ...state,
                l2s: action.response.data
            }

        case 'MODEL_LEXICON':
            return {
                ...state,
                lexicon: action.response.data
            }

        case 'MODEL_SETTINGS':
            return {
                ...state,
                settings: action.response.data.data
            }

        case 'MODEL_TRAIN':
            return {
                ...state,
                status: action.response.data.data
            }

        case 'MODEL_RESULTS':
            return {
                ...state,
                results: action.response.data.data
            }

        case 'MODEL_STATUS':
            return {
                ...state,
                status: action.response.data.data
            }

        default:
            return state;
    }
}

export default model;