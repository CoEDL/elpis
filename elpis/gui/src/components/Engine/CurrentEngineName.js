import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { connect } from 'react-redux';
import { withTranslation } from 'react-i18next';
import { Message } from 'semantic-ui-react';

class CurrentEngineName extends Component {

    render() {
        const { t, engine_name } = this.props;

        const current = engine_name ?
        (
            <Message color='olive'>
                { t('engine.common.currentEngineLabel') + engine_name }
            </Message>
        ) : (
            <Message color='purple'>
                { t('engine.common.noCurrentEngineLabel') }
            </Message>
        );

        return (
            <>{ current }</>
        );
    }
}

const mapStateToProps = state => {
    return {
        engine_name: state.engine.engine,
    };
};
export default withRouter(
    connect(mapStateToProps)(
        withTranslation("common")(CurrentEngineName)
    )
);
