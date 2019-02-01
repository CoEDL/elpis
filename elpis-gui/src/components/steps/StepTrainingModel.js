import React, { Component } from 'react';
import { Link } from "react-router-dom";
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';

export default class StepTrainingModel extends Component {
    render() {
        const settingDescription = [
            'audio XXX',
            'mfcc XXX',
            'n-gram XXX',
            'beam XXX'
        ].join(' ');

        return (
            <div>
                <Header as='h1'><img src="https://github.com/CoEDL/elpis/raw/master/docs/img/elpis.png" className="logo" alt="logo" /></Header>
                <Segment>
                    <Grid centered>
                        <Grid.Column width={5}>
                            <StepInformer instructions={NewModelInstructions} />
                        </Grid.Column>
                        <Grid.Column width={11}>
                            <Header as='h1' text='true'> <Icon name='schlix' /> Training the Model </Header>
                            <Message icon>
                                <Icon name='circle notched' loading />
                                <Message.Content>
                                <Message.Header>The model is being trained</Message.Header>
                                </Message.Content>
                            </Message>
                        <Card>
                            <Card.Content header='Settings' />
                            <Card.Content description={settingDescription} />
                        </Card>
                        <Step.Group size='mini'>
                            <Step>
                            <Icon name='info' size='tiny'/>
                            <Step.Content>
                                <Step.Title>PREPARING ACOUSTIC DATA</Step.Title>
                            </Step.Content>
                            </Step>
                            <Step active>
                            <Icon name='info' size='tiny'/>
                            <Step.Content>
                                <Step.Title>FEATURES EXTRACTION</Step.Title>
                            </Step.Content>
                            </Step>
                            <Step disabled>
                            <Icon name='info' size='tiny'/>
                            <Step.Content>
                                <Step.Title>PREPARING LANGUAGE DATA</Step.Title>
                            </Step.Content>
                            </Step>
                        </Step.Group>
                        <Card>
                            <Card.Content header='Logs' />
                            <Card.Content description= 'gory output from Kaldi - but not interactive' />
                        </Card>
                        <Button as={Link} to="/training-success">Next: model trained OK</Button>
                        <Button as={Link} to="/training-error" icon> <Icon name='warning sign'/> Next: model trained Error</Button>
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}