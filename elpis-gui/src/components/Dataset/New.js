import React, { Component } from 'react';
import { Grid, Header, Segment } from 'semantic-ui-react';
import { translate } from 'react-i18next';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import NewForm from 'components/Dataset/NewForm';


class DatasetNew extends Component {

    componentDidMount() {}

    render() {
        const { t } = this.props;
        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1' text="true">
                                { t('dataset.new.title') }
                            </Header>

                            <NewForm />

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        )
    }
}

export default translate('common')(DatasetNew)
