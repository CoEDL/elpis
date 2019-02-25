import React, { Component } from 'react'
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { Message } from 'semantic-ui-react';

class CurrentModelName extends Component {

    render() {
        const { t, name } = this.props

        const current = name ?
        (
            <Message>
                { t('model.common.currentModelLabel') + name }
            </Message>
        ) : (
            <Message negative>
                { t('model.common.noCurrentModelLabel') }
            </Message>
        )

        return (
            <>{ current }</>
        )
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name
    }
}
export default connect(mapStateToProps)(translate('common')(CurrentModelName))
