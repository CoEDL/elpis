import React, { Component } from 'react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'
import { Grid, Header, Segment, Icon, Form, Button, label } from 'semantic-ui-react';

export default class StepModelSettings extends Component {
    
    render() {
        return (
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>

                <Segment>
                    <Grid centered>
                            <Grid.Column width={6}>
                                <AccordionFluid title={'Step 1'}/>
                                <AccordionFluid title={'Step 2'}/>
                                <AccordionFluid title={'Step 3'}/>
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
                                    <Button type='submit' onClick={()=> {this.props.toStepTrainingModel()}}>Next:train model</Button>
                                </Form>
                            </Grid.Column>
                       
                    </Grid>  
                </Segment>
                <Button onClick={()=>{this.props.goBack()}}>Back</Button>
            </div>
        );
    }
}