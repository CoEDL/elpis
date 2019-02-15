import React, { Component } from 'react';
import { Grid, Header, Segment, Icon, Button } from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Steps/Shared/Branding';
import Informer from 'components/Steps/Shared/Informer';

class ModelLexicon extends Component {
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
                                { t('model.lexicon.title') }
                            </Header>


                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}
export default translate('common')(ModelLexicon)
