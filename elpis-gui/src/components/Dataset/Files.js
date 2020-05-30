import React, { Component } from 'react';
import { Link, withRouter } from "react-router-dom";
import { Button, Select, Divider, Form, Grid, Header, Icon, Input, List, Message, Segment, Table } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { translate } from 'react-i18next';
import { datasetSettings, datasetPrepare } from 'redux/actions/datasetActions';
import Branding from 'components/Shared/Branding';
import SideNav from 'components/Shared/SideNav';
import FileUpload from './FileUpload';
import CurrentDatasetName from "./CurrentDatasetName";
import urls from 'urls'

class DatasetFiles extends Component {

    handleNextButton = () => {
        const { history, datasetPrepare} = this.props
        datasetPrepare(history)
        history.push(urls.gui.dataset.prepare)
    }

    render() {

        const { t, name, status, audioFiles, transcriptionFiles, additionalTextFiles, settings, ui, datasetSettings } = this.props;

        const interactionDisabled = name ? false : true

        const loadingIcon = (status === 'loading') ? (
            <div className="status">
                <Icon name='circle notched' size="big" loading /> Uploading files
            </div>
        ) : null

        const audioFileList = audioFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))
        const transcriptionFilesList = transcriptionFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))
        const additionalTextFilesList = additionalTextFiles.map(file => (
            <List.Item key={ file }>
                <List.Content>{ file }</List.Content>
            </List.Item>
        ))

        const filesHeader = (
            audioFileList.length > 0 ||
            transcriptionFilesList.length > 0 ||
            additionalTextFilesList.length > 0) ? (
                 t('dataset.files.filesHeader')
            ) : null

        // const writeCountOptions = []
        // for (var i = 1; i <= settings.tier_max_count; i++) {
        //     writeCountOptions.push(
        //         <option key={i} value={i}>{i}</option>
        //     )
        // }

        return (
            <div>
                <Branding />
                <Segment>
                    <Grid centered>
                        <Grid.Column width={ 4 }>
                            <SideNav />
                        </Grid.Column>

                        <Grid.Column width={ 12 }>
                            <Header as='h1'>
                                { t('dataset.files.title') }
                            </Header>

                            <CurrentDatasetName />

                            <Message attached content={ t('dataset.files.description') } />

                            <Segment className="attached">

                                <FileUpload name={name} />

                                <div>{loadingIcon}</div>

                                <Header as='h3'>
                                    { filesHeader }
                                </Header>

                                <Grid columns={ 3 }>
                                    <Grid.Column>
                                        <List>
                                            { audioFileList }
                                        </List>
                                    </Grid.Column>
                                    <Grid.Column>
                                        <List>
                                            { transcriptionFilesList }
                                        </List>
                                    </Grid.Column>
                                    <Grid.Column>
                                        <List>
                                            { additionalTextFilesList }
                                        </List>
                                    </Grid.Column>
                                </Grid>
                            </Segment>
                            <Segment>
                                <Header as='h3'>
                                    { t('dataset.files.settingsHeader') }
                                </Header>

                                <SettingsForm settings={settings} ui={ui} datasetSettings={datasetSettings} />
                            </Segment>

                            <Divider />

                            <Button onClick={this.handleNextButton} disabled={interactionDisabled}>
                                { t('common.nextButton') }
                            </Button>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }
}


const SettingsForm = ({settings, ui, datasetSettings}) => {
    console.group("SettingsForm");
    console.log({settings});
    console.log({ui});
    const handleSubmit = props => {}

    // Sort names into groups by title followed by settings.
    let settingGroups = [];
    {
        // scope protect.
        let group = [];
        ui['order'].forEach(ui_name => {
            if (ui['type'][ui_name] === "title" && group.length !== 0) {
                settingGroups.push(group);
                group = []; // clear for the next group
            }
            group.push(ui_name);
        });
        if (group.length !== 0) { // add the last group
            settingGroups.push(group);
        }
    }

    // Construct individual tables
    let tables = [];
    {
        let groupIndex = 0;
        settingGroups.forEach(group => {
            let header = null;
            let settingRows = [];

            // Construct table rows for group
            group.forEach(ui_name => {
                console.group("Row for " + ui_name);
                if (ui['type'][ui_name] === "title") {
                    console.log("Building title");
                    header = (
                        <Table.Row>
                            <Table.HeaderCell colSpan='2'>{ui['data'][ui_name]['title']}</Table.HeaderCell>
                        </Table.Row>
                    );
                } else { // ui['type'][ui_name] == "settings"
                    console.log("Building input");
                    let data = ui['data'][ui_name];
                    let label = data.display_name !== null ? data.display_name : ui_name;

                    // Switch input type based on importer ui specification
                    let dataEntryElement;
                    switch (data.type) {
                        case 'str': {
                            dataEntryElement = (<Input type='text' />);
                        }
                        break;
                        case 'int': {
                            dataEntryElement = (<Input type='number' />);
                        }
                        break;
                        default: /*ENUM*/ {
                            let options = [];
                            data.type.forEach(v => {
                                if (v === null) {
                                    console.log("pushing: ", {key: "- not selected -", value: "- not selected -", text: "- not selected -"});
                                    options.push({key: "- not selected -", value: "- not selected -", text: "- not selected -"})
                                }
                                else {
                                    console.log("pushing: ", {key: v, value: v, text: v});
                                    options.push({key: v, value: v, text: v})
                                }
                            });
                            dataEntryElement = (<Select
                                options={options}
                                // value={settings[ui_name]}
                                onChange={(event, data)=>{
                                    let newSettings = { ...settings };
                                    if (data.value === "- not selected -") {
                                        newSettings[ui_name] = null;
                                    } else {
                                        newSettings[ui_name] = data.value;
                                    }
                                    console.log("Sending new settings: ", {newSettings});
                                    datasetSettings(newSettings)
                                }}
                                selection
                            />);
                            // TODO: add a onChange that dispatches the setting (do this for int and string as well)
                        }
                    }

                    // Construct row for individual setting
                    let row = (
                        <Table.Row key={ui_name}>
                            <Table.Cell collapsing>{label}</Table.Cell>
                            <Table.Cell>{dataEntryElement}</Table.Cell>
                        </Table.Row>
                    );
                    settingRows.push(row);
                }
                console.groupEnd();
            });

            // Construct table
            let table = (
                <Table celled striped key={groupIndex++}>
                    {header===null?null:(
                        <Table.Header>
                            {header}
                        </Table.Header>
                    )}
                    <Table.Body>
                        {settingRows}
                    </Table.Body>
                </Table>
            );
            tables.push(table);
        });
    }

    /* Generate the settings */
    // let elements = []
    // ui['order'].forEach(ui_name => {
    //     let element = null;
    //     if (ui['type'][ui_name] === "title") {
    //         element = <Header key={ui_name} as="h4">{ui['data'][ui_name]['title']}</Header>;
    //     } else {
    //         let data = ui['data'][ui_name];
    //         let label = data.display_name !== null ? data.display_name : ui_name;
    //         let ooo = [
    //             { key: 'au', value: 'au', text: 'AU' },
    //             { key: 'az', value: 'az', text: 'AZ' }
    //         ];
    //         element = (<div key={ui_name} >
    //             <p>Type: {data.type}</p>
    //             <p>Display name: {label}</p>
    //             <Message attached content={data.description} />
    //             <Select placeholder="whats uuuup:" options={ooo} />
    //         </div>)
    //     }
    //     elements.push(element);
    // });
    console.log("here");
    console.groupEnd();
    return (<>
        <Form onSubmit={handleSubmit}>
            {tables}
        </Form>
    </>);
}

const mapStateToProps = state => {
    return {
        name: state.dataset.name,
        audioFiles: state.dataset.audioFiles,
        transcriptionFiles: state.dataset.transcriptionFiles,
        additionalTextFiles: state.dataset.additionalTextFiles,
        settings: state.dataset.settings,
        ui: state.dataset.ui,
        status: state.dataset.status
    }
}

const mapDispatchToProps = dispatch => ({
    datasetSettings: postData => {
        dispatch(datasetSettings(postData));
    },
    datasetPrepare: (history) => {
        dispatch(datasetPrepare(history))
            .then((response) => {
                history.push(urls.gui.dataset.prepare)
            })
    }
})

export default withRouter(
    connect(
        mapStateToProps,
        mapDispatchToProps
    )(
        translate('common')(DatasetFiles)
    )
);
