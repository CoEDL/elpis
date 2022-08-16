import React, {Component} from "react";
import {Link} from "react-router-dom";
import {Button, Grid, Header, Message, Segment, Tab} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import {fromEvent} from "file-selector";
import {pronDictL2S} from "redux/actions/pronDictActions";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import CurrentPronDictName from "./CurrentPronDictName";
import FrequencyBar from "components/Visualisations/FrequencyBar";
import SankeyWordOrder from "components/Visualisations/SankeyWordOrder";
import urls from "urls";

class PronDictL2S extends Component {
    state = {
        activeTab: 0,
    }

    handleTabChange = (e, {activeIndex}) => this.setState({activeTab: activeIndex})

    onDrop = (acceptedFiles) => {
        console.log("files dropped:", acceptedFiles);

        const {pronDictL2S} = this.props;
        var formData = new FormData();

        formData.append("file", acceptedFiles[0]);
        pronDictL2S(formData);
    }

    render() {
        const {t, currentEngine, l2s, name} = this.props;
        const interactionDisabled = name ? false : true;
        const rawL2s = <pre> { l2s } </pre>;
        const { 
            activeTab,
        } = this.state;
        const panes = [
            {
                menuItem: "File", render: () => <Tab.Pane>{rawL2s}</Tab.Pane>,
            },
            {
                menuItem: "Bar Graph", render: () => 
                    <Tab.Pane>{<FrequencyBar dataUrl={urls.api.statistics.l2sFreq} />}</Tab.Pane>,
            },
            {
                menuItem: "Sankey Graph", render: () => 
                    <Tab.Pane>{<SankeyWordOrder dataUrl={urls.api.statistics.sankeyGraph} />}</Tab.Pane>,
            },
        ];
        const pron = l2s ? 
                    (<Tab
                        activeIndex={activeTab}
                        menu={{secondary: true, pointing: true}}
                        panes={panes}
                        onTabChange={this.handleTabChange}
                     />) : null;

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={4}>
                            <SideNav />
                        </Grid.Column>
                        <Grid.Column width={12}>
                            <Header as="h1">
                                {t("pronDict.l2s.title")}
                            </Header>
                            <CurrentPronDictName />
                            {!currentEngine &&
                                <p>{t("engine.common.noCurrentEngineLabel")}</p>
                            }
                            {currentEngine && !name &&
                                <p>{t("pronDict.common.noCurrentPronDictLabel")}</p>
                            }
                            {currentEngine && name &&
                                <>
                                    <Message content={t("pronDict.l2s.description")} />
                                    {!pron &&
                                        <Segment>
                                            <Dropzone
                                                disabled={interactionDisabled}
                                                className="dropzone"
                                                onDrop={this.onDrop}
                                                getDataTransferItems={evt => fromEvent(evt)}
                                            >
                                                {({getRootProps, getInputProps, isDragActive}) => {
                                                    return (
                                                        <div
                                                            {...getRootProps()}
                                                            className={classNames("dropzone", {
                                                                dropzone_active: isDragActive,
                                                            })}
                                                        >
                                                            <input {...getInputProps()} />
                                                            {isDragActive ?
                                                                <p>{t("pronDict.l2s.dropFilesHintDragActive")}</p> :
                                                                <p>{t("pronDict.l2s.dropFilesHint")}</p>
                                                            }
                                                            <Button>{t("pronDict.l2s.uploadButton")}</Button>
                                                        </div>
                                                    );
                                                }}
                                            </Dropzone>
                                        </Segment>
                                    }
                                    <Button as={Link} to={urls.gui.pronDict.lexicon} disabled={interactionDisabled}>
                                        {t("common.nextButton")}
                                    </Button>
                                    {pron &&
                                        <Segment>
                                            {pron}
                                        </Segment>
                                    }
                                </>
                            }
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        l2s: state.pronDict.l2s,
        name: state.pronDict.name,
        currentEngine: state.engine.engine,
    };
};
const mapDispatchToProps = dispatch => ({
    pronDictL2S: postData => {
        dispatch(pronDictL2S(postData));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(PronDictL2S)
);
