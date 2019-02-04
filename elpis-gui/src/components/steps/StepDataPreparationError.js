import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Button } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';

class StepDataPreparationError extends Component {
    render() {
        const { t } = this.props;
        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 6 }>
                            <StepInformer instructions={ NewModelInstructions } />
                        </Grid.Column>

                        <Grid.Column width={ 10 }>
                            <Header as='h1'>
                                <Icon name='warning' />
                                { t('dataPreparationError.title') }
                            </Header>

                            <p>Banner Message: errors were found when cleaning(processing) your data</p>
                            <p>Novice readable description of what just happened</p>
                            <p>Show the errors and information about how to fix the error</p>

                            <Button type='submit' as={ Link } to="/add-data">
                                { t('dataPreparationError.backButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(StepDataPreparationError)
