import React, { Component } from 'react';
import { Grid, Header, List, Segment, Icon, Button } from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelList extends Component {
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
                            <Header as='h1'>Previously trained models</Header>
                            <List>
                                <List.Item>
                                    <List.Icon name='square outline' />
                                    <List.Content>English-Indonesian 1-gram</List.Content>
                                </List.Item>
                                <List.Item>
                                    <List.Icon name='square outline' />
                                    <List.Content>English-Indonesian 3-gram</List.Content>
                                </List.Item>
                                <List.Item>
                                    <List.Icon name='square outline' />
                                    <List.Content>English-Indonesian 5-gram with Indonesian 12s</List.Content>
                                </List.Item>
                                <List.Item>
                                    <List.Icon name='square outline' />
                                    <List.Content>Indonesian 1-gram</List.Content>
                                </List.Item>
                                <List.Item>
                                    <List.Icon name='square outline' />
                                    <List.Content>Everything 3-gram with Indonesian 12s</List.Content>
                                </List.Item>
                            </List>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(ModelList)
