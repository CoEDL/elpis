import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Grid, Header, Segment, Icon, Form, Button } from 'semantic-ui-react';
import StepInformer, { NewModelInstructions } from '../StepInformer';
import { setModelName } from '../../redux/actions';
import { connect } from 'react-redux';

class StepNaming extends Component {
    
    handleChangeModelName = (event) => {
        // TODO check for errors in the naming process
        const { setModelName } = this.props;
        setModelName(event.target.value);
        // TODO goto next step
        // TODO verify on the go if this is a valid name or not
        // TODO enable/disable depending on the above comment.
        // TODO Debounce.
    }

    render() {
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
                                <p>{this.props.modelName}</p>
                                <Form.Field>
                                    <input type='text' placeholder='Project Name' onChange={this.handleChangeModelName}/>
                                </Form.Field>
                                <Button type='submit' as={Link} to="/add-data">GO</Button>
                            </Form>
                        </Grid.Column>
                    </Grid>  
                </Segment>
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
      modelName: state.model.name,
    }
  }
  const mapDispatchToProps = dispatch => ({
    setModelName: name => {
      dispatch(setModelName(name))
    },
  })
export default connect(mapStateToProps, mapDispatchToProps)(StepNaming);