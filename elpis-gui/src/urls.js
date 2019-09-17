export default {
    "gui": {
        "dataset": {
            "index": "/dataset",
            "new": "/dataset/new",
            "files": "/dataset/files",
            "prepare": "/dataset/prepare",
            "prepareError": "/dataset/prepare/error"
        },
        "pronDict": {
            "index": "/pron-dict",
            "new": "/pron-dict/new",
            "l2s": "/pron-dict/l2s",
            "lexicon": "/pron-dict/lexicon"
        },
        "model": {
            "index": "/model",
            "new": "/model/new",
            "settings": "/model/settings",
            "train": "/model/train",
            "results": "/model/results",
            "error": "/model/error"
        },
        "transcription": {
            "new": "/transcription/new",
            "results": "/transcription/results"
        }
    },
    "api": {
        "config": {
            "reset": "/api/config/reset"
        },
        "dataset": {
            "load": "/api/dataset/load",
            "list": "/api/dataset/list",
            "name": "/api/dataset/name",
            "new": "/api/dataset/new",
            "name": "/api/dataset/name",
            "settings": "/api/dataset/settings",
            "files": "/api/dataset/files",
            "prepare": "/api/dataset/prepare"
        },
        "pronDict": {
            "load": "/api/pron-dict/load",
            "list": "/api/pron-dict/list",
            "name": "/api/pron-dict/name",
            "new": "/api/pron-dict/new",
            "l2s": "/api/pron-dict/l2s",
            "lexicon": "/api/pron-dict/lexicon",
            "generateLexicon": "/api/pron-dict/generate-lexicon",
            "saveLexicon": "/api/pron-dict/save-lexicon"
        },
        "model": {
            "load": "/api/model/load",
            "list": "/api/model/list",
            "name": "/api/model/name",
            "new": "/api/model/new",
            "settings": "/api/model/settings",
            "train": "/api/model/train",
            "status": "/api/model/status",
            "results": "/api/model/results",
            "logstream": "/api/logstream"
        },
        "transcription": {
            "new": "/api/transcription/new",
            "transcribe": "/api/transcription/transcribe",
            "transcribe_align": "/api/transcription/transcribe-align",
            "status": "/api/transcription/status",
            "text": "/api/transcription/text",
            "elan": "/api/transcription/elan"
        }
    }
}