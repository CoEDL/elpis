import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, Form, Button } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { modelSettings } from 'redux/actions';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelSettings extends Component {
    handleAudioSetting = (e) => {
        const { settings, modelSettings } = this.props;
        const newSettings = {...settings, frequency:e.target.value}
        console.log(newSettings)
        modelSettings({settings:newSettings})
    }
    handleMfccSetting = (e) => {
        const { settings, modelSettings } = this.props;
        const newSettings = {...settings, mfcc:e.target.value}
        modelSettings({settings:newSettings})
    }
    handleNgramSetting = (e) => {
        const { settings, modelSettings } = this.props;
        const newSettings = {...settings, ngram:e.target.value}
        modelSettings({settings:newSettings})
    }
    handleBeamSetting = (e) => {
        const { settings, modelSettings } = this.props;
        const newSettings = {...settings, beam:e.target.value}
        modelSettings({settings:newSettings})
    }
    render() {
        const { t, settings } = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <Informer />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>

                            <Header as='h1' text='true'>
                                { t('model.settings.title') }
                            </Header>

                            <Form>
                                <Form.Field>
                                    <label>{ t('model.settings.nGramLabel') }</label>
                                    <input type='text' placeholder={ settings.ngram } onChange={ this.handleNgramSetting } />
                                </Form.Field>

                                <Header as='h2' text='true'>
                                    { t('model.settings.advancedHeader') }
                                </Header>

                                <Form.Field>
                                    <label>{ t('model.settings.audioLabel') }</label>
                                    <input type='text' placeholder={ settings.frequency } onChange={ this.handleAudioSetting } />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('model.settings.mfccLabel') }</label>
                                    <input type='text' placeholder={ settings.mfcc } onChange={ this.handleMfccSetting } />
                                </Form.Field>

                                <Form.Field>
                                    <label>{ t('model.settings.beamLabel') }</label>
                                    <input type='text' placeholder={ settings.beam } onChange={ this.handleBeamSetting } />
                                </Form.Field>

                            </Form>

                            <Divider />

                            <Button as={ Link } to="/model/training">
                                { t('model.settings.nextButton') }
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
    modelSettings: postData => {
        dispatch(modelSettings(postData));
    }
})

export default connect(mapStateToProps, mapDispatchToProps)(translate('common')(ModelSettings));
