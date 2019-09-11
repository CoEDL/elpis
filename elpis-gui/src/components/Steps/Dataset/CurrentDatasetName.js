import React, { Component } from 'react'
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';
import urls from 'urls'

class CurrentDatasetName extends Component {

    render() {
        const { t, name, match } = this.props

        const link = (match.url !== urls.gui.dataset.index) ? (
            <>
            &nbsp;
            <Link to={urls.gui.dataset.index}>
                { t('common.chooseOrNewLabel') }
            </Link>
            </>
        ) : (
            <>&nbsp; { t('common.selectOneBelow') }</>
        )

        const current = name ?
        (
            <Message color='olive'>
                { t('dataset.common.currentDatasetLabel') + name }
            </Message>
        ) : (
            <Message negative>
                { t('dataset.common.noCurrentDatasetLabel') }
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
        name: state.dataset.name
    }
}
export default withRouter(
    connect(mapStateToProps)(
        translate('common')(CurrentDatasetName)
    )
)