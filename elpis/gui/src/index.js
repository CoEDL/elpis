import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './components/App';
import * as serviceWorker from './serviceWorker';


import { Provider } from 'react-redux'
// import { PersistGate } from 'redux-persist/integration/react'
import store from './redux/store'

import {I18nextProvider} from 'react-i18next';
import i18next from 'i18next';
import common_en from "./translations/en/common.json";
import common_fr from "./translations/fr/common.json";

// We should add soon a language selection button (with dynamic text switching) and keep this code for best default language detection…
let available_languages = ['en', 'fr']; // Should be better to make it dynamic (folder names in translation?) and non redundant with i18next.init below.
let favorite_languages = Array.from(navigator.languages);
if(!favorite_languages.includes('en')){favorite_languages.push('en');}
let favorite_language = favorite_languages.filter(language => available_languages.includes(language))[0];

i18next.init({
  interpolation: { escapeValue: false },  // React already does escaping
  lng: favorite_language,                              // language to use
  resources: {
      en: {
          common: common_en               // 'common' is our custom namespace
      },
      fr: {
          common: common_fr               // 'common' is our custom namespace
      }
    }
});

ReactDOM.render(
      <Provider store={store}>
          <I18nextProvider i18n={i18next}>
          <App />
        </I18nextProvider>
      </Provider>,
    document.getElementById('root')
  );

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();

