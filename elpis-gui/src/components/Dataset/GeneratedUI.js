import React from 'react';
import { Select, Form, Input, Table } from 'semantic-ui-react';

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
    console.group("GeneratedUI");
    console.log({settings});
    console.log({ui});

    if (ui === null || ui === undefined) {
        return (<>No Settings.</>);
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
                let label = (data.display_name !== null) ? data.display_name : ui_name;

                // Switch input type based on ui specification
                let dataEntryElement;
                switch (data.type) {
                    case 'str': {
                        dataEntryElement = (<Input type='text' />); /* TODO */
                    }
                    break;
                    case 'int': {
                        dataEntryElement = (<Input type='number' />); /* TODO */
                    }
                    break;
                    default: /*ENUM*/ {
                        let options = [];
                        data.type.forEach(v => {
                            // <Select> does not like to display text if the key or value (?) is null.
                            // So convert null to string "- not selected -".
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
                            onChange={(event, data)=>{
                                let newSettings = { ...settings };
                                // Convert from "not selected" string back to null.
                                if (data.value === "- not selected -") {
                                    newSettings[ui_name] = null;
                                } else {
                                    newSettings[ui_name] = data.value;
                                }
                                changeSettingsCallback(newSettings)
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
    console.groupEnd();
    return (<>
        <Form>
            {tables}
        </Form>
    </>);
}

export default GeneratedUI;