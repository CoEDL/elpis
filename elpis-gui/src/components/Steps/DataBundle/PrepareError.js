import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Header, Segment, Icon, Button } from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';
import urls from 'urls'

class DataBundlePrepareError extends Component {
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
                            <Header as='h1'>
                                <Icon name='warning' />
                                { t('dataBundle.prepareError.title') }
                            </Header>

                            <p>Banner Message: errors were found when cleaning(processing) your data</p>
                            <p>Novice readable description of what just happened</p>
                            <p>Show the errors and information about how to fix the error</p>

                            <Button as={ Link } to={urls.gui.dataBundle.files}>
                                { t('dataBundle.prepareError.backButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(DataBundlePrepareError)
