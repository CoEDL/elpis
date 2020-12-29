import React, {Component} from 'react';
import {Link} from "react-router-dom";
import {Grid, Button, Header, Container, Segment, Placeholder} from 'semantic-ui-react';
import {connect} from 'react-redux';
import {withTranslation} from 'react-i18next';
import Branding from './Shared/Branding';
import urls from 'urls'

class StepWelcome extends Component {

    render() {
        const {t, list} = this.props
        return (

            <Grid>
                <Grid.Row centered>
                    <Grid.Column>
                        <Branding/>
                    </Grid.Column>
                </Grid.Row>

                <Grid.Row>
                    <Grid.Column>
                        <Segment>
                            <div className="keep-line-breaks">{t('welcome.description')}</div>
                        </Segment>
                        <Segment>
                            <p>
                                <Link to={urls.gui.engine.index}>{t('welcome.start')}</Link>
                            </p>
                        </Segment>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
    }
}


export default withTranslation("common")(StepWelcome)
