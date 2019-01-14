import React, { Component } from 'react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'
import { Grid, Header, Segment, Icon, Form, Button } from 'semantic-ui-react';

export default class StepNaming extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return(
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
                                <Header as='h1' text> <Icon name='setting' /> Build a new model </Header>
                            
                                <Form>
                                    <Form.Field>
                                        <input placeholder='Project Name'/>
                                    </Form.Field>
                                    <Button type='submit' onClick={()=> {this.props.toStepAddData()}}>GO</Button>
                                </Form>
                            </Grid.Column>
                       
                    </Grid>  
                </Segment>
                <Button onClick={()=>{this.props.goBack()}}>Back</Button>
            </div>
        )
    }
}