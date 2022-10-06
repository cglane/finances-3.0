
import React from 'react';
import $ from 'jquery'
import {DefaultButton, SelectField} from '../components';
import ReactFileReader from 'react-file-reader';
// import RaisedButton from 'material-ui/RaisedButton';
import Button from '@mui/material/Button';

const createReactClass = require('create-react-class');
const csvOptions = ['AMEX', 'CapitolOne', 'BOA']

const styles = {
    "marginLeft": '10%'
}



const UploadPage = createReactClass({
 getInitialState() {
        return {
            value: 'Authenticate',
            fileType: null
        };
    },
    
handleChange(fileType) {
    this.setState({
        fileType: fileType
    });
},
sendToServer(type, csvList, userId){
    $.ajax({
        url: 'http://localhost:8000/api/v1/read_csv',
        type: "POST",      
        dataType : "json",        
        data: JSON.stringify({type, csvList, userId}),
        contentType: "application/json; charset=utf-8",
        crossDomain: true,        
        dataType: 'json',
        success: function (data) {
            console.log(data, 'data')
            console.log(data.keys, 'data')
            if (data.keys) {
            console.log(this.props, 'props')
               this.props.handleChange('Results', data['keys'], data['rows'])
              }
        }.bind(this),
        error: function (data) {
           if (data && data.responseJSON) {
                alert(data.responseJSON.msg)
           }
         }
      });
    },
handleFiles(files){
        var reader = new FileReader();
        reader.onload = function(e) {
            const allTextLines = reader.result.split(/\r\n|\n/);
            this.sendToServer(this.state.fileType, allTextLines, this.props.userId)
        }.bind(this)
      reader.readAsText(files[0]);
    },
    render() {
        let fileReaderButton = null;        
        if(this.state.fileType) {
         fileReaderButton = 
         <ReactFileReader handleFiles={this.handleFiles} fileTypes={'.csv'}>
            <Button            
                label={'Upload'}
                labelPosition="before"
                containerElement="label"
                >
            </Button>                    
        </ReactFileReader>
        } 
        return (
            <div style={styles}>
                <h1>Upload </h1>
                <SelectField onChange={this.handleChange} items={csvOptions}/>
                {fileReaderButton}  
            </div>
            )
        }
})
export default UploadPage