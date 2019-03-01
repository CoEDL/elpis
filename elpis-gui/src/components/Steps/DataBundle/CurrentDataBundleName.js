import React, { Component } from 'react'
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';
import urls from 'urls'

class CurrentDataBundleName extends Component {

    render() {
        const { t, name, match } = this.props

        const link = (match.url !== urls.gui.dataBundle.index) ? (
            <>
            &nbsp;
            <Link to={urls.gui.dataBundle.index}>
                { t('common.chooseOrNewLabel') }
            </Link>
            </>
        ) : (
            <>&nbsp; { t('common.selectOneBelow') }</>
        )

        const current = name ?
        (
            <Message color='olive'>
                { t('dataBundle.common.currentDataBundleLabel') + name }
            </Message>
        ) : (
            <Message negative>
                { t('dataBundle.common.noCurrentDataBundleLabel') }
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
        name: state.dataBundle.name
    }
}
export default withRouter(
    connect(mapStateToProps)(
        translate('common')(CurrentDataBundleName)
    )
)