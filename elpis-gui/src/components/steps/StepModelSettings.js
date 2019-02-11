import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Form, Button } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer from '../StepInformer';
import { translate } from 'react-i18next';
import { connect } from 'react-redux';
import { updateModelSettings } from '../../redux/actions';

class StepModelSettings extends Component {
    handleAudioSetting = (e) => {
        const { settings, updateModelSettings } = this.props;
        const newSettings = {...settings, frequency:e.target.value}
        console.log(newSettings)
        updateModelSettings({settings:newSettings})
    }
    handleMfccSetting = (e) => {
        const { settings, updateModelSettings } = this.props;
        const newSettings = {...settings, mfcc:e.target.value}
        updateModelSettings({settings:newSettings})
    }
    handleNgramSetting = (e) => {
        const { settings, updateModelSettings } = this.props;
        const newSettings = {...settings, ngram:e.target.value}
        updateModelSettings({settings:newSettings})
    }
    handleBeamSetting = (e) => {
        const { settings, updateModelSettings } = this.props;
        const newSettings = {...settings, beam:e.target.value}
        updateModelSettings({settings:newSettings})
    }
    render() {
        const { t, settings } = this.props;
        return (
            <div>
                <StepBranding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 6 }>
                            <StepInformer />
                        </Grid.Column>

                        <Grid.Column width={ 10 }>

                            <Header as='h1' text='true'>
                                { t('modelSettings.title') }
                            </Header>

                            <Form>
                                <Form.Field>
                                    <label>{ t('modelSettings.audioLabel') }</label>
                                    <input type='text' placeholder={ settings.frequency } onChange={ this.handleAudioSetting } />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('modelSettings.mfccLabel') }</label>
                                    <input type='text' placeholder={ settings.mfcc } onChange={ this.handleMfccSetting } />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('modelSettings.nGramLabel') }</label>
                                    <input type='text' placeholder={ settings.ngram } onChange={ this.handleNgramSetting } />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('modelSettings.beamLabel') }</label>
                                    <input type='text' placeholder={ settings.beam } onChange={ this.handleBeamSetting } />
                                </Form.Field>

                            </Form>

                            <Divider />

                            <Button as={ Link } to="/model-training">
                                { t('modelSettings.nextButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        settings: state.model.settings
    }
}

const mapDispatchToProps = dispatch => ({
    updateModelSettings: postData => {
        dispatch(updateModelSettings(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(StepModelSettings));
