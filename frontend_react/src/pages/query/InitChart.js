import * as echarts from "echarts";
import './App.css';

const InitChart = (data, ids) => {
    console.log('调用initChart了', data)
    console.log('渲染的id', ids);
    var d = data[0][0];   
    var dataArr = [];

    var l = data[1]; 
    var linkArr = [];

    for (var k in d) {
      // console.log(d[k]);
      if (typeof d[k] != "string") {    
        dataArr.push({
          id: k,
          name: d[k][0],   
          formula: eval(d[k][1]),   
        });
      } else {
        // console.log(d[k]);
        dataArr.push({
          id: k,
          name: "△G:" + d[k] + "eV",    
          itemStyle: {
            color: "#8DCC93",
            borderType: "solid",
            borderColor: "#5DB665",
            borderWidth: 4,
          },
        });
      }
    }

    for (var i = 0; i < l.length; i++) {
      linkArr.push({
        source: l[i][0],    
        target: l[i][2],
        lineStyle: {
          normal: {
            color: "#E6A23C",
            borderWidth: 4,
          },
        },
        label: {
          normal: {
            textStyle: {
              color: "#000000",
            },
          },
        },
      });
    }

    // console.log('dataArr', dataArr);
    // console.log('linkArr', linkArr);

    let that = this;
    var getchart = echarts.init(document.getElementById(ids));
    getchart.clear();

    let option = {
      tooltip: {
        formatter: "{c}",
      },
      series: [
        {
          type: "graph",
          layout: "force",
          symbolSize: 60,
          force: {
            repulsion: 3000,
            edgeLength: [10, 60],
          },
          categories: "categories",
          roam: true, // 是否可拖拽
          focusNodeAdjacency: true, // 指定的节点以及其所有邻接节点高亮
          draggable: true, //节点是否可拖拽，只在使用力引导布局的时候有用。
          edgeSymbol: ["circle", "arrow"],
          lineStyle: {
            normal: {
              width: 2,
              shadowColor: "none",
              color: "#fac858",
              // curveness: 0.1
            },
          },
          lineStyle: {
            normal: {
              opacity: 1,
              width: 2,
              // curveness: 0.1
            },
          },
          // layoutAnimation : false,
          label: {
            show: true,
          },
          data: dataArr,
          links: linkArr,
        },
      ],
    };

    getchart.setOption(option);

    // 随着屏幕大小调节图表
    window.addEventListener("resize", () => {
      getchart.resize();
    }); 
}

export default InitChart