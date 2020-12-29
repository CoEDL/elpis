import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';
import languages from "./translations/languages";

i18n
    .use(Backend)
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        fallbackLng: 'en-GB',
        debug: true,
        react: {
            useSuspense: false,
        },
        interpolation: {
            escapeValue: false, // not needed for react as it escapes by default
        },
        resources: languages
    });


export default i18n;
