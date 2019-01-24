import React, { Component } from "react";
import classNames from "classnames";
import Dropzone from "react-dropzone";
import {fromEvent} from "file-selector";

export default class FileUpload extends Component {
    state={
        files:[],
        fileNames:[]
    }

    render(){
        return(
            <div>
                <h1>Hello FIle Upload</h1>
            </div>
        )
    }
}