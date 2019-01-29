import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import {fromEvent} from "file-selector";
import request from "superagent";

export default class FileUpload extends Component {
    state={
        files:[],
        fileNames:[]
    }

    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log(acceptedFiles);
        
        
        acceptedFiles.forEach(file => {
            //console.log(file)
            request
            .post('http://127.0.0.1:5000/corpus/wav')
            .attach(file.name, file.path);
        });

        const fileNames = acceptedFiles.map(f => f.name);
        //console.log(fileNames);
        this.setState({ ...this.state, files: acceptedFiles, fileNames: fileNames  });
    };

    render(){
        const fileNameList = (this.state.fileNames) ? (this.state.fileNames.map((f) => <li key={f}>{f}</li>)) : ''

        return(
            <div className="App">
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