import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import {Button} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {engineLoad} from "redux/actions/engineActions";
import urls from "urls";


class ChooseEngine extends Component {
    render() {
        let {t, list, _engineLoad, history} = this.props;

        let selectEngine = engine_name => {
            let postData = {engine_name};

            _engineLoad(postData, history);
        };

        let cards = list.map(name => {
            let engine_name, engine_description;

            switch (name) {
                case "kaldi":
                    engine_name = t("engine.common.kaldi_name");
                    engine_description = t("engine.common.kaldi_description");
                    break;
                case "espnet":
                    engine_name = t("engine.common.espnet_name");
                    engine_description = t("engine.common.espnet_description");
                    break;
            }

            return (
                <div key={name} className="row">
                    <div className="left-col choose-engine-button">
                        <Button onClick={() => selectEngine(name)}>{engine_name}</Button>
                    </div>
                    <div className="right-col">
                        <p>{engine_description}</p>
                    </div>
                </div>
            );
        });

        return (
            <>
                {list.length === 0 &&
                    <p>{t("engine.select.waitingForEngineList")}</p>
                }
                <div className="choose-engine">
                    {cards}
                </div>
            </>
        );
    }
}

const mapStateToProps = state => {
    return {
        list: state.engine.engine_list,
        currentEngine: state.engine.engine,
    };
};
const mapDispatchToProps = dispatch => ({
    _engineLoad: (postData, history) => {
        dispatch(engineLoad(postData))
        .then(() => {
            history.push(urls.gui.dataset.index);
        });
    },
});

export default withRouter(
    connect(mapStateToProps, mapDispatchToProps)(
        withTranslation("common")(ChooseEngine)
    )
);
