import React, {Component} from "react";
import PropTypes from "prop-types";
import {Link} from "react-router-dom";
import {
  Accordion,
  Grid,
  Header,
  Segment,
  Icon,
  Card,
  Button,
  Message,
  Loader,
} from "semantic-ui-react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import ReactTimeout from "react-timeout";
import {
  modelTrain,
  modelStatus,
  modelGetLogs,
} from "redux/actions/modelActions";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import CurrentModelName from "./CurrentModelName";
import urls from "urls";
import downloadjs from "downloadjs";

class ModelTrain extends Component {
  state = {
    statusInterval: null,
    activeIndex: null,
  };

  componentDidMount = () => {};

  handleModelTrain = () => {
    this.props.modelTrain();
    this.setState({
      ...this.state,
      statusInterval: this.props.setInterval(this.handleModelStatus, 1000),
    });
  };

  handleModelStatus = () => {
    const {status, modelStatus, modelGetLogs} = this.props;

    modelStatus();
    modelGetLogs();

    if (status === "trained" || status === "error")
      this.props.clearInterval(this.state.statusInterval);
  };

  handleLogDownload = () => {
    const {log, modelGetLogs} = this.props;

    modelGetLogs();

    downloadjs(log, "log.txt", "text/txt");
  };

  onScroll = () => {};

  follow = () => {};

  selectAccordion = (i) => {
    this.setState({...this.state, activeIndex: i});
  };

  render() {
    const {t, currentEngine, name, settings, status, stage_status, log} =
      this.props;

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={4}>
                            <SideNav />
                        </Grid.Column>
                        <Grid.Column width={12}>
                            <Header as="h1" text="true">
                                {t("model.train.title")}
                            </Header>
                            <CurrentModelName />
                            {!currentEngine && (
                                <p>{t("engine.common.noCurrentEngineLabel")}</p>
                            )}
                            {currentEngine && !name && (
                                <p>{t("model.common.noCurrentModelLabel")}</p>
                            )}
                            {currentEngine && name && (
                                <>
                                    {/* Only Kaldi has settings. Should make this dynamic */}
                                    {currentEngine && currentEngine === "kaldi" && (
                                        <Card fluid>
                                            <Card.Content header={t("model.train.settingsHeader")} />
                                            <Card.Content
                                                description={
                                                    t("model.settings.ngramLabel") + " " + settings.ngram
                                                }
                                            />
                                        </Card>
                                    )}
                                    <Message icon>
                                        <Message.Content className="train-log">
                                            {stage_status && (
                                                <div className="stages">
                                                    <Accordion fluid styled exclusive={false}>
                                                        {Object.keys(stage_status).map((stage, i) => {
                                                            let name = stage_status[stage]["name"];
                                                            let status = stage_status[stage]["status"];
                                                            let log = stage_status[stage]["log"];
                                                            let icon =
                                                                status === "in-progress" ? (
                                                                    <Icon name="circle notched" loading />
                                                                ) : (
                                                                    <Icon name="dropdown" />
                                                                );
                                                            let stage_status_icon =
                                                                status === "complete" ? (
                                                                    <Icon name="check" />
                                                                ) : (
                                                                    ""
                                                                );
                                                            let active =
                                                                this.state.activeIndex === i ||
                                                                status === "in-progress";

                                                            return (
                                                                <div key={name}>
                                                                    <Accordion.Title
                                                                        index={i}
                                                                        active={active}
                                                                        onClick={() => this.selectAccordion(i)}
                                                                    >
                                                                        {icon}
                                                                        {name} {stage_status_icon}
                                                                    </Accordion.Title>
                                                                    <Accordion.Content
                                                                        className="accordion_log"
                                                                        active={this.state.activeIndex === i}
                                                                    >
                                                                        {log}
                                                                    </Accordion.Content>
                                                                </div>
                                                            );
                                                        })}
                                                    </Accordion>
                                                    <StatusIndicator status={status} />
                                                </div>
                                            )}
                                        </Message.Content>
                                    </Message>
                                    <Segment>
                                        <Button
                                            onClick={this.handleModelTrain}
                                            disabled={!name || status !== "ready"}
                                        >
                                            {t("model.train.trainButton")}
                                        </Button>
                                        <Button
                                            as={Link}
                                            to={urls.gui.model.results}
                                            disabled={status === "ready" || status === "training"}
                                        >
                                            {t("common.nextButton")}
                                        </Button>
                                    </Segment>
                                    {/* Logs */}
                                    {status !== "ready" && (
                                        <Segment padded inverted loading={log === null}>
                                            <p style={{overflow: "scroll", height: "300px"}}>
                                                {log}
                                            </p>
                                            <Button
                                                onClick={this.handleLogDownload}
                                                disabled={
                                                    !name ||
                                                    !(status === "trained" || status === "error")
                                                }
                                            >
                                                {t("model.train.logButton")}
                                            </Button>
                                        </Segment>
                                    )}
                                </>
                            )}
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

function StatusIndicator({status}) {
    if (status === "training") {
        return (<Loader size="medium" text>Training</Loader>);
    }

    return (
        <p>{status}</p>
    );
}

StatusIndicator.propTypes = {
    status: PropTypes.string.isRequired,
};


const mapStateToProps = (state) => {
  return {
    name: state.model.name,
    settings: state.model.settings,
    status: state.model.status,
    stage_status: state.model.stage_status,
    currentEngine: state.engine.engine,
    log: state.model.log,
  };
};
const mapDispatchToProps = (dispatch) => ({
  modelTrain: () => {
    dispatch(modelTrain());
  },
  modelStatus: () => {
    dispatch(modelStatus());
  },
  modelGetLogs: () => {
    dispatch(modelGetLogs());
  },
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withTranslation("common")(ReactTimeout(ModelTrain)));
