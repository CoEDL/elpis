import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Divider, Grid, Header, Segment, List, Button} from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class DataBundlePreparation extends Component {
    render() {
        const { t } = this.props;
        return (
                <div>
                    <Branding />
                    <Segment>
                        <Grid centered>
                                <Grid.Column width={4}>
                                    <Informer />
                                </Grid.Column>
                                <Grid.Column width={12}>
                                    <Header as='h1'>{t('dataBundle.preparation.title')}</Header>
                                    <h2>{t('dataBundle.preparation.header')}</h2>
                                    <p>{t('dataBundle.preparation.bannerMessage')}</p>
                                    <p>{t('dataBundle.preparation.bannerMessageDetailed')}</p>
                                   <Grid columns={2}>
                                        <Grid.Column>
                                        <Header as='h1'>{t('dataBundle.preparation.wordlistHeader')}</Header>
                                            <List>
                                                <List.Item>
                                                    <List.Content>amakaang</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>kaai</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>muila</List.Content>
                                                </List.Item>
                                            </List>
                                        </Grid.Column>
                                        <Grid.Column>
                                            <Header as='h1'>{t('dataBundle.preparation.frequencyHeader')}</Header>
                                            <List>
                                                <List.Item>
                                                    <List.Content>21</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>77</List.Content>
                                                </List.Item>
                                                <List.Item>
                                                    <List.Content>84</List.Content>
                                                </List.Item>
                                            </List>
                                        </Grid.Column>
                                    </Grid>
                                    <Divider />
                                    <Button type='submit' as={Link} to="/model/pronunciation-dictionary">{t('dataBundle.preparation.nextButton')}</Button>
                                </Grid.Column>
                        </Grid>
                    </Segment>
                </div>
        );
    }
}
export default translate('common')(DataBundlePreparation)
