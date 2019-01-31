import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Grid, Header, Segment, Icon, Form, Button, Divider, Label } from 'semantic-ui-react';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { updateModelName } from '../../redux/actions';
import { connect } from 'react-redux';

class StepNaming extends Component {
    
    handleChangeModelName = (event) => {
        // TODO check for errors in the naming process
        const { updateModelName } = this.props;
        updateModelName({name: event.target.value});
        // TODO goto next step
        // TODO verify on the go if this is a valid name or not
        // TODO enable/disable depending on the above comment.
        // TODO Debounce.
    }

    render() {
        const {modelName} = this.props;
        return(
            <div>
                <Header as='h1'>ELPIS LOGO (ACCELERATE TRANSCRIPTION)</Header>
                <Segment>
                    <Grid centered>
                        <Grid.Column width={6}>
                            <StepInformer instructions={NewModelInstructions} />
                        </Grid.Column>
                        <Grid.Column width={10}>
                            <Header as='h1' text="true"> <Icon name='setting' /> Build a new model </Header>
                            <Form>
                                <Form.Field>
                                    <input
                                        type='text'
                                        placeholder='Project Name'
                                        onChange={this.handleChangeModelName}
                                        value={modelName}
                                    />
                                    {/* {modelList.indexOf(modelName) > -1 ? (<Label basic color='red' pointing>
                                        Model name already exists
                                    </Label>):(<div/>)} */}
                                </Form.Field>
                                <Button type='submit' as={Link} to="/add-data" >GO</Button>
                                {/* <Button type='submit' as={Link} to="/add-data" disabled={modelList.indexOf(modelName) > -1 || modelName===""}>GO</Button> */}
                            </Form>
                            <Divider />
                            {/* {modelList} */}
                        </Grid.Column>
                    </Grid>  
                </Segment>
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        modelName: state.apiModelReducer.name,
    }
  }
  const mapDispatchToProps = dispatch => ({
    updateModelName: name => {
      dispatch(updateModelName(name))
    },
  })
export default connect(mapStateToProps, mapDispatchToProps)(StepNaming);
// export default StepNaming;