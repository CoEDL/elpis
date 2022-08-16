import React, {Component} from "react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {ResponsiveSwarmPlot} from "@nivo/swarmplot";
import {BasicTooltip} from "@nivo/tooltip";
import {useTheme} from "@nivo/core";
import {calculateTickValues} from "./NivoUtils";
import {Header, List} from "semantic-ui-react";
import CustomNode from "./CustomFileNodeVisualisation";
import urls from "urls";

class DatasetOverviewSwarmplot extends Component {
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
                    var tickValues = calculateTickValues(
                        Math.min(...res.data.swarmplot.map(node => node.length)), 
                        Math.max(...res.data.swarmplot.map(node => node.length)), 
                        8);

                    this.setState({
                        dataLoaded: true,
                        data: res.data,
                        tickValues: tickValues,
                        minLength: Math.min(...tickValues),
                        maxLength: Math.max(...tickValues),
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
            tickValues,
            minLength,
            maxLength,
            minCount,
            maxCount,
        } = this.state;
        const tooltipContent = ({node}) => (() => 
            (<div style={useTheme().tooltip.basic}>
                <span>
                    <strong>{node.id}</strong>
                    <List value="-" size="tiny">
                        <List.Item><strong>{Number.parseFloat(node.data.length).toFixed(1)} mins</strong></List.Item>
                        <List.Item><strong>{node.data.count} words</strong></List.Item>
                        <List.Item><strong>{Number.parseFloat(node.data.annotated * 100).toFixed(1)} % annotated</strong></List.Item>
                    </List>
                </span>
             </div>)
        );
        const tooltip = (node) => (
            <BasicTooltip
                renderContent={tooltipContent(node)}
            />
        );
        const plot =
            dataError ? (
                <div>Error Loading Data: {dataError.message}</div>
            ) : (
                !dataLoaded ? (
                    this.fetchData
                    (<div>Loading Data...</div>)
                ) : (
                    (<div style={{height: 500}}>
                        <ResponsiveSwarmPlot
                            data={data.swarmplot}
                            value = "length"
                            identity = "file"
                            label="file"
                            groups={["Files"]}
                            size={{
                                key: "count",
                                values: [minCount, maxCount],
                                sizes: [55, 75],
                            }}
                            colors={"#D3A0F0"}
                            spacing={12}
                            enableGridY={true}
                            enableGridX={false}
                            valueScale={{ 
                                type: "linear", 
                                min: minLength,
                                max: maxLength,
                            }}
                            gridYValues={tickValues}
                            axisBottom={{
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: -45,
                                legend: "Each node represents a file with sizes relative to the number of annotated words.",
                                legendPosition: "middle",
                                legendOffset: 50,
                            }}
                            axisLeft={{
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: 0,
                                tickValues: tickValues,
                                legend: "Audio Length (seconds)",
                                legendPosition: "middle",
                                legendOffset: -40,
                            }}
                            axisRight={null}
                            axisTop={null}
                            margin={{
                                top: 50,
                                right: 50,
                                bottom: 80,
                                left: 60,
                            }}
                            renderNode={props => <CustomNode {...props} />}
                            tooltip={tooltip}
                        />
                    </div>)
                )
            );

            return (
                <div>
                    <div>
                        <Header as="h1">File List</Header>
                        <p>This visualisation gives an overview of the file pairs in the dataset. You can hover over each blob to get the file name if the blob isn't labelled.</p>
                        <List bulleted>
                            <List.Item>Size: The number of annotated "words" in the file pair. Annotated "words" is the number of space separated "words" in the EAF file for the file pair.</List.Item>
                            <List.Item>Vertical Position: Audio length of the file.</List.Item>
                            <List.Item>Internal Pie/Arc: Percentage annotated.</List.Item>
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

export default connect(mapStateToProps)(withTranslation("common")(DatasetOverviewSwarmplot));
