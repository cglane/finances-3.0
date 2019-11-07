import $ from 'jquery'

import React from 'react';
import GoogleLogin from 'react-google-login';
import {DefaultButton} from '../components';

const createReactClass = require('create-react-class');


const AuthenticatePage = createReactClass({
 getInitialState() {
        return {
            value: 'Authenticate'
        };
    },
    handleClick() {
        console.log('authenticate')
        this.props.handleChange('Upload', null, null, '')
    },
    responseGoogle(res) {
        console.log(res, 'res')
         $.ajax({
        url: 'http://localhost:8000/api/v1/authorize',
        type: "POST",
        dataType : "json",
        data: JSON.stringify(res),
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        dataType: 'json',
        success: function (data) {
           console.log(data, 'data')
           this.props.handleChange('Upload', null, null, data.userId)

        }.bind(this),
        error: function (data) {
          console.log(data, 'datumk')
         }
      });
    },
    failureResponse(res) {
        alert('Failure to authenticate!')

    },

    render() {
        return (
            <div>
                <h1>Activate </h1>
                 <GoogleLogin
                    clientId="202096165736-655hc8iotb8s5ce1jcaog5qm0rpruqmb.apps.googleusercontent.com"
                    buttonText="Login"
                    onSuccess={this.responseGoogle}
                    onFailure={this.failureResponse}
                  />
                <DefaultButton label={'Continue'} onSomeEvent= {this.handleClick} path="Upload"> Upload </DefaultButton>
             </div>
            )
        }
})
export default AuthenticatePage