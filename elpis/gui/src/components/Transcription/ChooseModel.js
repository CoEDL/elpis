import React, {Component} from "react";
import {Link, withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {Button, Divider, Grid, Header, Segment, Loader} from "semantic-ui-react";
import {modelLoad, modelList, modelUpload, modelUploadStatusReset} from "redux/actions/modelActions";
import {datasetLoad} from "redux/actions/datasetActions";
import {engineLoad} from "redux/actions/engineActions";
import {pronDictLoad} from "redux/actions/pronDictActions";
import Branding from "components/Shared/Branding";
import urls from "urls";
import Dropzone from "react-dropzone";
import {fromEvent} from "file-selector";
import classNames from "classnames";

const UPLOAD_STATUS = {
	NOT_STARTED: "not_started",
	STARTED: "started",
	FINISHED: "finished",
	ERROR: "error",
};

class ChooseModel extends Component {
    redirectOnUploadFinish = () => {
        if (this.props.uploadStatus === UPLOAD_STATUS.FINISHED) {
            this.props._modelUploadFinished();
            this.props.history.push(urls.gui.transcription.new);
        }
    }

    componentDidMount() {
        this.redirectOnUploadFinish();
        this.props._modelList();
    }

    componentDidUpdate() {
        this.redirectOnUploadFinish();
    }

    handleSelectModel = (model_name) => {
        const {history, list, _modelLoad} = this.props;
        var selectedModel = list.filter(m => m.name === model_name);
        const modelData = {name: selectedModel[0].name};
        const datasetData = {name: selectedModel[0].dataset_name};
        const engineName = {engine_name: selectedModel[0].engine_name};
        const pronDictData = {name: selectedModel[0].pron_dict_name};

        _modelLoad(modelData, datasetData, engineName, pronDictData);
        history.push(urls.gui.transcription.new);
    }

    onDrop = (acceptedFiles) => {
        var formData = new FormData();

        formData.append("file", acceptedFiles[0]);
        this.props._modelUpload(formData);
        this.setState({uploadStatus: "started"});
    }


    render() {
        const {t, list, uploadStatus} = this.props;

        console.log("Upload Status: ", uploadStatus);
        console.log("list", list);

        const modelList = (list ?? []).map((model, index) => {
            return (
                <Button key={index} onClick={() => this.handleSelectModel(model.name)}>
                    {model.name}
                </Button>
            );
        });

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Row>
                            <Grid.Column>
                                <Header as="h1" text="true">
                                    {t("transcription.choose_model.title")}
                                </Header>
                                {list.length > 0 &&
                                    <>
                                        <Divider />
                                        <p>{t("transcription.choose_model.use_existing")}</p>
                                        <div>
                                            {modelList}
                                        </div>
                                    </>
                                }
                                <Divider />
                                {list.length === 0 &&
                                    t("transcription.choose_model.no_models_found")
                                }
                                <Link to={urls.gui.engine.index}>
                                    {t("transcription.choose_model.train_new")}
                                </Link>
                                <Divider />
                                {(uploadStatus === "not_started" || uploadStatus === "finished") && 
                                    <div className="FileUpload">
                                        <Dropzone
                                            className="dropzone"
                                            onDrop={this.onDrop}
                                            getDataTransferItems={evt => fromEvent(evt)}
                                        >
                                            {({getRootProps, getInputProps}) => {
                                                    return (
                                                        <div
                                                            {...getRootProps()}
                                                            className={classNames("dropzone", {
                                                                dropzone_active: true,
                                                            })}
                                                        >
                                                            <input {...getInputProps()} />
                                                            <p>
                                                                {t("transcription.choose_model.upload_model")}
                                                            </p>
                                                        </div>
                                                    );
                                                }}
                                        </Dropzone>
                                    </div>
                                }
                                {uploadStatus === "started" && 
                                    <>
                                        <Loader indeterminate active>
                                            The zipped model is being uploaded.
                                        </Loader>
                                    </>
                                }
                                {uploadStatus === "error" && 
                                    <>
                                        <p>
                                            Error in uploading zipped model.
                                        </p>
                                        <Button
                                            onClick={
                                            () => this.setState({uploadStatus: "not_started"})
                                            }
                                        >
                                        </Button>
                                    </>
                                }

                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        list: state.model.modelList,
        currentEngine: state.engine.engine,
        uploadStatus: state.model.uploadStatus,
    };
};
const mapDispatchToProps = dispatch => ({
    _modelList: () => {
        dispatch(modelList());
    },
    _modelUpload: formData => {
        dispatch(modelUpload(formData));
    },
    _modelUploadFinished: () => {
        dispatch(modelUploadStatusReset());
    },
    _modelLoad: (modelData, datasetData, engineName, pronDictData) => {
        dispatch(engineLoad(engineName))
            .then(() => dispatch(modelLoad(modelData)))
            .then(() => {
                if (datasetData.name) {
                    dispatch(datasetLoad(datasetData));
                }
            })
            .then(() => {
                if (pronDictData.name) {
                    dispatch(pronDictLoad(pronDictData));
                }
            });
    },
});

export default withRouter(
    connect(mapStateToProps, mapDispatchToProps)(
        withTranslation("common")(ChooseModel)
    )
);
