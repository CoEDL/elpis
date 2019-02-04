import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import {fromEvent} from "file-selector";
import { translate } from 'react-i18next';
// import request from "superagent";
import axios from 'axios'

import { updateModelTranscriptionFiles } from '../../redux/actions';
import { connect } from 'react-redux';

class FileUpload extends Component {
    state={
        files:[],
        fileNames:[],
        file:null
      }

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("files dropped:", acceptedFiles);
        var formData = new FormData();
        acceptedFiles.forEach(file => {
            console.log(file)
            formData.append('file', file);
        })
        this.props.updateModelTranscriptionFiles(formData);

    };



    render(){
        const fileNameList = (this.state.fileNames) ? (this.state.fileNames.map((f) => <li key={f}>{f}</li>)) : ''
        const { t } = this.props;

        return(
            <div className="App">
            {this.props.myName}
                    <p>{t('fileUpload.audioLabel')} {this.props.audioFiles}</p>
                    <p>{t('fileUpload.transcriptionLabel')} {this.props.transcriptionFiles}</p>
                    <p>{t('fileUpload.additionalLabel')} {this.props.additionalTextFiles}</p>

                    <Dropzone className="dropzone" onDrop={this.onDrop} getDataTransferItems={evt => fromEvent(evt)}>
                        {({ getRootProps, getInputProps, isDragActive }) => {
                            return (
                                <div
                                    {...getRootProps()}
                                    className={classNames("dropzone", {
                                        "dropzone_active": isDragActive
                                    })}
                                >

                                    <input {...getInputProps()} />

                                        {isDragActive ? (
                                            <p>{t('fileUpload.dropFilesHeader')} </p>
                                        ) : (
                                            <p>
                                                {t('fileUpload.dropFilesHint')}
                                            </p>
                                        )}

                            </div>
                        );
                    }}
                    </Dropzone>

                    <ul>{fileNameList}</ul>
            </div>

        );
    }
}

const mapStateToProps = state => {
    return {
        // myName: state.myName,
        // audioFiles: state.model.audioFiles,
        // transcriptionFiles: state.model.transcriptionFiles,
        // additionalTextFiles: state.model.additionalTextFiles,
    }
}

const mapDispatchToProps = dispatch => ({
    updateModelTranscriptionFiles: data => {
        dispatch(updateModelTranscriptionFiles(data));
    }
    // addTranscriptionFile: filename => {
    //     dispatch(addTranscriptionFile(filename));
    // },
    // addAdditionalTextFile: filename => {
    //     dispatch(addAdditionalTextFile(filename));
    // },
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(FileUpload));
