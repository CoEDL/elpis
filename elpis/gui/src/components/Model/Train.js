import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Accordion, Dimmer, Loader, Divider, Grid, Header, Segment, Icon, Card, Button, Message, Step } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { withTranslation } from 'react-i18next';
import ReactTimeout from 'react-timeout'
import { modelTrain, modelStatus } from 'redux/actions/modelActions';
import Branding from '../Shared/Branding';
import SideNav from '../Shared/SideNav';
import CurrentModelName from "./CurrentModelName";
import urls from 'urls'

class ModelTrain extends Component {

    state = {
        statusInterval: null,
        activeIndex: null
    }

    componentDidMount = () => {
    }

    handleModelTrain = () => {
        this.props.modelTrain()
        this.setState({...this.state, statusInterval: this.props.setInterval(this.handleModelStatus, 1000)})
    }

    handleModelStatus = () => {
        const { status, modelStatus } = this.props;
        modelStatus()
        if (status === 'trained') this.props.clearInterval(this.state.statusInterval)
    }


    onScroll = () => {
    }
    follow = () => {
    }

    selectAccordion = i => {
        this.setState({...this.state, activeIndex: i })
        return
    }

    render() {
        const { t, currentEngine, name, settings, status, stage_status } = this.props;

        const loadingIcon = (status === 'training') ? (
            <Icon name='circle notched' loading  />
        ) : null

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>

                            <Header as='h1' text='true'>
                                { t('model.train.title') }
                            </Header>

                            <CurrentModelName />

                            {!currentEngine &&
                              <p>{ t('engine.common.noCurrentEngineLabel') }</p>
                            }

                            {currentEngine && !name &&
                              <p>{ t('model.common.noCurrentModelLabel') }</p>
                            }

                            {currentEngine && name &&
                            <>

                                {/* Only Kaldi has settings. Should make this dynamic */}
                                {currentEngine && currentEngine == 'kaldi' &&
                                    <Card fluid>
                                        <Card.Content header={t('model.train.settingsHeader')}/>
                                        <Card.Content description={t('model.settings.ngramLabel') + ' ' + settings.ngram}/>
                                    </Card>
                                }

                                <Message icon>
                                    {/*{loadingIcon}*/}
                                    <Message.Content className="train-log">

                                        {stage_status &&
                                        <div className="stages">
                                            <Accordion
                                                fluid
                                                styled
                                                exclusive={false}
                                            >
                                            {Object.keys(stage_status).map((stage, i) => {


                                                let name = stage_status[stage]["name"]
                                                let status = stage_status[stage]["status"]
                                                let message = stage_status[stage]["message"]
                                                let log = stage_status[stage]["log"]
                                                let icon = (status === "in-progress") ?
                                                    (<Icon name='circle notched' loading />) :
                                                    (<Icon name='dropdown' />)
                                                let stage_status_icon = (status === "complete") ?
                                                    (<Icon name='check' />) :
                                                    ('')

                                                    return (
                                                        <div key={name}>
                                                            <Accordion.Title
                                                              index={i}
                                                              active={this.state.activeIndex === i || status === "in-progress"}
                                                              onClick={() => this.selectAccordion(i)}
                                                            >
                                                                {icon}
                                                                {name} {stage_status_icon}
                                                            </Accordion.Title>

                                                            <Accordion.Content
                                                                className="accordion_log"
                                                                active={this.state.activeIndex === i}>
                                                                {log}
                                                            </Accordion.Content>
                                                        </div>
                                                    )
                                                }
                                            )}

                                            </Accordion>

                                            <p>{status}</p>

                                        </div>
                                        }
                                    </Message.Content>
                                </Message>

                                <Segment>

                                    <Button onClick={this.handleModelTrain} disabled={!name || status !== 'ready'}>
                                        {t('model.train.trainButton')}
                                    </Button>

                                    <Button as={Link} to={urls.gui.model.results}
                                            disabled={status === 'ready' || status === "training"}>
                                        {t('common.nextButton')}
                                    </Button>

                                </Segment>
                            </>
                            }

                        </Grid.Column>
                    </Grid>
                </Segment>

            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        name: state.model.name,
        settings: state.model.settings,
        status: state.model.status,
        stage_status: state.model.stage_status,
        currentEngine: state.engine.engine
    }
}
const mapDispatchToProps = dispatch => ({
    modelTrain: () => {
        dispatch(modelTrain())
    },
    modelStatus: () => {
        dispatch(modelStatus())
    },
})
export default connect(mapStateToProps, mapDispatchToProps)(
    withTranslation("common")(
        ReactTimeout(ModelTrain)
    )
);
