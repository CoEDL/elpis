import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import {fromEvent} from "file-selector";
import request from "superagent";

import { addAudioFile, addTranscriptionFile, addAdditionalTextFile } from '../../redux/actions';
import { connect } from 'react-redux';

class FileUpload extends Component {
    state={
        files:[],
        fileNames:[]
    }

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("file dropped:", acceptedFiles);
        
        
        // acceptedFiles.forEach(file => {
        //     //console.log(file)
        //     request
        //     .post('http://127.0.0.1:5000/corpus/wav')
        //     .attach(file.name, file.path);
        // });

        const fileNames = acceptedFiles.map(f => f.name);
        //console.log(fileNames);
        // this.setState({ ...this.state, files: acceptedFiles, fileNames: fileNames  });
    };

    render(){
        const fileNameList = (this.state.fileNames) ? (this.state.fileNames.map((f) => <li key={f}>{f}</li>)) : ''

        return(
            <div className="App">
                    <p>Audio files: {this.props.audioFiles}</p>
                    <p>Transcription files: {this.props.transcriptionFiles}</p>
                    <p>Audio files: {this.props.audioFiles}</p>
                    <Dropzone className="dropzone"  onDrop={this.onDrop} getDataTransferItems={evt => fromEvent(evt)}>
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
                                            <p>Drop files here...</p>
                                        ) : (
                                            <p>
                                                Drop individual files or a folder containing your file here
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
        audioFiles: state.model.audioFiles,
        transcriptionFiles: state.model.transcriptionFiles,
        additionalTextFiles: state.model.additionalTextFiles,
    }
}

const mapDispatchToProps = dispatch => ({
    addTranscriptionFile: filename => {
        dispatch(addTranscriptionFile(filename));
    },
    addAudioFile: filename => {
        dispatch(addAudioFile(filename));
    },
    addAdditionalTextFile: filename => {
        dispatch(addAdditionalTextFile(filename));
    },
})

export default connect(mapStateToProps, mapDispatchToProps)(FileUpload);