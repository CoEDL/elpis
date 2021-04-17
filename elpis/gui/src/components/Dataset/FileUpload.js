import React, {Component} from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import {Button} from "semantic-ui-react";
import {fromEvent} from "file-selector";
import {withTranslation} from "react-i18next";
import {datasetFiles} from "redux/actions/datasetActions";
import {connect} from "react-redux";

class FileUpload extends Component {
    parseElan = (files) => {
        const wavFileNames = [];

        files.forEach(file => {
            const reader = new FileReader();
            reader.readAsText(file);
            reader.onload = () => {
                const parser = new DOMParser();
                const eafDoc = parser.parseFromString(reader.result, "application/xml")
                const wavUrl = eafDoc
                    .getElementsByTagName("ANNOTATION_DOCUMENT")[0]
                    .getElementsByTagName("HEADER")[0]
                    .getElementsByTagName("MEDIA_DESCRIPTOR")[0]
                    .getAttribute("RELATIVE_MEDIA_URL").split("./")[1];
                wavFileNames.push(wavUrl);
            }
            reader.onerror = () => {
                console.log(reader.error);
            }
        });

        return wavFileNames;
    }

    onDrop = (acceptedFiles) => {
        console.log("files dropped:", acceptedFiles);
        const eafFiles = acceptedFiles.filter(file => file.name.split('.').pop() === "eaf");
        const wavFiles = acceptedFiles.filter(file => file.name.split('.').pop() === "wav");

        // Add wav file names from eaf file contents
        const wavFileNames = this.parseElan(eafFiles);
        // Add media file names from eaf file names
        eafFiles.forEach(file => {
            wavFileNames.push(file.name.split('.')[0].concat(".wav"));
        })

        console.log(wavFileNames);

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
