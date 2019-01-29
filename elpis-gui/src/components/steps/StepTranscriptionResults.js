import React, { Component } from 'react';
import { Link } from "react-router-dom";
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { Grid, Header, Segment, Icon, Card, Button } from 'semantic-ui-react';

export default class StepTranscriptionResults extends Component {
    render() {
        return (
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                <Segment>
                    <Grid centered>
                        <Grid.Column width={5}>
                            <StepInformer instructions={NewModelInstructions} />
                        </Grid.Column>
                        <Grid.Column width={11}>
                            <Header as='h1' text='true'> <Icon name='schlix' /> Transcribed new audio - Results </Header>
                            <p>Used English-Indonesian 5-gram with Indonesian 12s</p>
                            <p>for audio filename</p>
            
                        <Card>
                            <Card.Content header='Error Log' />
                            <Card.Content description='Were there any errors? Just output the log, nothing fancy' />
                        </Card>
                    
                        <Card>
                            <Card.Content header='Transcription as text' />
                            <Card.Content description= 'Blah Blah Blah Blah Blah' />
                        </Card>
                        <Button as={Link} to="/">Download ELAN file here</Button>
                        <Button as={Link} to="/">Download TextGrid PRAAT file here</Button>

                        </Grid.Column>
                    </Grid>  
                </Segment>
            </div>
        );
    }
}