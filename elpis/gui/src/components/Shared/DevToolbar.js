import React, { Component } from 'react';
import { translate } from 'react-i18next';
import SelectEngine from 'components/Engine/SelectEngine'
import urls from 'urls';

const DevToolbar = props => {
    return props.dev_mode ? (
        <div className="dev-toolbar">
            <p>DEV MODE</p>
            <SelectEngine />
        </div>
    ) : (
        <></>
    )
}


export default translate('common')(DevToolbar)
