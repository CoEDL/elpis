import React, { Component } from 'react';
import { translate } from 'react-i18next';
import SelectEngineList from 'components/Engine/SelectEngineList'
import urls from 'urls';

const DevToolbar = props => {
    return props.dev_mode ? (
        <div className="dev-toolbar">
            <p>DEV MODE</p>
            <SelectEngineList />
        </div>
    ) : (
        <></>
    )
}


export default translate('common')(DevToolbar)
