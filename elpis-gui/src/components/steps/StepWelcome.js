import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Grid, Button, Header, Container, Segment, } from 'semantic-ui-react';
import StepBranding from './StepBranding';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { translate } from 'react-i18next';

class StepWelcome extends Component {

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
                            <Button as={Link} to="/naming">
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

// translate uses a namespace
export default translate('common')(StepWelcome)
