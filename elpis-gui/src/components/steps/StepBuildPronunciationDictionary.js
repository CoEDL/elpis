import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Divider, Button } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import Dropzone from "react-dropzone";
import { fromEvent } from "file-selector";
import { translate } from 'react-i18next';

class StepBuildPronunciationDictionary extends Component {
    onDrop = (acceptedFiles, rejectedFiles) => {
        console.log("acceptedFiles:", acceptedFiles);
    }
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
                                { t('buildPron.title') }
                            </Header>

                            <Header as="h3">
                                { t('buildPron.header') }
                            </Header>

                            <Divider />

                            <Dropzone onDrop={ this.onDrop } getDataTransferItems={ evt => fromEvent(evt) }>
                                { ({ getRootProps, getInputProps, isDragActive }) => {
                                    if (isDragActive) {
                                        return (
                                            <Segment { ...getRootProps() } placeholder>
                                                <input { ...getInputProps() } />
                                                <Header icon>
                                                    <Icon name='file outline' />
                                                    { t('buildPron.dropHereHeader') }
                                                </Header>
                                            </Segment>
                                        );
                                    } else {
                                        return (
                                            <Segment { ...getRootProps() } raised style={ { fontFamily: '"Lucida Console", Monaco, monospace' } }>
                                                { t('buildPron.dropHereHint') }
                                            </Segment>
                                        );
                                    }
                                } }
                            </Dropzone>

                            <Button onClick={ () => { } }>
                                { t('buildPron.uploadButton') }
                            </Button>

                            <Divider />

                            <Button type='submit' as={ Link } to="/model-settings">
                                { t('buildPron.nextButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(StepBuildPronunciationDictionary)
