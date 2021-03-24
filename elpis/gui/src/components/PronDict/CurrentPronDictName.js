import React, {Component} from "react";
import {Link, withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {Message} from "semantic-ui-react";
import SelectEngineDropdown from "components/Engine/SelectEngineDropdown";
import urls from "urls";

class CurrentPronDictName extends Component {
    render() {
        const {t, currentEngine, engineHumanNames, pronDictList, datasetName, name, match} = this.props;
        const onDashboard = (match.url === urls.gui.pronDict.index) ? true : false;
        const engineHumanName = currentEngine ? engineHumanNames[currentEngine] : "";

        return (
            <>
                {name &&
                    <Message color="olive">
                        {t("engine.common.currentEngineLabel") + engineHumanName}
                        <br />
                        {t("pronDict.common.currentPronDictLabel") + name}
                        <br />
                        {t("dataset.common.currentDatasetLabel") + datasetName}
                    </Message>
                }
                {!currentEngine &&
                    <Message color="purple">
                        {t("engine.common.noCurrentEngineLabel")}
                        <SelectEngineDropdown />
                    </Message>
                }
                {currentEngine && !name &&
                    <Message color="purple">
                        {onDashboard && pronDictList.length === 0 &&
                        t("common.makeNewOne")
                    }
                        {onDashboard && pronDictList.length > 0 &&
                        t("common.selectOneBelow")
                    }
                        {!onDashboard &&
                            <>
                                <p>{t("pronDict.common.currentPronDictLabel")}</p>
                                <Link to={urls.gui.pronDict.index}>
                                    {t("common.chooseOrNewLabel")}
                                </Link>
                            </>
                    }
                    </Message>
                }
            </>
        );
    }
}


const mapStateToProps = state => {
    return {
        name: state.pronDict.name,
        datasetName: state.dataset.name,
        pronDictList: state.pronDict.pronDictList,
        currentEngine: state.engine.engine,
        engineHumanNames: state.engine.engine_human_names,
    };
};

export default withRouter(
    connect(mapStateToProps)(
        withTranslation("common")(CurrentPronDictName)
    )
);
