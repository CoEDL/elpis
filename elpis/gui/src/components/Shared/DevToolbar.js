import React, { Component } from 'react';
import { translate } from 'react-i18next';
import SelectEngineDropdown from 'components/Engine/SelectEngineDropdown'
import urls from 'urls';

const DevToolbar = props => {
    return props.dev_mode ? (
        <div className="dev-toolbar">
            <p>DEV MODE</p>
            <SelectEngineDropdown />
        </div>
    ) : (
        <></>
    )
}


export default translate('common')(DevToolbar)
