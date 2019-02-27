import React, { Component } from 'react'
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';
import urls from 'urls'

class CurrentModelName extends Component {

    render() {
        const { t, dataBundleName, name, match } = this.props

        const link = (match.url !== urls.gui.model.index) ? (
            <>
            &nbsp;
            <Link to={urls.gui.model.index}>
                { t('model.common.chooseOrNewLabel') }
            </Link>
            </>
        ) : ( null )

        const current = name ?
        (
            <Message color='olive'>
                { t('model.common.currentModelLabel') + name }
                <br />
                { t('dataBundle.common.currentDataBundleLabel') + dataBundleName }
            </Message>
        ) : (
            <Message negative>
                { t('model.common.noCurrentModelLabel') }
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
        dataBundleName: state.model.dataBundleName
    }
}
export default withRouter(
    connect(mapStateToProps)(
        translate('common')(CurrentModelName)
    )
)