import React, { Component } from 'react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'
import { Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';

export default class StepTrainingModel extends Component {
    // constructor(props) {
    //     super(props);
    // }
    
    render() {
        const settingDescription = [
            'audio XXX',
            'mfcc XXX',
            'n-gram XXX',
            'beam XXX'
        ].join(' ');

        return (
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>

                <Segment>
                    <Grid centered>
                            <Grid.Column width={5}>
                                <AccordionFluid title={'Step 1'}/>
                                <AccordionFluid title={'Step 2'}/>
                                <AccordionFluid title={'Step 3'}/>
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

                            <Button onClick={()=>{this.props.toStepTrainingSuccess()}}>Next:model trained OK</Button>
                            </Grid.Column>
                       
                    </Grid>  
                </Segment>
                <Button onClick={()=>{this.props.goBack()}}>Back</Button>
            </div>
        );
    }
}