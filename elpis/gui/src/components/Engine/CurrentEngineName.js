import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {Message} from "semantic-ui-react";

class CurrentEngineName extends Component {
    render() {
        const {t, engine_name} = this.props;
        const color = engine_name ? "olive" : "purple";
        const message = engine_name ?
            t("engine.common.currentEngineLabel") + engine_name :
            t("engine.common.noCurrentEngineLabel");

        return (
            <Message color={color}>
                {message}
            </Message>
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
