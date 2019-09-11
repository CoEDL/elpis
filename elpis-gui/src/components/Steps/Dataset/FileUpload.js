import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { translate } from 'react-i18next';
import { datasetFiles, datasetStatus } from 'redux/actions';
import { connect } from 'react-redux';

class FileUpload extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);

        var formData = new FormData();
        acceptedFiles.forEach(file => {
            console.log(file)
            formData.append('file', file);
        })
        this.props.datasetStatus("loading");
        this.props.datasetFiles(formData);
    };

    render() {
        const { t } = this.props;

        return (
            <div className="FileUpload">

                <Dropzone className="dropzone" onDrop={ this.onDrop } getDataTransferItems={ evt => fromEvent(evt) }>
                    { ({ getRootProps, getInputProps, isDragActive }) => {
                        return (
                            <div
                                { ...getRootProps() }
                                className={ classNames("dropzone", {
                                    "dropzone_active": isDragActive
                                }) }
                            >
                                <input { ...getInputProps() } />
                                {
                                    isDragActive ? (
                                        <p>{ t('dataset.fileUpload.dropFilesHintDragActive') } </p>
                                    ) : (<p>{ t('dataset.fileUpload.dropFilesHint') }</p>)
                                }
                            </div>
                        );
                    } }
                </Dropzone>
            </div>
        );
    }
}


const mapDispatchToProps = dispatch => ({
    datasetFiles: postData => {
        dispatch(datasetFiles(postData));
    },
    datasetStatus: status => {
        dispatch(datasetStatus(status));
    }
})

export default connect(null, mapDispatchToProps)(translate('common')(FileUpload));
