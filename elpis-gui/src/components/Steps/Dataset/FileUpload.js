import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import { Button } from 'semantic-ui-react';
import { fromEvent } from "file-selector";
import { translate } from 'react-i18next';
import { datasetFiles } from 'redux/actions/datasetActions';
import { connect } from 'react-redux';

class FileUpload extends Component {

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles)
        var formData = new FormData()
        acceptedFiles.forEach(file => {
            formData.append('file', file)
        })
        this.props.datasetFiles(formData)
    }

    render() {
        const { t } = this.props
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
                                <Button>{t('dataset.files.uploadButton')}</Button>
                            </div>
                        )
                    } }
                </Dropzone>
            </div>
        )
    }
}


const mapDispatchToProps = dispatch => ({
    datasetFiles: postData => {
        dispatch(datasetFiles(postData))
    }
})

export default connect(null, mapDispatchToProps)(translate('common')(FileUpload))
