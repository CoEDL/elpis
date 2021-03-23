import React, { Component } from 'react';
import { Grid, Header, Segment } from 'semantic-ui-react';
import { withTranslation } from 'react-i18next';
import Branding from '../Shared/Branding';
import SideNav from '../Shared/SideNav';
import NewForm from '../Model/NewForm';


class ModelNew extends Component {

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
                                { t('model.new.title') }
                            </Header>

                            <NewForm />

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}


export default withTranslation("common")(ModelNew);
