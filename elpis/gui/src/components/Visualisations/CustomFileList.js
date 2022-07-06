import React, {Component} from "react";
import {connect} from "react-redux";
import {translate} from "react-i18next";
import {getSizeGenerator} from "@nivo/swarmplot";
import CustomNode from "./CustomFileNodeVisualisation";
import {Table, Header, List} from "semantic-ui-react";
import urls from "urls";

class CustomFileList extends Component {
    state = {
        activeTab: 0,
        dataError: false,
        dataLoaded: false,
        data: 0,
    }

    fetchData = () => {
        fetch(urls.api.statistics.swarmplot)
            .then(res => res.json())
            .then(
                (res) => {
                    console.log(res.data);
                    this.setState({
                        dataLoaded: true,
                        data: res.data,
                        minCount: Math.min(...res.data.swarmplot.map(node => node.count)),
                        maxCount: Math.max(...res.data.swarmplot.map(node => node.count)),
                    });
                },
                (error) => {
                    this.setState({
                        dataLoaded: true,
                        dataError: error,
                    });
                }
            );
    }
    
    render() {
        const { 
            t, 
            additionalTextFiles, 
            status, 
            wordlist, 
        } = this.props;
        const {
            activeTab,
            dataError,
            dataLoaded,
            data,
            minCount,
            maxCount,
        } = this.state;
        const getSize = getSizeGenerator({
            key: "count",
            values: [minCount, maxCount],
            sizes: [55, 75],
        });
        const fileRows = (dataLoaded && !dataError) ? (
            data.swarmplot.map((node, index) => (
                <Table.Row>
                    <Table.Cell>
                        <svg viewBox="0 0 100 100">
                            <CustomNode
                                node = {{
                                    data: {
                                        annotated: node.annotated,
                                    },
                                    id: node.file,
                                }}
                                size = {getSize(node)}
                                x = {50}
                                y = {50}
                            />
                        </svg>
                    </Table.Cell>
                    <Table.Cell>
                        {node.file} 
                    </Table.Cell>
                    <Table.Cell>
                        {node.count}
                    </Table.Cell>
                    <Table.Cell>
                        {Number.parseFloat(node.annotated * 100).toFixed(1)}
                    </Table.Cell>
                    <Table.Cell>
                        {Number.parseFloat(node.length).toFixed(1)} seconds
                    </Table.Cell>
                </Table.Row>
            ))) : null;
        const fileTable = 
            (<Table celled padded>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Visualisation</Table.HeaderCell>
                        <Table.HeaderCell singleLine>File Name</Table.HeaderCell>
                        <Table.HeaderCell>Annotated Words</Table.HeaderCell>
                        <Table.HeaderCell>Annotated %</Table.HeaderCell>
                        <Table.HeaderCell>Audio Length</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    { fileRows }
                </Table.Body>
            </Table>);
        const plot =
            dataError ? (
                <div>Error Loading Data: {dataError.message}</div>
            ) : (
                !dataLoaded ? (
                    this.fetchData
                    (<div>Loading Data...</div>)
                ) : (
                    fileTable
                )
            );
        
        return (
            <div>
                <div>
                    <Header as="h1">File List</Header>
                    <p>This is a list of all the files included in the dataset. Specifically it includes interesting stats about the file pairs.</p>
                    <List bulleted>
                        <List.Item>Visualisation: The graphic generated for a file as seen in the swarmplot visualisation.</List.Item>
                        <List.Item>File Name: File name of the pair the row represents.</List.Item>
                        <List.Item>Annotated Words: Annotated "words" is the number of space separated "words" in the EAF file for the file pair.</List.Item>
                        <List.Item>Annotated %: Percentage of the audio file that is annotated. Calculated by taking the summed timespan of annotations and dividing by file length.</List.Item>
                        <List.Item>Annotation Length: Length of annotated audio in seconds.</List.Item>
                        <List.Item>Audio Length: Length of the audio file uploaded in seconds.</List.Item>
                    </List>
                </div>
                <div>
                    { plot }
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        name: state.dataset.name,
        wordlist: state.dataset.wordlist,
        additionalTextFiles: state.dataset.additionalTextFiles,
        status: state.dataset.status,
    };
};

export default connect(mapStateToProps)(translate("common")(CustomFileList));
