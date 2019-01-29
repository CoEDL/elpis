import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Grid, Header, Segment, Icon, Form, Button } from 'semantic-ui-react';
import StepInformer, { NewModelInstructions } from '../StepInformer';

export default class StepNaming extends Component {
    render() {
        return(
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                <Segment>
                    <Grid centered>
                        <Grid.Column width={6}>
                            <StepInformer instructions={NewModelInstructions} />
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