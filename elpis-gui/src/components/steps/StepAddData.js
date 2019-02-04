import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, List, Button, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import FileUpload from '../FileuploadComponents/FileUpload';
import { translate } from 'react-i18next';

class StepAddData extends Component {
    // constructor(props) {
    //     super(props);
    // }
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
                                { t('addData.title') }
                            </Header>
                            <p>
                                { t('addData.description') }
                            </p>

                            <Segment>
                                <FileUpload />
                            </Segment>

                            <Header as='h1'>
                                { t('addData.dragHeader') }
                            </Header>
                            <Grid>
                                <Grid.Column width={ 5 }>
                                    <List>
                                        <List.Item>
                                            <List.Icon name='check square' />
                                            <List.Content>File1.eaf</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='check square' />
                                            <List.Content>File2.eaf</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='check square' />
                                            <List.Content>File3.eaf</List.Content>
                                        </List.Item>
                                    </List>
                                </Grid.Column>

                                <Grid.Column width={ 5 }>
                                    <List>
                                        <List.Item>
                                            <List.Icon name='check square' />
                                            <List.Content>File1.wav</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='check square' />
                                            <List.Content>File2.wav</List.Content>
                                        </List.Item>
                                        <List.Item>
                                            <List.Icon name='check square' />
                                            <List.Content>File3.wav</List.Content>
                                        </List.Item>
                                    </List>
                                </Grid.Column>
                            </Grid>
                            <Button type='submit' as={ Link } to="/data-preparation">
                                { t('addData.nextButton') }
                            </Button>
                            <Button type='submit' as={ Link } to="/data-preparation-error" icon>
                                <Icon name='warning sign' />
                                { t('addData.nextButtonError') }
                            </Button>
                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(StepAddData)
