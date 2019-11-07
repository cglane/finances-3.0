import React, {Component} from 'react';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';

const styles = {
  customWidth: {
    width: 150,
  },
};


export default class SelectFieldExampleSimple extends Component {
    state = {
      value: 1,
    };
  
    handleChange = (event, index, value) => {
      this.setState({value})
      if (this.props.onChange) {
        this.props.onChange(value)        
      }
    };
  
    render() {
      return (
        <div>
          <SelectField
            floatingLabelText="Sheet Title"
            value={this.state.value}
            onChange={this.handleChange}
          >
          {this.props.items.map((item, index) => {
               return (
                <MenuItem key={index} value={item} primaryText={item}/>                
              )
            })
          }
          </SelectField>
        </div>
      );
    }
  }