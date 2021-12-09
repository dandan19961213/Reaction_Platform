<template>
  <div id="wrap">
    <el-header id="header" style="height: 200px">
      <el-row>
        <el-col :span="10">
            <div>
              <div class="demo-image" style="margin-top: 30px">
                <el-image
                  style="width: 100px; height: 100px"
                  :src="
                    require('./BISTU.jpg')
                  "
                  :fit="fits"
                ></el-image>
                <el-image
                  style="width: 100px; height: 100px"
                  :src="
                    require('./ICCCAS.jpg')
                  "
                  :fit="fits"
                ></el-image>
              </div>
              <span>碳氢反应计算平台</span>
            </div>
          </el-col>
        <el-col :span="5">
            <div id="input" style="margin-top:50px; padding-right: 50px">
              <div class="sub-title">step #1</div>
            <el-input
              v-model="input"
              placeholder="例如：7"
            ></el-input>    
            </div>
            </el-col>
            <el-col :span="7">
              <div id="select" style="margin-top:50px; padding-right: 80px">
              <div class="sub-title">step #2</div>
              <el-select
                clearable 
                @change="handleSelect"
                v-model="select"
                placeholder="10"
              >
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
              >
                </el-option>
              </el-select>
              </div></el-col> 
              <div id="shuoming">
              <span>step #1：请输入化学反应范围起点（总计84个反应）</span>
              <span>step #2：请选择化学反应数量</span><br>
              <!-- <span>step #3：请选择化学反应数量</span><br> -->
              <span>注：当输入起点0，选择反应数量后将进行随机展示</span>
            </div>                      
      </el-row>
    </el-header>
    <div style="width:90%; margin:0 auto;">
      <el-row>
        <el-col :span="14">
            <div
              class="echart"
              id="echart-line"
              :style="{ width: '100%', margin: '10px auto 0', height: '700px' }"
            ></div>
        </el-col>
        <el-col :span="10">
            
            <!-- <div id="upload" v-show="showUpload" style="padding-right: 80px">
              <el-input
                type="textarea"
                rows="13"
                placeholder="分子结构(xyz)"
                v-model="text"
                :disabled="true"
              >
              </el-input>
            </div> -->
            <div
              id="result3"
              v-show="!showResult"
              v-if = "input !='0'"
            >
              <div
                id="container-01"
                class="mol-container"
                v-show="showMol"
              ></div>
              <!-- <div style="clear: both"></div> -->
              <h4>当前有{{tableList2.length}}条CO和H2的反应</h4>
              <ul class="ul3">
                <li v-for="item in tableList2">
                  <span>{{item[0]}} + {{item[1]}} = <img :src="'/static/picture/picture' + item[2] + '.png'" :alt="item[2]">
                  </span>
                </li>
              </ul>
            </div>
            <div
              id="result3"
              v-show="!showResult"
              v-if = "input =='0'"
            >
              <div
                id="container-01"
                class="mol-container"
                v-show="showMol"
              ></div>
              <h4>当前有{{tableList3.length}}条CO和H2的反应</h4>
              <ul class="ul3">
                <li v-for="item in tableList3">
                  <span>{{item[0]}} + {{item[1]}} = <img :src="'/static/picture/picture' + item[2] + '.png'" :alt="item[2]">
                  </span>
                </li>
              </ul>
            </div>
            <div
              id="result"
              v-show="showResult"
              style="margin-top: 150px"
            >
              <el-table
                :data="tableData1"
                border
                style="width: 94%; margin: 0 auto"
              >
                <el-table-column prop="分子式" label="反应物" width=""></el-table-column>
                <el-table-column
                  prop="分子系数"
                  label="配平系数"
                  width=""
                ></el-table-column>
                <el-table-column
                  prop="Gibbs/eV"
                  label="Gibbs自由能(eV)"
                  width=""
                ></el-table-column>
              </el-table>
              <el-table
                :data="tableData2"
                border
                style="width: 94%; margin: 30px auto"
              >
                <el-table-column prop="分子式" label="产物" width=""> </el-table-column>
                <el-table-column
                  prop="分子系数"
                  label="配平系数"
                  width=""
                ></el-table-column>
                <el-table-column
                  prop="Gibbs/eV"
                  label="Gibbs自由能(eV)"
                  width=""
                ></el-table-column>
              </el-table>
            </div>
        </el-col>
      </el-row>
      <div style="clear: both"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "Home",
  data() {
    return {
      showMol: false,
      showUpload: false,
      showResult: false,
      tableList2:[],
      tableList3:[],
      fits: "contain",
      input: "",
      text: "",
      options: [{
                    value: '10',
                    label: '10'
                }, {
                    value: '20',
                    label: '20'
                },{
                    value: '50',
                    label: '50'
                }],
      select: [],

      tableData1: [
        {
          分子式: "C2O",
          分子系数: "1",
          "Gibbs/eV": "2.331",
          "HOMO/eV" : "111",
          "LUMO/eV" : "111",
          
        },
        {
          分子式: "C2O",
          分子系数: "1",
          "Gibbs/eV": "2.331",
          "HOMO/eV" : "111",
          "LUMO/eV" : "111",
        },
      ],
      tableData2: [
        {
          分子式: "C2O",
          分子系数: "1",
          "Gibbs/eV": "2.331",
          "HOMO/eV" : "111",
          "LUMO/eV" : "111",
        },
      ],
    };
  },

  methods: {
    handleSelect() {
      console.log(this.input, this.select);
      var reg = /^(\d{0,5})$/g;
      if (this.input !== "" && this.select !== "") {
        if (reg.test(this.input) && parseInt(this.input) > 0 && parseInt(this.input) <= 91766 - parseInt(this.select)) {
          this.method2();         
        }else if (parseInt(this.input) == 0) {
          this.method3();
        }else {
          alert("请检查起点输入！");
        }
      } 
    },

    handleMol(val) {
      let element = $("#container-01");
      let config = { backgroundColor: "white" };
      let viewer = $3Dmol.createViewer(element, config);
      viewer.addModel(val, "xyz");
      viewer.addUnitCell();
      viewer.setStyle({}, { sphere: {} });
      viewer.zoomTo();
      viewer.render();
      viewer.setBackgroundColor(0x00ffffff);
    },

    initChart(dataObj) {
      var d = dataObj[0][0];   // node
      var dataArr = [];

      var l = dataObj[1];     // link
      var linkArr = [];

      for (var k in d) {
        // console.log(d[k]);
        if (typeof d[k] != "string") {    // d[k]:分子式，坐标
          dataArr.push({
            id: k,
            name: d[k][0],    // 分子式
            formula: eval(d[k][1]),    // 分子的坐标；  eval() 函数计算或执行参数。
          });
        } else {
          // console.log(d[k]);
          dataArr.push({
            id: k,
            name: "△G:" + d[k] + "eV",     // // d[k]:△G的值
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
        // console.log(l[i]);
        // console.log(l[i][0]);
        linkArr.push({
          source: l[i][0],    // 反应物
          //value: l[i][1],
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

    //console.log(dataArr);
    // console.log(linkArr);

      let that = this;
      let getchart = echarts.init(document.getElementById("echart-line"));
      getchart.clear();
      var option = {
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

      getchart.on("click", (param) => {
        console.log(param);
        var formula = param.data.formula;
        var G = param.data.id;
        if (formula) {
          that.text = formula;
          console.log(that.text);
          that.handleMol(that.text);
          this.showMol = true;
          this.showUpload = true;
          this.showResult = false;
        } else if (G) {
          if(G==140000 || G==140001){
            ;
          }
          else{
            that.text = G;
            this.method1(that.text);
            this.showMol = false;
            this.showUpload = false;
            this.showResult = true;
          }
        }
      });
      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        getchart.resize();
      });
            
    },

    method1(gib) {
      // console.log(gib);
      console.log(gib.split('g')[0])
      var ids = gib.split('g')[0]
      var g_val= gib.split('g')[1]
      console.log(gib.split('g')[1])
      var self = this;
      console.log(this.$api + "/method1");
      this.$http
        .post(this.$api + "/method1", {
          text1: ids,
          text2: g_val,
        })
        .then((response) => {
          var res_data = response.data;
          console.log(res_data);
          this.tableData1 = res_data.tabledata[0];
          this.tableData2 = res_data.tabledata[1];
          console.log(res_data.tabledata);
        })
        .catch(function (error) {
          console.log(error);
          // self.$router.push({ name: "servererror" });
        });
    },

    method2() {
      console.log(this.text);
      var self = this;
      console.log(this.$api + "/method2");
      this.$http
        .post(this.$api + "/method2", {
          text: self.input,
          text2: self.select,
        })
        .then((response) => {
          var res_data = response.data;
          console.log(res_data);
          self.initChart(res_data.tabledata);
          this.tableList2 = res_data.tabledata[2]
          this.showMol = false;
          this.showUpload = false;
          this.showResult = false;
        })
        .catch(function (error) {
          console.log(error);
          // self.$router.push({ name: "servererror" });
        });
    },
    method3() {
      console.log(this.text);
      var self = this;    // this指向调用这个函数的对象
      console.log(this.$api + "/method3");
      this.$http.post(this.$api + "/method3", {    // 传值给后台
          text: self.input,
          text2: self.select,
        })
        .then((response) => {
          var res_data = response.data;
          console.log(res_data);
          console.log(res_data.tabledata);
          self.initChart(res_data.tabledata);
          this.tableList3 = res_data.tabledata[2]
          console.log(this.tableList3);
          this.showMol = false;
          this.showUpload = false;
          this.showResult = false;       
        })
        .catch(function (error) {
          console.log(error);
          // self.$router.push({ name: "servererror" });
        });
    },
  },

  mounted() {
    let that = this;
    that.input = 0;
    that.select =10;
    that.method3();
    // that.text = '10\n\nO -1.7198 0.3001 -0.6366 \nC -0.5955 0.5226 0.1810 \nC 0.4990 -0.3809 -0.3810 \nO 1.6784 -0.2792 0.3172\nH -1.7928 -0.6976 -0.7744\nH -0.8417 0.2793 1.2265\nH -0.3058 1.5961 0.0499\nH 0.0687 -1.4047 -0.3970\nH 0.6048 -0.0729 -1.4556\nH 2.4047 0.1372 -0.2138'  
    // that.handleMol(that.text);
    // that.showMol = true;
    // that.showUpload = true;
  },
};
</script>

<style>
body{margin:0;}
ul li{list-style: decimal; text-align:left; text-indent:1em;}
.ul3{width:300px; margin:0 auto;}
.ul3 li{margin-bottom:10px;}
.ul3 li img{width:130px; height:100px; vertical-align: middle;}
#result3{height:700px; overflow-y: auto;}
#header {
  background-color: #ffffff;
  /* color: #fff; */
  color: #6b6c6f;
  font-size: 30px;
  line-height: 47px;
}

.el-header{
  border-color:#dddddd;
}
#wrap {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: #f4f4f4;
  color: #409eff;
}

.el-input__inner{
  border-width: 2px;
  border-color:#909399;
  font-size: 15px;
}
#input{
  color: #e2231a;
  font-size: 20px;
  text-align: center;
}
#select{
  position: relative;
  float:left;
  font-size: 20px;
  color: #e2231a;
  text-align: center;
}
#shuoming{
  position: relative;
  float:left;
  color: #C0C4CC;
  font-size: 15px;
  line-height:26px;
}
#result {
  margin-top: 50px;
  width: 530fpx;
}
#upload {
  width: 90%;
  height: 200px;
  margin: 30px auto 0;
}

.el-textarea.is-disabled .el-textarea__inner {
  color: #75777b;
}
.mol-container {
  height: 300px;
  width: 90%;
  position: relative;
  margin-top: 30px;
}
</style>
