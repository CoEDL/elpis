import React, { Component } from 'react';
import { Link } from "react-router-dom";
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { Grid, Header, Segment, Icon, Form, Button } from 'semantic-ui-react';

export default class StepModelSettings extends Component {
    
    render() {
        return (
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                <Segment>
                    <Grid centered>
                        <Grid.Column width={6}>
                            <StepInformer instructions={NewModelInstructions} />
                        </Grid.Column>
                        <Grid.Column width={10}>
                            <Header as='h1' text='true'> <Icon name='server' /> Model Settings </Header>
                            <Form>
                                <Form.Field>
                                    <label>Audio Frequency</label>
                                    <input type= 'text' placeholder='44100'/>
                                </Form.Field>
                                <Form.Field>
                                    <label>MFCC stuff</label>
                                    <input type= 'text' placeholder='22050'/>
                                </Form.Field>
                                <Form.Field>
                                    <label>n-gram</label>
                                    <input type= 'text' placeholder='3'/>
                                </Form.Field>
                                <Form.Field>
                                    <label>Beam</label>
                                    <input type= 'text' placeholder='10'/>
                                </Form.Field>
                                <Button type='submit' as={Link} to="/training-model">Next: train model</Button>
                            </Form>
                        </Grid.Column>
                    </Grid>  
                </Segment>
            </div>
        );
    }
}