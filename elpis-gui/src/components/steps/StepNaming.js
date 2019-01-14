import React, { Component } from 'react';
import AccordionFluid from '../SemanticsComponents/AccordionFluid'
import { Grid, GridColumn, Placeholder } from 'semantic-ui-react';

export default class StepNaming extends Component {
    // constructor(props) {
    //     super(props);
    // }
    render() {
        return(
            <Grid>
                <Grid.Column width={4}>
                    <AccordionFluid title={'Step 1'}/>
                    <AccordionFluid title={'Step 2'}/>
                    <AccordionFluid title={'Step 3'}/>
                </Grid.Column>

                <Grid.Column width={12}>
                    <Placeholder>
                        <Placeholder.Header image>
                            <Placeholder.Line />
                        </Placeholder.Header>
                    </Placeholder>
                </Grid.Column>
            </Grid>
        )
    }
}