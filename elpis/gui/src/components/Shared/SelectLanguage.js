import React, { useEffect } from 'react';
import {Dropdown} from 'semantic-ui-react';
import {useTranslation} from "react-i18next";
import i18next from "i18next";


const SelectLanguage = () => {
    const { t, i18n } = useTranslation('common');
    const languages = Object.keys(i18next.services.resourceStore.data);
    const options = languages.map((name) => ({key: name, text: name, value: name}));

    let handleChange = (_event, data) => {
        let newLang = data.value;
        i18n.changeLanguage(newLang)
            .then(() => console.log(`Changed language to ${newLang}.`))
            .catch(() => console.log("Failed to change language."));
    };

    return (
        <Dropdown
            placeholder={t('Language')}
            selection
            options={options}
            value={i18n.language}
            onChange={handleChange}
        />

    );
};

export default SelectLanguage;
