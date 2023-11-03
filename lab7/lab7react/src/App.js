import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      email: ''
    }
    }  

  render() {
	  return(
      <div className="App">
        <form id="contact-form" onSubmit={this.handleSubmit.bind(this)} method="POST">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input type="text" className="form-control" value={this.state.name} onChange={this.onNameChange.bind(this)} />
          </div>
          <div className="form-group">
            <label htmlFor="exampleInputEmail1">Email address</label>
            <input type="email" className="form-control" aria-describedby="emailHelp" value={this.state.email} onChange={this.onEmailChange.bind(this)} />
          </div>
        
          <button type="submit" className="btn btn-primary">Submit</button>
        </form>
      </div>
	);
}
onNameChange(event) {
  this.setState({name: event.target.value});
}
 
onEmailChange(event) {
  this.setState({email: event.target.value});
}
 
  handleSubmit(event) {
  event.preventDefault();
  console.log(this.state);
  fetch('http://localhost:5000/insert', {
    mode:'cors',
    method: "POST",
    body: JSON.stringify(this.state),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
    
  .then ( (data) => {
    return data.json()
  }).then( (json) => {
    console.log( json.data )
  }) 
  }
}

export default App;
