import React, { Component } from 'react'
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';

class CurrentDataBundleName extends Component {

    render() {
        const { t, name } = this.props

        const current = name ?
        (
            <Message>
                { t('dataBundle.common.currentDataBundleLabel') + name }
            </Message>
        ) : (
            <Message negative>
                { t('dataBundle.common.noCurrentDataBundleLabel') }
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
export default connect(mapStateToProps)(translate('common')(CurrentDataBundleName))
