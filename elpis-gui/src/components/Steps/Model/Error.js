import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Card, Button } from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelError extends Component {
    render() {
        const { t } = this.props;
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
                                <Icon name='warning' />
                                { t('model.error.title') }
                            </Header>
                            <p>We ran into a problem when training the model</p>
                            <p>Please click the button below to connect you to a tech person on slack</p>
                            <p>An error file detailing the log showing below will be sent as an attachment to the technical team on slack</p>

                            <Card>
                                <Card.Content header={ t('model.error.errorLogHeader') } />
                                <Card.Content description='Error logs from training model' />
                            </Card>

                            <Button href="https:slack.com/" target="_blank">
                                { t('model.error.contactButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(ModelError)
