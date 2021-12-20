import '../App.css';
import React, { useState } from 'react';
import {  Form, Input, Button, Select  } from 'antd';
import './video/rmg.avi'
const { Option } = Select;
const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};
const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};

const ShowResult = (props)=> {
    console.log('展示出来', props.url);
    return(
        <video src={props.url} height="300px" width="500px" controls="controls">
        </video>
    )
};

const Query = (props) => {
    const [form] = Form.useForm();

    var url = props.url

    var [myPath, setMyPath] = React.useState([]);

    const OnFinish = (values) => {
        var data = values;
        console.log(data);
        
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
            myPath = response.path;
            console.log('路径:',myPath);
            setMyPath(myPath);
        })
    };

    const onReset = () => {
        form.resetFields();
    };

    return (
        <div>
            <Form {...layout} form={form} name="control-hooks" onFinish={OnFinish}>
            <Form.Item
                name="species"
                label="Species"
                rules={[
                {
                    required: true,
                },
                ]}
            >
                <Select
                id="mySpecies"
                placeholder="请选择反应物"
                allowClear
                >
                <Option value="乙烷">乙烷</Option>
                </Select>
            </Form.Item>
            <Form.Item
                name="temperature"
                label="Temperature"
                rules={[
                {
                    required: true,
                },
                ]}
            >
                <Select
                id="myTemperature"
                placeholder="请选择温度"
                allowClear
                >
                <Option value=" 1350 k ">1350 'k'</Option>
                </Select>
            </Form.Item>
            <Form.Item {...tailLayout}>
                <Button type="primary" htmlType="submit" >
                Submit
                </Button>
                <Button htmlType="button" onClick={onReset}>
                Reset
                </Button>
            </Form.Item>
            </Form>
            <ShowResult url="./video/11.mp4"></ShowResult>
        </div>
    );
}

export default Query