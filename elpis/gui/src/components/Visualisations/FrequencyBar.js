import React, {Component} from "react";
import {connect} from "react-redux";
import {translate} from "react-i18next";
import {ResponsiveBar} from "@nivo/bar";
import {convertToBarData, calculateTickValues} from "./NivoUtils";
import {Header, Button} from "semantic-ui-react";
import arraySort from "array-sort";

class FrequencyBar extends Component {
    state = {
        dataError: false,
        dataLoaded: false,
        data: 0,
        sortType: "id",
        reverse: false,
    }

    handleSort = (sortBy, data) => () => {
        const {sortType} = this.state;

        console.log("Handling Sort");

        if (sortType !== sortBy) {
            this.setState({
                sortType: sortBy,
                reverse: false,
            });
            arraySort(data, sortBy, {reverse: false});
        } else {
            this.setState({
                reverse: !this.state.reverse,
            });
            arraySort(data, sortBy, {reverse: !this.state.reverse});
        }
    }

    fetchData = (url) => () => {
        fetch(url)
            .then(res => res.json())
            .then(
                (res) => {
                    var tickValues = calculateTickValues(
                        0, 
                        Math.max(...Object.values(res.data)), 
                        8,
                        true,
                        true);

                    console.log(tickValues);
                    this.setState({
                        dataLoaded: true,
                        data: convertToBarData(res.data),
                        tickValues: tickValues,
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

    frequencyIcon = () => {
        if (this.state.sortType !== "frequency") {
            return "ellipsis horizontal";
        } else {
            if (this.state.reverse) {
                return "sort amount down";
            } else {
                return "sort amount up";
            }
        }
    }

    alphabeticalIcon = () => {
        if (this.state.sortType !== "id") {
            return "ellipsis horizontal";
        } else {
            if (this.state.reverse) {
                return "sort alphabet up";
            } else {
                return "sort alphabet down";
            }
        }
    }
    
    render() {
        const {
            dataUrl,
        } = this.props;
        const {
            tickValues,
            dataError,
            dataLoaded,
            data,
        } = this.state;
        const plot =
            dataError ? (
                <div>Error Loading Data: {dataError.message}</div>
            ) : (
                !dataLoaded ? (
                    this.fetchData(dataUrl)
                    (<div>Loading Data...</div>)
                ) : (
                    (<div style={{height: 500}}>
                        <ResponsiveBar
                            data={data}
                            keys={["frequency"]}
                            indexBy="id"
                            colors={"#D3A0F0"}
                            colorBy="index"
                            gridYValues={tickValues}
                            valueScale={{ 
                                type: "linear", 
                                min: Math.min(...tickValues),
                                max: Math.max(...tickValues),
                            }}
                            axisBottom={{
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: -45,
                                legend: "Word",
                                legendPosition: "middle",
                                legendOffset: 50,
                            }}
                            axisLeft={{
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: 0,
                                tickValues: tickValues,
                                legend: "Frequency",
                                legendPosition: "middle",
                                legendOffset: -40,
                            }}
                            margin={{
                                top: 50,
                                right: 50,
                                bottom: 80,
                                left: 60,
                            }}
                        />
                     </div>)
                )
            );

            return (
                <div>
                    <Header as="h1">"Word" Frequency Bar Graph</Header>
                    <div style={{display: "flex"}}>
                        <Button 
                            content="Alphabetical" 
                            icon={this.alphabeticalIcon()} 
                            labelPosition="right" 
                            onClick={this.handleSort("id", data)}
                        />
                        <Button 
                            content="Frequency" 
                            icon={this.frequencyIcon()} 
                            labelPosition="right" 
                            onClick={this.handleSort("frequency", data)}
                        />
                    </div>
                    { plot }
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

export default connect(mapStateToProps)(translate("common")(FrequencyBar));
