import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { translate } from 'react-i18next';
import { updateModelTranscriptionFiles } from '../../redux/actions';
import { connect } from 'react-redux';

class FileUpload extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        var formData = new FormData();
        acceptedFiles.forEach(file => {
            console.log(file)
            formData.append('file', file);
        })
        this.props.updateModelTranscriptionFiles(formData);
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
                                        <p>{ t('fileUpload.dropFilesHintDragActive') } </p>
                                    ) : (<p>{ t('fileUpload.dropFilesHint') }</p>)
                                }
                            </div>
                        );
                    } }
                </Dropzone>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        // myName: state.model.myName,
    }
}

const mapDispatchToProps = dispatch => ({
    updateModelTranscriptionFiles: postData => {
        dispatch(updateModelTranscriptionFiles(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(FileUpload));
