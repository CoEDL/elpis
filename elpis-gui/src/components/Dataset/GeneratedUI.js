import React, { useEffect } from 'react';
import { Select, Form, Input, Table, TextArea } from 'semantic-ui-react';

function groupSettingsFromUI(ui) {
    let settingGroups = [];
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
    return settingGroups;
}


const GeneratedUI = ({settings, ui, changeSettingsCallback}) => {
    // console.group("GeneratedUI");
    // console.log({settings});
    // console.log({ui});

    const forceUpdate = React.useState()[1].bind(null, {})  // see NOTE above

    // On initialisation of component, show the tier name and set it properly
    useEffect(() => {
        if (settings !== null) {
            const selection_mechanism = settings['selection_mechanism']
            ui['data'][selection_mechanism]['shown'] = true;
            // If settings haven't been set, set to the first option
            if (settings[selection_mechanism] === "") {
                settings[selection_mechanism] = ui['data'][selection_mechanism]['options'][0]
            }
            changeSettingsCallback(settings)
        }
    }, [ui])

    if (ui === null || ui === undefined) {
        // console.groupEnd();
        return (<>No Settings.</>);
    }

    const handleStrChange = (ui_name, data) => {
        // console.log(ui_name, data)
        let newSettings = { ...settings };
        newSettings[ui_name] = data.value
        changeSettingsCallback(newSettings)
    }

    const handleSelectChange = (ui_name, data) => {
        let newSettings = {...settings};
        if (ui_name === "selection_mechanism") {
            // Hide other selection mechanisms and show current one
            for (const option of data.options) {
                newSettings[option.value] = null;
                ui['data'][option.value]['shown'] = false;
            }
            ui['data'][data.value]['shown'] = true;
            // Update new settings with default value of selected mechanism
            newSettings[data.value] = ui['data'][data.value]['options'][0]
        }
        if (newSettings[ui_name]) {
            newSettings[ui_name] = data.value
        }
        changeSettingsCallback(newSettings)
    }
    
    // Sort names into groups by title followed by settings.
    let settingGroups = groupSettingsFromUI(ui);

    // Construct individual tables
    let tables = [];
    let groupIndex = 0;
    settingGroups.forEach(group => {
        let header = null;
        let settingRows = [];

        // Construct table rows for group
        group.forEach(ui_name => {
            // console.group("Row for " + ui_name);
            if (ui['type'][ui_name] === "title") {
                // console.log("Building title");
                header = (
                    <>
                        <Table.Row>
                            <Table.HeaderCell colSpan='2'>{ui['data'][ui_name]['title']}</Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell colSpan='2' className='description'>{ui['data'][ui_name]['description']}</Table.HeaderCell>
                        </Table.Row>
                    </>
                );
            } else { // ui['type'][ui_name] == "settings"
                // console.log("Building input");
                let data = ui['data'][ui_name];
                if (data.shown) {
                    let label = (data.display_name !== null) ? data.display_name : ui_name;
                    // Switch input type based on ui specification
                    let dataEntryElement;
                    switch (data.ui_format) {
                        case 'text': {
                            dataEntryElement = (<Input
                                    type='text'
                                    value={settings[ui_name]}
                                    onChange={(event, data) => {
                                        handleStrChange(ui_name, data)
                                    }} />);
                            }
                            break;
                        case 'textarea': {
                            dataEntryElement = (<TextArea
                                    value={settings[ui_name]}
                                    onChange={(event, data) => {
                                        handleStrChange(ui_name, data)
                                    }} />);
                            }
                            break;
                        case 'int': {
                            dataEntryElement = (<Input type='number'/>); /* TODO */
                            }
                            break;
                        case 'select': {
                            let options = [];
                            // Build options
                            data.options.forEach(v => {
                                options.push({key: v, value: v, text: v})
                            });
                            dataEntryElement = (<Select
                                defaultValue={settings[ui_name]}
                                options={options}
                                onChange={(event, data) => {
                                    handleSelectChange(ui_name, data)
                                }}
                                selection
                            />);
                            // TODO: add a onChange that dispatches the setting (do this for int and string as well)
                            }
                            break;
                        default: {
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
            }
            // console.groupEnd();
        });

        // Construct table
        let table = (
            <Table celled striped key={groupIndex++} className='settings'>
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
    // console.groupEnd();
    return (<>
        <Form>
            {tables}
        </Form>
    </>);
}

export default GeneratedUI;