// pages/display/display.js
const app = getApp()
var util = require('../../utils/util.js');
var wxCharts = require('../../utils/wxcharts-min.js');
var summary = require('../../utils/summary.js');
var repository = require('../../utils/repository.js');
var generateArray = function (start, end) {
  return Array.from(new Array(end + 1).keys()).slice(start)
}

var colors = [
  '#BEBEBE',
  '#FFA500'
];

var getColor = function (is_runnning) {
  var color = colors[is_runnning];
  return color;
};

var process_chart = function (cavId, name, is_running, load) {
  new wxCharts({
    canvasId: cavId,
    type: 'line',
    animation: false,
    categories: ["-12", "-10", "-8", "-6", "-4", "-2", "now"],
    series: [{
      name: "进程" + name,
      color: getColor(is_running),
      data: load
    }],
    yAxis: {
      title: "占用率",
      min: 0,
      max: 1
    },
    width: 320,
    height: 160
  });
}

var calculate_load_rate = function (list) {
  var no_status = list.slice(0, -1)
  var is_one = 0
  for (var i = 0; i < no_status.length; i++) {
    if (no_status[i] == 1) {
      is_one++
    }
  }
  var rate = is_one / no_status.length
  return rate
}

// var get_new_info = function () {
//   return {
//     0: [0, 0, 0, 0, 0, 0],
//     1: [0, 0, 1, 1, 1, 1],
//     2: [1, 1, 1, 1, 1, 1],
//     3: [0, 1, 1, 1, 1, 1],
//     4: [0, 0, 0, 0, 0, 0]
//   }

// }

function get_new_info_request(a) {
  return new Promise(resolve => {
    wx.request({
      url: 'http://127.0.0.1:5000/test',
      // url: 'http://118.113.144.212:16666/test',
      method: 'POST',
      data: {
        "Function": "get_data",
      },
      headers: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        a.setData({
          message: res.data
        })
        console.log(res.data)
        return resolve()
      }
    })
  });

}

Page({

  /**
   * 页面的初始数据
   */
  data: {
    message: {},
    inter: '',
    process_num: 0,
    thread_num: 0,
    number_list: ['0', '1', '2'],
    is_runnning_list: {},
    load_list: {}, //[ [], [], [] ],
    todaySummary: {},
    today: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */


  onLoad: function (options) {
    
    
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var process_num = app.globalData.process_num
    var thread_num = app.globalData.thread_num
    var info = {}

    //刚刚加载时，创建全0数组
    for (var i = 0; i < process_num; i++) {
      info[i] = Array(thread_num + 1).fill(0)
    }
    var is_runnning_list = {}
    var load_list = {} // { [],[],[] }
    for (var key in info) {
      is_runnning_list[key] = info[key][thread_num]
      load_list[key] = new Array(7).fill(0) //展示状态为7个状态
    }
    // console.log(this)
    this.setData({
      message: info,
      process_num: process_num,
      thread_num: thread_num,
      is_runnning_list: is_runnning_list,
      load_list: load_list
    })

    var that = this
    timer = setInterval(function () {
      get_new_info_request(that).then(res => {

        var info = that.data.message
        // console.log("use_info")
        var process_num = Object.keys(info).length
        var thread_num = info["0"].length - 1
        var new_load_rate = {}
        var new_is_running = {}
        var number_list = generateArray(0, process_num)
        for (var key in info) {
          new_load_rate[key] = calculate_load_rate(info[key])
          if (info[key][thread_num] == 0) {
            new_is_running[key] = 0
          } else {
            new_is_running[key] = 1
          }
        }
        //更新load_list
        var late_load_list = that.data.load_list
        for (var key in late_load_list) {
          late_load_list[key].push(new_load_rate[key])
          late_load_list[key].shift()
        }
        that.setData({
          message: info,
          process_num: process_num,
          thread_num: thread_num,
          load_list: late_load_list,
          is_runnning_list: new_is_running,
          number_list: number_list
        })

        process_chart("chart", "进程1", '1', that.data.load_list[2]);

        for (var key in that.data.load_list) {
          process_chart(key, key, that.data.is_runnning_list[key], that.data.load_list[key])
        }

      })
    }, 5000)

    
  },

  clearTimeInterval: function (that) {
    var interval = that.data.interval;
    clearInterval(interval)
  },
  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    var that = this;
    that.clearTimeInterval(that)
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    var that = this;
    that.clearTimeInterval(that)
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})