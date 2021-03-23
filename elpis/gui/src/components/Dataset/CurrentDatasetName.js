import React, {Component} from "react";
import {Link, withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {Message} from "semantic-ui-react";
import SelectEngineDropdown from "components/Engine/SelectEngineDropdown";
import urls from "urls";

class CurrentDatasetName extends Component {
    render() {
        const {t, currentEngine, engineHumanNames, name, datasetList, match} = this.props;

        const onDashboard = (match.url === urls.gui.dataset.index);
        const engineHumanName = currentEngine ? engineHumanNames[currentEngine] : "";

        return (
            <>
                {name &&
                <Message color="olive">
                    {t("engine.common.currentEngineLabel") + engineHumanName}
                    <br />
                    {t("dataset.common.currentDatasetLabel") + name}
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
                    {onDashboard && datasetList.length === 0 &&
                        t("common.makeNewOne")
                    }
                    {onDashboard && datasetList.length > 0 &&
                        t("common.selectOneBelow")
                    }
                    {!onDashboard &&
                        <>
                            <p>{t("dataset.common.noCurrentDatasetLabel")}</p>
                            <Link to={urls.gui.dataset.index}>
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
        name: state.dataset.name,
        datasetList: state.dataset.datasetList,
        currentEngine: state.engine.engine,
        engineHumanNames: state.engine.engine_human_names,
    };
};
export default withRouter(
    connect(mapStateToProps)(
        withTranslation("common")(CurrentDatasetName)
    )
);
