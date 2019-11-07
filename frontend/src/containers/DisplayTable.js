import React from 'react';
import {is, map, keys, pick} from 'ramda'
import {
  Table,
  TableBody,
  TableHeader,
} from 'material-ui/Table';
import {TableRowCustom, DefaultButton} from '../components'
const createReactClass = require('create-react-class');

/**
 * A simple table demonstrating the hierarchy of the `Table` component and its sub-components.
 */
 

const hintFields = [
       '',
       '',
       '',
       '',
       "Work Related, BankSC, Salary, etc.",
       "Landscaping, New Computer"
]
const DisplayTable = createReactClass({  
  getInitialState() {
    // console.log(rows, 'rows')
    // const rows = map(
    //     (x) => {
    //         x[1] = 'Amount Placeholder'
    //         return x
    //     }
    // )(this.props.tablerows)
    // console.log(rows, 'rows')
         return {
             headers: this.props.tablekeys,
             tableRows: this.props.tablerows            
         };
     },
  removeRow(rowIndex) {
        let rows = this.state.tableRows;
        rows.splice(rowIndex, 1)
        this.setState({
            tableRows: rows
        })

  },
  updateTable(row, column, value) {
    if (is(Number, row) && is(Number, column)) {
      let tableRows = [ ...this.state.tableRows ];
      tableRows[row][column] = value ;  //new value
      this.setState({ tableRows });
    }
    },
 render() {
 return (
  <div>
  <Table key={this.props.value}>
     <TableHeader>
            <TableRowCustom type='header'  row={this.state.headers}/>
    </TableHeader>

    <TableBody>
   {this.state.tableRows.map((row, index) => {
        return (
            <TableRowCustom hints={hintFields} removeRow={this.removeRow} onChange={this.updateTable} rownum={index} key={index} row={row}/>
        )
   })}
       </TableBody>
  </Table>
  <DefaultButton label = "Continue" tablerows={this.state.tableRows} tablekeys={this.state.tableKeys} onSomeEvent= { () => {this.props.handleChange('Actions', this.state.headers, this.state.tableRows)}} path="Actions">  </DefaultButton>

</div>
)
 }
});

export default DisplayTable;