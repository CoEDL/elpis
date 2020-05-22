export default {
    "gui": {
        "dataset": {
            "index": "/dataset",
            "new": "/dataset/new",
            "files": "/dataset/files",
            "prepare": "/dataset/prepare",
            "prepareError": "/dataset/prepare/error",
            "ui": "/dataset/import/ui",
            "settings": "/dataset/import/settings",
            "punctuation_to_explode_by": "/dataset/punctuation_to_explode_by"
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
            "new": "/api/dataset/new",
            "load": "/api/dataset/load",
            "list": "/api/dataset/list",
            "files": "/api/dataset/files",
            "settings": "/api/dataset/settings",
            "prepare": "/api/dataset/prepare"
        },
        "pronDict": {
            "new": "/api/pron-dict/new",
            "load": "/api/pron-dict/load",
            "list": "/api/pron-dict/list",
            "l2s": "/api/pron-dict/l2s",
            "generateLexicon": "/api/pron-dict/generate-lexicon",
            "saveLexicon": "/api/pron-dict/save-lexicon"
        },
        "model": {
            "new": "/api/model/new",
            "load": "/api/model/load",
            "list": "/api/model/list",
            "settings": "/api/model/settings",
            "train": "/api/model/train",
            "status": "/api/model/status",
            "results": "/api/model/results"
        },
        "transcription": {
            "new": "/api/transcription/new",
            "transcribe": "/api/transcription/transcribe",
            "status": "/api/transcription/status",
            "text": "/api/transcription/text",
            "elan": "/api/transcription/elan"
        }
    }
}