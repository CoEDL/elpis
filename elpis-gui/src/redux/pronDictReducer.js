const toyLexicon = `!SIL sil
<UNK> spn
di d I
kaai k a: I
amakaang a m a k a: ŋ
hada h a d a
muila m u I l a
`;

const initState = {
    pronDictList: [],
    name: '',
    datasetName: '',
    date: null,
    l2s: '',
    lexicon: '',
    apiWaiting: {status: false, message: 'something'}
}

const pronDict = (state = initState, action) => {
    switch (action.type) {

        case 'TRIGGER_API_WAITING':
            return {
                ...state,
                apiWaiting: {status: true, message: action.message}
            }

        case 'PRON_DICT_LIST':
            return {
                ...state,
                pronDictList: action.response.data.data
            }

        case 'PRON_DICT_NEW':
            console.log("pron dict new", action.response.data.data.config.name)
        case 'PRON_DICT_LOAD':
            console.log("pron dict load", action.response.data.data.config.name)
            return {
                ...state,
                name: action.response.data.data.config.name,
                datasetName: action.response.data.data.config.dataset_name,
                l2s: action.response.data.data.l2s,
                lexicon: action.response.data.data.lexicon,
            }

        case 'PRON_DICT_NAME':
            return {
                    ...state,
                    name: action.response.data.data.name
                }

        case 'PRON_DICT_L2S':
            return {
                ...state,
                l2s: action.response.data
            }

        case 'PRON_DICT_LEXICON':
            return {
                ...state,
                lexicon: action.response.data
            }

        case 'PRON_DICT_SAVE_LEXICON':
            return {
                ...state,
                lexicon: action.response.data
            }
        case 'TEST_UPDATE_LEXICON':
            return {
                ...state,
                lexicon: action.data.lexicon
            }

        default:
            return state;
    }
}

export default pronDict;