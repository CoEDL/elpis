import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, List, Button} from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';

class StepDataPreparation extends Component {
    render() {
        const { t } = this.props;
        return (
                <div>
                    <StepBranding />
                    <Segment>
                        <Grid centered>
                                <Grid.Column width={6}>
                                    <StepInformer instructions={NewModelInstructions} />
                                </Grid.Column>
                                <Grid.Column width={10}>
                                    <Header as='h1'>{t('dataPreparation.title')}</Header>
                                    <h2>{t('dataPreparation.header')}</h2>
                                    <p>{t('dataPreparation.bannerMessage')}</p>
                                    <p>{t('dataPreparation.bannerMessageDetailed')}</p>
                                   <Grid columns={2}>
                                        <Grid.Column>
                                        <Header as='h1'>{t('dataPreparation.wordlistHeader')}</Header>
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
                                            <Header as='h1'>{t('dataPreparation.frequencyHeader')}</Header>
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
                                    <Button type='submit' as={Link} to="/build-pronunciation-dictionary">{t('dataPreparation.nextButton')}</Button>
                                </Grid.Column>
                        </Grid>
                    </Segment>
                </div>
        );
    }
}
export default translate('common')(StepDataPreparation)
