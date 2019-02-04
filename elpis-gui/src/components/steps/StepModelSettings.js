import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Form, Button } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';

class StepModelSettings extends Component {

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
                            <Header as='h1' text='true'>
                                { t('modelSettings.title') }
                            </Header>

                            <Form>
                                <Form.Field>
                                    <label>{ t('modelSettings.audioLabel') }</label>
                                    <input type='text' placeholder='44100' />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('modelSettings.mfccLabel') }</label>
                                    <input type='text' placeholder='22050' />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('modelSettings.nGramLabel') }</label>
                                    <input type='text' placeholder='3' />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('modelSettings.beamLabel') }</label>
                                    <input type='text' placeholder='10' />
                                </Form.Field>

                                <Button type='submit' as={ Link } to="/training-model">
                                    { t('modelSettings.nextButton') }
                                </Button>
                            </Form>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(StepModelSettings)
