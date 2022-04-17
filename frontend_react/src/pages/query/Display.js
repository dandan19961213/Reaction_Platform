import React from "react";
import './App.css';

class Display extends React.Component {
    constructor(props){
      super(props)
    }
    render(){
      // console.log('Display数量', this.props.reactlist );
      return(
        <div>
          <h4 className='Display'>当前有{this.props.reactlist.length}条CO和H2的反应</h4>
          <ul className='ul3'>
            {
              this.props.reactlist.map(function(item){
                let imgs = require("./image/picture" + item[2] + ".png").default;
                // console.log(imgs);
                return(
                  <li> 
                    {item[0]} + {item[1]} = <img src={ imgs }  className='Display-img' alt="" />
                  </li>
                ) 
              })
            }
          </ul>
        </div>
      ) 
    }
}

export default Display