import React, {Component} from "react";
import {connect} from "react-redux";
import {withTranslation} from "react-i18next";
import {ResponsiveSankey} from "@nivo/sankey";
import {Header} from "semantic-ui-react";
// import urls from "urls";

class SankeyWordOrder extends Component {
    state = {
        dataError: false,
        dataLoaded: false,
        data: 0,
    }

    fetchData = (url) => () => {
        fetch(url)
            .then(res => res.json())
            .then(
                (res) => {
                    this.setState({
                        dataLoaded: true,
                        data: res.data,
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
            dataUrl,
        } = this.props;
        const {
            // activeTab,
            dataError,
            dataLoaded,
            data,
        } = this.state;
        const plot =
            dataError ? (
                <div>Error Loading Data: {dataError.message}</div>
            ) : (
                !dataLoaded ? (
                    this.fetchData(dataUrl)(<div>Loading Data...</div>)
                ) : (
                    (
                        <div style={{height: 500}}>
                            <ResponsiveSankey
                                data={data.sankey}
                                margin={{
                                    top: 50,
                                    right: 50,
                                    bottom: 80,
                                    left: 60,
                                }}
                            />
                        </div>
                    )
                )
            );

            return (
                <div>
                    <div>
                        <Header as="h1">Sankey Order Visualisation</Header>
                        <p>This visualisation gives an overview of the ordering in the 
                            corpus. Note that this is a trimmed dataset that only shows 
                            the strongest links as the underlying utility does not support
                            circular links. 
                        </p>
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

export default connect(mapStateToProps)(withTranslation("common")(SankeyWordOrder)); 
