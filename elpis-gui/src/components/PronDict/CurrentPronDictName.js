import React, { Component } from 'react'
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';
import urls from 'urls'

class CurrentPronDictName extends Component {

    render() {
        const { t, datasetName, name, match } = this.props

        const link = (match.url !== urls.gui.pronDict.index) ? (
            <Link to={urls.gui.pronDict.index}>
                { t('common.chooseOrNewLabel') }
            </Link>
        ) : (
            t('common.selectOneBelow')
        )

        const current = name ?
        (
            <Message color='olive'>
                {t('dataset.common.currentDatasetLabel') + datasetName }
                <br />
                {t('pronDict.common.currentPronDictLabel') + name }
            </Message>
        ) : (
            <Message color='purple'>
                { t('pronDict.common.noCurrentPronDictLabel') }
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
        name: state.pronDict.name,
        datasetName: state.dataset.name
    }
}
export default withRouter(
    connect(mapStateToProps)(
      translate('common')(CurrentPronDictName)
    )
)