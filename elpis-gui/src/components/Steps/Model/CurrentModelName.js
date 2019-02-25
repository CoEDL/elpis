import React, { Component } from 'react'
import { connect } from 'react-redux';
import { translate } from 'react-i18next';

class CurrentModelName extends Component {

    render() {
        const { t, name } = this.props

        const current = name ?
        (
            t('model.common.currentModelLabel') + name
        ) : (
            t('model.common.noCurrentModelLabel') +
            ' ' +
            t('model.common.chooseOrNew')
        )

        return (
            <div className="current-name">
                { current }
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name
    }
}
export default connect(mapStateToProps)(translate('common')(CurrentModelName))
