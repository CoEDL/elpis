import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Divider, Button } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import Dropzone from "react-dropzone";
import {fromEvent} from "file-selector";

export default class StepBuildPronunciationDictionary extends Component {
    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("acceptedFiles:", acceptedFiles);
    }
    render() {
        return (
            <div>
                    <StepBranding />
                    <Segment>
                        <Grid centered>
                                <Grid.Column width={6}>
                                    <StepInformer instructions={NewModelInstructions} />
                                </Grid.Column>
                                <Grid.Column width={10}>
                                    <Header as='h1'>  <Icon name='train' />Build the pronunciation dictionary</Header>
                                    <Header as="h3">Pronunciation file:</Header>
                                    <Divider />

                                    <Dropzone onDrop={this.onDrop} getDataTransferItems={evt => fromEvent(evt)}>
                                        {/* <Segment raised style={{fontFamily: '"Lucida Console", Monaco, monospace'}}>
                                        here is some font
                                        </Segment> */}
                                        {({ getRootProps, getInputProps, isDragActive }) => {
                                            if (isDragActive) {
                                                return (<Segment {...getRootProps()} placeholder>
                                                    <input {...getInputProps()} />
                                                    <Header icon>
                                                        <Icon name='file outline' />
                                                        Drop new pronunciation file here
                                                    </Header>
                                                </Segment>);
                                            } else {
                                                return (<Segment {...getRootProps()} raised style={{fontFamily: '"Lucida Console", Monaco, monospace'}}>
                                                    here here
                                                </Segment>);
                                            }
                                        }}
                                    </Dropzone>
                                    <Button onClick={()=>{}}>Upload dictionary</Button>
                                    <Button type='submit' as={Link} to="/model-settings">Next: model settings</Button>
                                </Grid.Column>
                        </Grid>
                    </Segment>
                </div>
        );
    }
}