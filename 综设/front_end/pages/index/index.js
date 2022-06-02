//index.js
var util = require('../../utils/util.js');
var summary = require('../../utils/summary.js');
var repository = require('../../utils/repository.js');
const app = getApp()
Page({
  data: {
    userInfo: {},
    todaySummary: {},
    today: '',
    process_num:0,
    thread_num:0
  },
  onLoad: function () {
    console.log('onLoad')    
    
  },
  onShow: function () {
    console.log('onshow');
    var that = this;
    var todayDate = util.formatDate(new Date());
    var process_num = app.globalData.process_num
    var thread_num = app.globalData.thread_num
    wx.request({
      url: 'http://127.0.0.1:5000/test2',
      // url: 'http://118.113.144.212:16666/test',
      method: 'POST',
      data: {
        "process_num": process_num,
        "thread_num": thread_num
      },
      headers: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        a.setData({
          message: res.data
        })
        console.log(res.data)
      }
    })
    this.setData({
      process_num: process_num,
      thread_num: thread_num,
    })
    repository.findDateNode(todayDate,(result) => {
      if (result.success) {
        var todaySummary = summary.dateDefaultSummary(result.result);
        that.setData({
          todaySummary: todaySummary,
          today: todayDate
        });
      } else {
        that.setData({
          todaySummary: {},
          today: todayDate
        });
      }
    });
  }
})
