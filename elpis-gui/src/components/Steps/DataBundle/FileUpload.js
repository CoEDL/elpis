import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { translate } from 'react-i18next';
import { dataBundleFiles } from 'redux/actions';
import { connect } from 'react-redux';

class FileUpload extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);

        var formData = new FormData();
        // backend will need to know whether to add to existing files
        // or wipe existing and use only these
        // we'll also need to update redux state on this basis

        // formData.append('replaceFiles', this.props.replaceFiles);

        acceptedFiles.forEach(file => {
            console.log(file)
            formData.append('file', file);
        })
        this.props.dataBundleFiles(formData);
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
                                        <p>{ t('dataBundle.fileUpload.dropFilesHintDragActive') } </p>
                                    ) : (<p>{ t('dataBundle.fileUpload.dropFilesHint') }</p>)
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
        replaceFiles: state.model.replaceFiles
    }
}

const mapDispatchToProps = dispatch => ({
    dataBundleFiles: postData => {
        dispatch(dataBundleFiles(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(FileUpload));
