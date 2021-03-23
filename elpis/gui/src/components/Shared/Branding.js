import React, {Component} from "react";
import {Button, Image, Menu, Segment} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {withTranslation} from "react-i18next";
import elpisLogo from "./elpis.png";
import {connect} from "react-redux";
import {configReset} from "redux/actions/configActions";
import DevToolbar from "./DevToolbar";
import SelectLanguage from "./SelectLanguage";

class StepBranding extends Component {

    reset = () => {
        this.props._configReset();
        window.location.href = "/";
    }

    render() {
        const {t, dev_mode, currentEngine, engineHumanNames} = this.props;

        const engineHumanName = currentEngine ? engineHumanNames[currentEngine] : "";

        return (
            <Segment clearing className="top-nav">
                <Menu secondary>
                    <Menu.Item>
                        <Link to="/">
                            <Image floated="left" src={elpisLogo} className="logo" alt="logo" />
                        </Link>
                    </Menu.Item>
                    <Menu.Item>
                        <Link to="/">
                            Home
                        </Link>
                    </Menu.Item>
                    <Menu.Item>
                        <a href="https://elpis.readthedocs.io/en/latest/index.html" target="docs">
                            Documentation
                        </a>
                    </Menu.Item>
                    <Menu.Item>
                        <DevToolbar dev_mode={dev_mode} />
                    </Menu.Item>
                    <Menu.Item>
                        <SelectLanguage />
                    </Menu.Item>
                    <Menu.Item position="right">
                        {currentEngine &&
                            <div className="current-engine-dot">
                                <span>{engineHumanName}</span>
                            </div>
                        }
                        <Button basic onClick={this.reset}>{t("common.resetButton")}</Button>
                    </Menu.Item>
                </Menu>
            </Segment>
        );
    }
}

const mapStateToProps = state => {
    return {
        currentEngine: state.engine.engine,
        engineHumanNames: state.engine.engine_human_names,
        dev_mode: state.config.app_config.dev_mode,
    };
};

const mapDispatchToProps = dispatch => ({
    _configReset: postData => {
        dispatch(configReset(postData))
            .then(response => console.log("reset OK", response))
            .catch(error => console.log("reset failed", error));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(StepBranding)
);
