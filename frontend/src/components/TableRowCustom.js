import React from 'react';
import {
  TableRow,
  TableRowColumn,
  TableHeaderColumn,
} from 'material-ui/Table';
import TextField from 'material-ui/TextField';
import NavigationClose from 'material-ui/svg-icons/navigation/close';


const TableRowCustom = (props) => {
    const { order, ...otherProps } = props;
    let lastRow = ''
    if (props.type !== 'header') {
            lastRow = <TableRowColumn><NavigationClose onClick={(e)=> props.removeRow(props.rownum)}/> Remove Row</TableRowColumn>
      }else {
        lastRow = <TableRowColumn> </TableRowColumn>
     }
return(
     <TableRow {...otherProps }>
      {props.row.map((item, index) => {
                if (props.type === 'header') {
                     return (
                            <TableHeaderColumn key={index}>
                                {item}
                            </TableHeaderColumn>
                            )
                }else{
                  return (
                       <TableRowColumn key={index}>
                       <TextField
                        id={`${props.rownum}: ${index}`} 
                          onChange={(e)=> props.onChange(props.rownum, index, e.target.value)} 
                          value={item}
                          hintText={props.hints[index]}
                       />
                      </TableRowColumn>
                      )
                  
                }
      })}
           {lastRow}

     </TableRow>


);
}
export default TableRowCustom;