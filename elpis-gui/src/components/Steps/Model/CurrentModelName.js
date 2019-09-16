import React, { Component } from 'react'
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';
import urls from 'urls'

class CurrentModelName extends Component {

    render() {
        const { t, datasetName, pronDictName, name, match } = this.props

        const link = (match.url !== urls.gui.model.index) ? (
            <Link to={urls.gui.model.index}>
                { t('common.chooseOrNewLabel') }
            </Link>
        ) : (
            t('common.selectOneBelow')
        )

        const current = name ?
        (
            <Message color='olive'>
                    {t('dataset.common.currentDatasetLabel') + datasetName}
                    <br />
                    {t('pronDict.common.currentPronDictLabel') + pronDictName}
                    <br />
                { t('model.common.currentModelLabel') + name }
            </Message>
        ) : (
            <Message negative>
                { t('model.common.noCurrentModelLabel') }
                <br />
                { link }
            </Message>
        )

        return (
            <>{ current }</>
        )
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name,
        datasetName: state.model.datasetName,
        pronDictName: state.model.pronDictName
    }
}
export default withRouter(
    connect(mapStateToProps)(
        translate('common')(CurrentModelName)
    )
)