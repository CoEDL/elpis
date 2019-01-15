import React, { Component } from 'react';
import { Link } from "react-router-dom";
import AccordionFluid from '../SemanticsComponents/AccordionFluid'
import { Grid, Header, Segment, Icon, Form, Button } from 'semantic-ui-react';

export default class StepNaming extends Component {
    render() {
        return(
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                <Segment>
                    <Grid centered>
                        <Grid.Column width={6}>
                            <AccordionFluid title={'Step 1'} active/>
                            <AccordionFluid title={'Step 2'}/>
                            <AccordionFluid title={'Step 3'}/>
                        </Grid.Column>
                        <Grid.Column width={10}>
                            <Header as='h1' text="true"> <Icon name='setting' /> Build a new model </Header>
                            <Form>
                                <Form.Field>
                                    <input type='text' placeholder='Project Name'/>
                                </Form.Field>
                                <Button type='submit' as={Link} to="/add-data">GO</Button>
                            </Form>
                        </Grid.Column>
                    </Grid>  
                </Segment>
            </div>
        )
    }
}