import React, { Component } from 'react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';


class ChooseTranscriptionModel extends Component {

    render() {

    return (
        <pre>
            Choose a model:
                import
                use existing
                train a new model
        </pre>
        )
    }
}

const mapStateToProps = state => {
    return {
    }
}

const mapDispatchToProps = dispatch => ({
})

export default
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(ChooseTranscriptionModel)
    )
