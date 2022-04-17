import React, { useEffect } from "react";
import InitChart from "./InitChart";
import './App.css';

const Method = (props) => {
    console.log(props);
    var url = props.url
    var data = {text: '0', text2: '10'}
    // var [tableList3, setTableList3] = React.useState([]);

    useEffect(() => {
        fetch(url, {
            method: 'post',
            headers: {
              "Content-Type": "application/json;charset=utf-8",
              'Token': localStorage.getItem('token')
            },
            body: JSON.stringify(data)
        }).then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => {
            console.log('Success:', response);
            console.log('数据', response.tabledata);

            // tableList3 = response.tabledata[2];

            InitChart(response.tabledata, props.ids);
        })
    },[])
    return (
      <div className='Method'>
      </div>
    ) 
}

export default Method