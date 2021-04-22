import React, {Component} from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import {Button, Message, MessageHeader} from "semantic-ui-react";
import {fromEvent} from "file-selector";
import {withTranslation} from "react-i18next";
import {datasetFiles} from "redux/actions/datasetActions";
import {connect} from "react-redux";

class FileUpload extends Component {
    constructor(props) {
        super(props);
        this.state = {missingFiles: []};
    }

    parseElan = async (file) => {
        return new Promise((resolve, reject) => {
            const reader = new window.FileReader();

            reader.readAsText(file);
            reader.onload = () => {
                const parser = new window.DOMParser();
                const eafDoc = parser.parseFromString(reader.result, "application/xml");
                const wavUrl = eafDoc
                    .getElementsByTagName("ANNOTATION_DOCUMENT")[0]
                    .getElementsByTagName("HEADER")[0]
                    .getElementsByTagName("MEDIA_DESCRIPTOR")[0]
                    .getAttribute("RELATIVE_MEDIA_URL").split("./")[1];

                resolve(wavUrl);
            };
            reader.onerror = () => {
                reject(reader.error);
            };
        });
    }

    onDrop = async (acceptedFiles) => {
        // TODO: Behaviour when dropping multiple times is still undefined
        // (do we empty the dataset?)
        this.setState({missingFiles: []});
        console.log("files dropped:", acceptedFiles);

        const eafFiles = acceptedFiles
            .filter(file => file.name.split(".").pop() === "eaf");
        const wavFileNames = acceptedFiles
            .filter(file => file.name.split(".").pop() === "wav")
            .map(file => file.name);

        // for each is not supported with await for some reason...
        for (let i = 0; i < eafFiles.length; i++) {
            const parsedWavFile = await this.parseElan(eafFiles[i]);
            const identicalWavFile = eafFiles[i].name.split(".")[0].concat(".wav");

            if (!wavFileNames.includes(parsedWavFile) && !wavFileNames.includes(identicalWavFile)) {
                this.setState(prevState => ({
                    missingFiles: [...prevState.missingFiles, [identicalWavFile, parsedWavFile]],
                }));
            }
        }

        var formData = new FormData();

        acceptedFiles.forEach(file => {
            formData.append("file", file);
        });
        this.props.datasetFiles(formData);
    }

    render() {
        const {t, name} = this.props;
        const interactionDisabled = name ? false : true;

        return (
            <div className="FileUpload">
                {this.state.missingFiles.length > 0 && 
                    <Message negative>
                        <MessageHeader>
                            {t("dataset.files.missingAudioFiles")}
                        </MessageHeader>
                        <p>
                            {t("dataset.files.missingAudioFilesDescription")}
                        </p>
                        <ul>
                            {this.state.missingFiles.map(wavFile => {
                        return (
                            <li key={wavFile[0]}>
                                {wavFile[0]} / {wavFile[1]}
                            </li>
                        );
                    })}
                        </ul>
                    </Message>}
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
                                    <p>{t("dataset.fileUpload.dropFilesHintDragActive")}</p> :
                                    <p>{t("dataset.fileUpload.dropFilesHint")}</p>
                                }
                                <Button>{t("dataset.files.uploadButton")}</Button>
                            </div>
                        );
                    }}
                </Dropzone>
            </div>
        );
    }
}


const mapDispatchToProps = dispatch => ({
    datasetFiles: postData => {
        dispatch(datasetFiles(postData));
    },
});

export default connect(null, mapDispatchToProps)(
    withTranslation("common")(FileUpload)
);
