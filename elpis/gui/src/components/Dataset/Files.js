import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { Button, Grid, Header, Icon, List, Message, Segment, Label, Popup } from "semantic-ui-react";
import { connect } from "react-redux";
import { withTranslation } from "react-i18next";
import { datasetSettings, datasetPrepare, datasetDelete } from "redux/actions/datasetActions";
import Branding from "../Shared/Branding";
import SideNav from "../Shared/SideNav";
import FileUpload from "./FileUpload";
import CurrentDatasetName from "./CurrentDatasetName";
import GeneratedUI from "./GeneratedUI";
import urls from "urls";

class DatasetFiles extends Component {

    handleNextButton = () => {
        const { history, datasetPrepare } = this.props;
        datasetPrepare(history);
        history.push(urls.gui.dataset.prepare);
    }

    handleDeleteButton = (file) => {
        var deleteData = new FormData();
        deleteData.append("file", file);
        this.props.datasetDelete(deleteData);
    }

    createFilesList = (files) => files.map(file => (
        <List.Item key={ file }>
            <Popup content={ file } size="mini" trigger={
                <Button as="div" labelPosition="left" className="file-button">
                    <Label as="a" className="file-label" basic>
                        <div className="file-truncate">{ file }</div>
                    </Label>
                    <Button icon onClick={() => this.handleDeleteButton(file)}>
                        <Icon name="trash" />
                    </Button>
                </Button>
            } />
        </List.Item>
    ));

    render() {
        const { t,
            currentEngine,
            name,
            status,
            audioFiles,
            transcriptionFiles,
            additionalTextFiles,
            settings,
            ui,
            datasetSettings } = this.props;

        const interactionDisabled = name ? false : true;

        const loadingIcon = (status === "loading") ? (
            <div className="status">
                <Icon name="circle notched" size="big" loading /> {t("dataset.fileUpload.uploading")}
            </div>
        ) : null;

        const audioFilesList = this.createFilesList(audioFiles);
        const transcriptionFilesList = this.createFilesList(transcriptionFiles);
        const additionalTextFilesList = this.createFilesList(additionalTextFiles);

        const filesHeader = (
            audioFilesList.length > 0 ||
            transcriptionFilesList.length > 0 ||
            additionalTextFilesList.length > 0) ? (
                 t("dataset.files.filesHeader")
            ) : null;

        const audioFilesHeader = audioFilesList.length > 0
            ? t("dataset.files.audioFilesHeader")
            : null;

        const transcriptionFilesHeader = transcriptionFilesList.length > 0
            ? t("dataset.files.transcriptionFilesHeader")
            : null;

        const additionalTextFilesHeader = additionalTextFilesList.length > 0
            ? t("dataset.files.additionalTextFilesHeader")
            : null;

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as="h1">
                                { t("dataset.files.title") }
                            </Header>

                            <CurrentDatasetName />

                            {!currentEngine &&
                              <p>{ t("engine.common.noCurrentEngineLabel") }</p>
                            }

                            {currentEngine && !name &&
                              <p>{ t("dataset.common.noCurrentDatasetLabel") }</p>
                            }

                            {currentEngine && name &&
                                <>
                                <Message attached content={ t("dataset.files.description") } />
                                <Segment className="attached">

                                    <FileUpload name={name} />

                                    <div>{loadingIcon}</div>

                                    {filesHeader &&
                                        <>
                                        <Header as="h3">
                                            { filesHeader }
                                        </Header>
                                        <div className="file-list">
                                            <Grid columns={3}>
                                                <Grid.Column>
                                                    <Header as="h4">
                                                        { audioFilesHeader }
                                                    </Header>
                                                    <List>
                                                        { audioFilesList }
                                                    </List>
                                                </Grid.Column>
                                                <Grid.Column>
                                                    <Header as="h4">
                                                        { transcriptionFilesHeader }
                                                    </Header>
                                                    <List>
                                                        { transcriptionFilesList }
                                                    </List>
                                                </Grid.Column>
                                                <Grid.Column>
                                                    <Header as="h4">
                                                        { additionalTextFilesHeader }
                                                    </Header>
                                                    <List>
                                                        { additionalTextFilesList }
                                                    </List>
                                                </Grid.Column>
                                            </Grid>
                                        </div>
                                        </>
                                    }
                                </Segment>
                                <br />
                                <Button onClick={this.handleNextButton} disabled={interactionDisabled}>
                                    { t("common.nextButton") }
                                </Button>
                                <Segment>
                                    <Header as="h3">
                                        { t("dataset.files.importSettingsHeader") }
                                    </Header>
                                    <GeneratedUI props={this.props} settings={settings} ui={ui} changeSettingsCallback={datasetSettings} />
                                </Segment>
                                <Button onClick={this.handleNextButton} disabled={interactionDisabled}>
                                    { t("common.nextButton") }
                                </Button>
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
        name: state.dataset.name,
        audioFiles: state.dataset.audioFiles,
        transcriptionFiles: state.dataset.transcriptionFiles,
        additionalTextFiles: state.dataset.additionalTextFiles,
        importer_name: state.dataset.importer_name,
        settings: state.dataset.settings,
        ui: state.dataset.ui,
        status: state.dataset.status,
        currentEngine: state.engine.engine,
    };
};

const mapDispatchToProps = dispatch => ({
    datasetSettings: postData => {
        dispatch(datasetSettings(postData));
    },
    datasetPrepare: (history) => {
        dispatch(datasetPrepare(history))
            .then(() => {
                history.push(urls.gui.dataset.prepare);
            });
    },
    datasetDelete: postData => {
        dispatch(datasetDelete(postData));
    },
});

export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        withTranslation("common")(DatasetFiles)
    )
);
