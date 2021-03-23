import React, {Component} from "react";
import {Dropdown} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {engineLoad} from "redux/actions/engineActions";

class SelectEngineDropdown extends Component {
    render() {
        let {t, currentEngine, engineHumanNames, list, _engineLoad} = this.props;

        let handleChange = (_event, data) => {
            let engine_name = data.value;
            let postData = {engine_name};

            _engineLoad(postData);
        };

        let options = list.map((name) => ({key: name, text: engineHumanNames[name], value: name}));

        return (
            <>
                {list.length === 0 &&
                    <p>{t("engine.select.waitingForEngineList")}</p>
                }
                {list.length > 0 &&
                    <Dropdown
                        className="engine-select"
                        placeholder={currentEngine ? currentEngine : t("engine.select.shortcutPlaceholder")}
                        selection
                        options={options}
                        value={currentEngine}
                        onChange={handleChange}
                    />
                }
            </>
        );
    }
}

const mapStateToProps = state => {
    return {
        list: state.engine.engine_list,
        currentEngine: state.engine.engine,
        engineHumanNames: state.engine.engine_human_names,
    };
};
const mapDispatchToProps = dispatch => ({
    _engineLoad: postData => {
        dispatch(engineLoad(postData));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(SelectEngineDropdown)
);
