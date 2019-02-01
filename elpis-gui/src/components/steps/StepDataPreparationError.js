import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Button} from 'semantic-ui-react';
import StepBranding from './StepBranding';
import AccordionFluid from '../Semantics Components/AccordionFluid'

export default class StepDataPreparationError extends Component{
    render(){
        return (
            <div>
                    <StepBranding />
                    <Segment>
                        <Grid centered>
                                <Grid.Column width={6}>
                                    <AccordionFluid title={'Step 1'} active/>
                                    <AccordionFluid title={'Step 2'}/>
                                    <AccordionFluid title={'Step 3'}/>
                                </Grid.Column>
                                <Grid.Column width={10}>
                                    <Header as='h1' text textAlign='center'>  <Icon name='warning' />Data preparation error</Header>
                                    <p>Banner Message: errors were found when cleaning(processing) your data</p>
                                    <p>Novice readable description of what just happened</p>
                                    <p>Show the errors and information about how to fix the error</p>

                                    <Button type='submit' as={Link} to="/add-data">Back to add data</Button>
                                </Grid.Column>
                        </Grid>
                    </Segment>
                </div>
        );
    }
}