import common_en from "./en-GB/common.json";
import common_fr from "./fr/common.json";
import common_hin from "./hin/common.json";

let languages = {
    "en-GB": {
        common: common_en, // 'common' is our custom namespace
    },
    fr: {
        common: common_fr, // 'common' is our custom namespace
    },
    hin: {
        common: common_hin, // 'common' is our custom namespace
    },
};

export default languages;
