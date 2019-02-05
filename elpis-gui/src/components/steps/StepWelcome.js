import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';
import { newModel } from '../../redux/actions';
import { connect } from 'react-redux';

class StepWelcome extends Component {

    handleNewModel = () => {
        this.props.newModel();
        this.props.history.push('/naming')
    }

    render() {
        const { t } = this.props

        return (
            <div>
                <Grid centered row={6}>
                    <Grid.Row centered>
                        <StepBranding />
                    </Grid.Row>

                    <Grid.Row centered>
                        <Segment>
                            <Button onClick={this.handleNewModel}>
                                {t('welcome.newModelButton')}
                            </Button>
                            <Button as={Link} to="/new-transcription">
                                {t('welcome.newTranscriptionButton')}
                            </Button>
                        </Segment>
                    </Grid.Row>

                    <Grid.Row centered>
                        <Container>
                            <Segment>
                                <Header as='h2'>Instructional Video</Header>
                                <p>{t('welcome.intro', {passInSomething:"memememe"})}</p>
                            </Segment>
                        </Container>
                    </Grid.Row>

                    <Grid.Row centered>
                        <StepInformer instructions={NewModelInstructions} />
                    </Grid.Row>

                </Grid>
            </div>
        );
      }
}


const mapDispatchToProps = dispatch => ({
    newModel: () => {
        dispatch(newModel());
    }
})

export default withRouter(
    connect(
        null,
        mapDispatchToProps
    )(
        translate('common')(StepWelcome)
    )
);
