import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';


const styles = {
  button: {
    margin: 12,
  },
  exampleImageInput: {
    cursor: 'pointer',
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    width: '100%',
    opacity: 0,
  },
};

const DefaultButton = (props) => (
    <RaisedButton
      onClick={() => props.onSomeEvent(props.path, props.tableData)}
      label={props.label}
      labelPosition="before"
      style={styles.button}
      containerElement="label"
    >
    </RaisedButton>

);

export default DefaultButton;